#!/usr/bin/env python3
import os
import sys
import shutil
import yaml
import attrdict
import imageio
import torch
import numpy as np
import open3d as o3d
import numpy as np
import sys 

if len(sys.argv) < 2:
    print("Please specify output folder name")

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api import depth_completion_api
from api import utils as api_utils

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = torch.device('cpu')
print(f"Using device: {device}")
# Paths
case_name = sys.argv[1]
CONFIG_FILE_PATH = "config/config.yaml"
RGB_PATH = f"../test_data/{case_name}/rgb_image.npy"
DEPTH_PATH = f"../test_data/{case_name}/input_depth.npy"

with open(CONFIG_FILE_PATH) as fd:
    config_yaml = yaml.safe_load(fd)
config = attrdict.AttrDict(config_yaml)

results_dir = f"./results_single/{case_name}"
os.makedirs(results_dir, exist_ok=True)
shutil.copy2(CONFIG_FILE_PATH, os.path.join(results_dir, 'config.yaml'))

# Depth Completion API
outputImgHeight = int(config.depth2depth.yres)
outputImgWidth = int(config.depth2depth.xres)

depthcomplete = depth_completion_api.DepthToDepthCompletion(
    normalsWeightsFile=config.normals.pathWeightsFile,
    outlinesWeightsFile=config.outlines.pathWeightsFile,
    masksWeightsFile=config.masks.pathWeightsFile,
    normalsModel=config.normals.model,
    outlinesModel=config.outlines.model,
    masksModel=config.masks.model,
    depth2depthExecutable=config.depth2depth.pathExecutable,
    outputImgHeight=outputImgHeight,
    outputImgWidth=outputImgWidth,
    fx=int(config.depth2depth.fx),
    fy=int(config.depth2depth.fy),
    cx=int(config.depth2depth.cx),
    cy=int(config.depth2depth.cy),
    filter_d=config.outputDepthFilter.d,
    filter_sigmaColor=config.outputDepthFilter.sigmaColor,
    filter_sigmaSpace=config.outputDepthFilter.sigmaSpace,
    maskinferenceHeight=config.masks.inferenceHeight,
    maskinferenceWidth=config.masks.inferenceWidth,
    normalsInferenceHeight=config.normals.inferenceHeight,
    normalsInferenceWidth=config.normals.inferenceWidth,
    outlinesInferenceHeight=config.normals.inferenceHeight,
    outlinesInferenceWidth=config.normals.inferenceWidth,
    min_depth=config.depthVisualization.minDepth,
    max_depth=config.depthVisualization.maxDepth,
    tmp_dir=results_dir
)

color_img = np.load(RGB_PATH)
input_depth = np.load(DEPTH_PATH)

# Prediction
output_depth, filtered_output_depth = depthcomplete.depth_completion(
    color_img,
    input_depth,
    inertia_weight=float(config.depth2depth.inertia_weight),
    smoothness_weight=float(config.depth2depth.smoothness_weight),
    tangent_weight=float(config.depth2depth.tangent_weight),
    mode_modify_input_depth=config.modifyInputDepth.mode,
    dilate_mask=True
)

# Results
import matplotlib.pyplot as plt
plt.imsave(os.path.join(results_dir, "output_depth.png"), output_depth, cmap='viridis')
plt.imsave(os.path.join(results_dir, "input.jpg"), color_img, cmap='viridis')
plt.imsave(os.path.join(results_dir, "filtered_output_depth.png"), filtered_output_depth, cmap='viridis')

# Save PLY
api_utils.write_point_cloud(os.path.join(results_dir, "pointcloud.ply"), color_img, filtered_output_depth,
    fx=int(config.depth2depth.fx),
    fy=int(config.depth2depth.fy),
    cx=int(config.depth2depth.cx),
    cy=int(config.depth2depth.cy),
)
print(f"Results saved in {results_dir}")

#Run with: python single_predict.py case_base_name 