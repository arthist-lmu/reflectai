from glob import glob
import argparse
import json
import torch
from PIL import Image
import matplotlib.pyplot as plt

from model.deformable_detr import DeformableDetrConfig, DeformableDetrFeatureExtractor
from model.egtr import DetrForSceneGraphGeneration



def parse_args():
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_paths", nargs="+", help="path to input files")
    parser.add_argument("-o", "--output_path", help="path to the output file")
    parser.add_argument("-c", "--cache_path", help="path to a cache folder")
    parser.add_argument("-p", "--pipeline", help="pipeline definition input")
    parser.add_argument(
        "-n", "--number", type=int, help="number of samples selected from the dataset"
    )
    parser.add_argument(
        "-t", "--tmp_path", help="save single step results in a tmp folder"
    )
    args = parser.parse_args()
    return args

# def main():
#     pass

# if __name__ == "__main__":
#     sys.exit(main())

YOUR_ARTIFACT_PATH = "egtr__pretrained_detr__SenseTime__deformable-detr__batch__32__epochs__150_50__lr__1e-05_0.0001__visual_genome__finetune__version_0/batch__64__epochs__50_25__lr__2e-07_2e-06_0.0002__visual_genome__finetune/version_0"
YOUR_IMAGE_PATH = "/nfs/home/ritterd/reflect/reflectai/wp3/scene_graph/egtr/Q650635.jpg"
YOUR_OBJ_THRESHOLD = 0.3
YOUR_REL_THRESHOLD = 1e-4

# config
architecture = "SenseTime/deformable-detr"
min_size = 800
max_size = 1333
artifact_path = YOUR_ARTIFACT_PATH

# feature extractor
feature_extractor = DeformableDetrFeatureExtractor.from_pretrained(
    architecture, size=min_size, max_size=max_size
)

# inference image
image = Image.open(YOUR_IMAGE_PATH)
image = feature_extractor(image, return_tensors="pt")

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
    pixel_values=image['pixel_values'].cuda(),
    pixel_mask=image['pixel_mask'].cuda(),
    output_attention_states=True
)

#print(outputs)

pred_logits = outputs['logits'][0]
obj_scores, pred_classes = torch.max(pred_logits.softmax(-1), -1)
pred_boxes = outputs['pred_boxes'][0]

pred_connectivity = outputs['pred_connectivity'][0]
pred_rel = outputs['pred_rel'][0]
pred_rel = torch.mul(pred_rel, pred_connectivity)

# get valid objects and triplets
obj_threshold = YOUR_OBJ_THRESHOLD
valid_obj_indices = (obj_scores >= obj_threshold).nonzero()[:, 0]
#print(valid_obj_indices)

valid_obj_classes = pred_classes[valid_obj_indices] # [num_valid_objects]
valid_obj_boxes = pred_boxes[valid_obj_indices] # [num_valid_objects, 4]
#print(valid_obj_classes)
#print(valid_obj_boxes)

rel_threshold = YOUR_REL_THRESHOLD
#print(pred_rel)
valid_triplets = (pred_rel[valid_obj_indices][:, valid_obj_indices] >= rel_threshold).nonzero() # [num_valid_triplets, 3]
#print(valid_triplets)

with open("vg_label.json") as f:
    id2label = json.load(f)

with open("vg_relation.json") as f:
    id2relation = json.load(f)


triplets = []
for trip in valid_triplets:
    triplets.append([id2label[str(trip[0].item())], 
                    id2relation[str(trip[1].item())], 
                    id2label[str(trip[2].item())]])
for a in triplets:
    print(a)


