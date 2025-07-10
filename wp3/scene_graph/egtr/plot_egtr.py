from glob import glob
import argparse
import os
import json
import sys
import torch
from PIL import Image
import numpy as np

import matplotlib.cm as cm
import matplotlib.pyplot as plt

from model.deformable_detr import DeformableDetrConfig, DeformableDetrFeatureExtractor
from transformers import AutoImageProcessor
from model.egtr import DetrForSceneGraphGeneration
from data.visual_genome import VGDataset


def parse_args():
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-c", "--checkpoint-path", help="path to checkpoint dir")
    parser.add_argument("-o", "--output-path", help="path to the output file")
    parser.add_argument("-i", "--image-path", help="path to the image file")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument(
        "--split", type=str, default="test", choices=["train", "val", "test"]
    )
    parser.add_argument(
        "--num-queries",
        type=int,
        default=200,
        help="How many potential objects the model “asks” about in each image. (typically 200 for Visual Genome, matching the config)",
    )
    parser.add_argument("--data-path", type=str, default="dataset/visual_genome")
    args = parser.parse_args()
    return args


class SceneGraphPredictorEGTR:
    def __init__(self, config):
        self.config = config
        artifact_path = self.config.get("artifact_path")
        architecture = self.config.get("architecture", "SenseTime/deformable-detr")
        self.device = self.config.get("device")
        min_size = self.config.get("min_size", 800)
        max_size = self.config.get("max_size", 1333)

        with open("vg_label.json") as f:
            self.id2label = json.load(f)
        with open("vg_relation.json") as f:
            self.id2relation = json.load(f)

        detr_config = DeformableDetrConfig.from_pretrained(artifact_path)
        self.model = DetrForSceneGraphGeneration.from_pretrained(
            architecture, config=detr_config, ignore_mismatched_sizes=True
        )

        self.image_processor = AutoImageProcessor.from_pretrained(architecture)
        ckpt_paths = sorted(
            glob(os.path.join(artifact_path, "checkpoints", "epoch=*.ckpt")),
            key=lambda x: int(x.split("epoch=")[1].split("-")[0]),
        )
        if not ckpt_paths:
            raise FileNotFoundError("No checkpoint files found in the artifact path.")
        ckpt_path = ckpt_paths[-1]
        state_dict = torch.load(ckpt_path, map_location="cpu")["state_dict"]
        for k in list(state_dict.keys()):
            state_dict[k[6:]] = state_dict.pop(k)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()

        self.feature_extractor = DeformableDetrFeatureExtractor.from_pretrained(
            architecture, size=min_size, max_size=max_size
        )

    @torch.no_grad()
    def __call__(self, image, obj_threshold=0.25, rel_threshold=0.0001, top_k=20):
        np_image = np.array(image)
        image_input = self.feature_extractor(image, return_tensors="pt")
        image_input = {k: v.to(self.device) for k, v in image_input.items()}

        outputs = self.model(
            pixel_values=image_input["pixel_values"],
            pixel_mask=image_input["pixel_mask"],
            output_attention_states=True,
        )

        pred_logits = outputs["logits"][0]
        obj_scores, pred_classes = torch.max(pred_logits.softmax(-1), dim=-1)
        pred_boxes = outputs["pred_boxes"][0]

        boxes_post_processed = self.image_processor.post_process_object_detection(
            outputs,
            threshold=0.0,
            target_sizes=torch.tensor([np_image.shape[:-1]]),
            top_k=200,
        )[0]

        valid_obj_mask = obj_scores >= obj_threshold
        if valid_obj_mask.sum() == 0:
            return {"triplets": [], "subjects": [], "predicates": [], "objects": []}

        valid_obj_indices = valid_obj_mask.nonzero(as_tuple=False).squeeze(1)
        valid_obj_scores = obj_scores[valid_obj_indices]
        valid_pred_classes = pred_classes[valid_obj_indices]
        valid_obj_boxes = (
            pred_boxes[valid_obj_indices].cpu().numpy()
        )  # [num_valid_objects, 4]

        scores = boxes_post_processed["scores"][valid_obj_indices].cpu().numpy()
        labels = boxes_post_processed["labels"][valid_obj_indices].cpu().numpy()
        boxes = boxes_post_processed["boxes"][valid_obj_indices].cpu().numpy()

        pred_rel = outputs["pred_rel"][0]
        pred_connectivity = outputs["pred_connectivity"][0]
        pred_rel = pred_rel * pred_connectivity
        valid_pred_rel = pred_rel[valid_obj_indices][:, valid_obj_indices]

        best_rel_score, best_rel_class = torch.max(valid_pred_rel, dim=-1)

        valid_obj_scores = valid_obj_scores.unsqueeze(1)
        sub_ob_scores = valid_obj_scores * valid_obj_scores.t()
        diag_idx = torch.arange(sub_ob_scores.size(0), device=self.device)
        sub_ob_scores[diag_idx, diag_idx] = 0.0

        triplet_scores = best_rel_score * sub_ob_scores
        triplet_scores_np = triplet_scores.cpu().numpy()

        valid_pairs = np.where(triplet_scores_np >= rel_threshold)
        if len(valid_pairs[0]) == 0:
            return {
                "triplets": [],
                "subjects": [],
                "predicates": [],
                "objects": [],
                "boxes": [],
            }

        pairs = np.stack(valid_pairs, axis=-1)
        pair_scores = triplet_scores_np[valid_pairs]

        sorted_indices = np.argsort(pair_scores)[::-1]
        top_pairs = pairs[sorted_indices][:top_k]
        top_scores = pair_scores[sorted_indices][:top_k]

        output_boxes = []
        for score, label, box in zip(scores, labels, boxes):
            label = label.item()
            box = [round(i, 2) for i in box.tolist()]
            output_boxes.append(
                {
                    "box": box,
                    "score": score,
                    "label": self.id2label.get(str(label), f"obj_{label}"),
                }
            )

        triplets = []
        subjects = []
        subjects_boxes = []

        predicates = []
        objects = []
        objects_boxes = []

        for idx, (i, j) in enumerate(top_pairs):
            subject_label = self.id2label.get(
                str(valid_pred_classes[i].item()), f"obj_{valid_pred_classes[i].item()}"
            )
            object_label = self.id2label.get(
                str(valid_pred_classes[j].item()), f"obj_{valid_pred_classes[j].item()}"
            )
            predicate_label = self.id2relation.get(
                str(best_rel_class[i, j].item()), f"rel_{best_rel_class[i, j].item()}"
            )
            triplets.append(
                {
                    "subject": subject_label,
                    "predicate": predicate_label,
                    "object": object_label,
                    "score": float(top_scores[idx]),
                }
            )
            subjects.append(subject_label)
            subjects_boxes.append(boxes[i])
            predicates.append(predicate_label)
            objects.append(object_label)
            objects_boxes.append(boxes[j])

        return {
            "triplets": triplets,
            "subjects": subjects,
            "subjects_boxes": subjects_boxes,
            "predicates": predicates,
            "objects": objects,
            "objects_boxes": objects_boxes,
            "boxes": output_boxes,
        }


def main():

    args = parse_args()

    egtr = SceneGraphPredictorEGTR(
        config={"device": args.device, "artifact_path": args.checkpoint_path}
    )
    
    pil_image = Image.open(args.image_path).convert("RGB")
    np_image = np.array(pil_image)

    egtr_output = egtr(pil_image)

    fig, ax = plt.subplots(1)
    plt.imshow(np_image)

    colors = cm.rainbow(np.linspace(0, 1, len(egtr_output["boxes"])))

    for i, (sub, trip, box) in enumerate(
        zip(
            egtr_output["subjects"],
            egtr_output["triplets"],
            egtr_output["subjects_boxes"],
        )
    ):
        print(trip)
        x = box[0]
        y = box[1]
        width = box[2] - box[0]
        height = box[3] - box[1]

        # print(x_max, y_max, x_min, y_min)
        ax.add_patch(
            plt.Rectangle(
                (x, y),
                width,
                height,
                ls="--",
                lw=2,
                ec=colors[i],
                fc="none",
            )
        )
        plt.text(x+2, y+2, sub, color=colors[i])

    plt.axis("off")
    plt.savefig(args.output_path, bbox_inches="tight")


if __name__ == "__main__":
    sys.exit(main())
