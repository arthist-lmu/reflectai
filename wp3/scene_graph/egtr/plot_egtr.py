from glob import glob
import argparse

import json
import sys
import torch
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from model.deformable_detr import DeformableDetrConfig, DeformableDetrFeatureExtractor
from model.egtr import DetrForSceneGraphGeneration


def parse_args():
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-c", "--checkpoint_path", help="path to checkpoint dir")
    parser.add_argument("-o", "--output_path", help="path to the output file")
    parser.add_argument("-i", "--image_path", help="path to the image file")
    args = parser.parse_args()
    return args


def main():

    args = parse_args()

    # YOUR_ARTIFACT_PATH = "egtr__pretrained_detr__SenseTime__deformable-detr__batch__32__epochs__150_50__lr__1e-05_0.0001__visual_genome__finetune__version_0/batch__64__epochs__50_25__lr__2e-07_2e-06_0.0002__visual_genome__finetune/version_0"
    # YOUR_IMAGE_PATH = "/nfs/home/springsteinm/tmp/reflectai_example_2.jpg"
    # YOUR_IMAGE_PATH = "/nfs/data/visual_genome/images/1009.jpg"
    YOUR_OBJ_THRESHOLD = 0.3
    YOUR_REL_THRESHOLD = 1e-4

    # config
    architecture = "SenseTime/deformable-detr"
    min_size = 800
    max_size = 1333
    artifact_path = args.checkpoint_path

    # feature extractor
    feature_extractor = DeformableDetrFeatureExtractor.from_pretrained(
        architecture, size=min_size, max_size=max_size
    )

    # inference image
    pil_image = Image.open(args.image_path)
    image = feature_extractor(pil_image, return_tensors="pt")

    # model
    config = DeformableDetrConfig.from_pretrained(artifact_path)
    model = DetrForSceneGraphGeneration.from_pretrained(
        architecture, config=config, ignore_mismatched_sizes=True
    )
    ckpt_path = sorted(
        glob(f"{artifact_path}/checkpoints/epoch=*.ckpt"),
        key=lambda x: int(x.split("epoch=")[1].split("-")[0]),
    )[-1]
    state_dict = torch.load(ckpt_path, map_location="cpu")["state_dict"]
    for k in list(state_dict.keys()):
        state_dict[k[6:]] = state_dict.pop(k)  # "model."

    model.load_state_dict(state_dict)
    model.cuda()
    model.eval()

    # output
    outputs = model(
        pixel_values=image["pixel_values"].cuda(),
        pixel_mask=image["pixel_mask"].cuda(),
        output_attention_states=True,
    )

    pred_logits = outputs["logits"][0]
    obj_scores, pred_classes = torch.max(pred_logits.softmax(-1), -1)
    pred_boxes = outputs["pred_boxes"][0]

    pred_connectivity = outputs["pred_connectivity"][0]
    pred_rel = outputs["pred_rel"][0]
    pred_rel = torch.mul(pred_rel, pred_connectivity)

    # get valid objects and triplets
    obj_threshold = YOUR_OBJ_THRESHOLD
    valid_obj_indices = (obj_scores >= obj_threshold).nonzero()[:, 0]
    print(valid_obj_indices)

    valid_obj_classes = pred_classes[valid_obj_indices]  # [num_valid_objects]
    valid_obj_boxes = pred_boxes[valid_obj_indices]  # [num_valid_objects, 4]
    print(valid_obj_classes)
    print(valid_obj_boxes)

    rel_threshold = YOUR_REL_THRESHOLD
    print(pred_rel)
    valid_triplets = (
        pred_rel[valid_obj_indices][:, valid_obj_indices] >= rel_threshold
    ).nonzero()  # [num_valid_triplets, 3]
    print(valid_triplets)

    np_image = np.array(pil_image)
    print(np_image.shape)

    with open("vg_label.json") as f:
        id2label = json.load(f)
    with open("vg_relation.json") as f:
        id2relation = json.load(f)

    fig, ax = plt.subplots(1)
    plt.imshow(np_image)
    for obj in valid_obj_indices.cpu().numpy().tolist():
        valid_obj_classes = (
            pred_classes[obj].detach().cpu().numpy()
        )  # [num_valid_objects]
        valid_obj_boxes = (
            pred_boxes[obj].detach().cpu().numpy()
        )  # [num_valid_objects, 4]
        print(valid_obj_classes)
        print(valid_obj_boxes)
        x = valid_obj_boxes[0] * np_image.shape[0]
        y = valid_obj_boxes[1] * np_image.shape[1]
        width = valid_obj_boxes[2] * np_image.shape[0]
        height = valid_obj_boxes[3] * np_image.shape[1]

        x_center, y_center, width, height = valid_obj_boxes
        x_max = int((x_center + width / 2) * pil_image.width)
        y_max = int((y_center + height / 2) * pil_image.height)
        x_min = int((x_center - width / 2) * pil_image.width)
        y_min = int((y_center - height / 2) * pil_image.height)
        print(x_max, y_max, x_min, y_min)
        ax.add_patch(
            plt.Rectangle(
                (x_max, y_min),
                x_max - x_min,
                y_max - y_min,
                ls="--",
                lw=2,
                ec="c",
                fc="none",
            )
        )
        plt.text((x_max, y_min), id2label[valid_obj_classes.item()])

    plt.axis("off")
    plt.savefig("plot.pdf", bbox_inches="tight")


if __name__ == "__main__":
    sys.exit(main())
