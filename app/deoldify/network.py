import os

import torch
import fastai
import cv2
import numpy

from .deoldify.visualize import *

torch.backends.cudnn.benchmark=True
#os.environ['CUDA_VISIBLE_DEVICES']='0'

results_img_directory = '/data/results/image/'
results_video_directory = '/data/results/video/'
model_directory = '/data/models/'


def colorize_image(input_path):

    #output_path = os.path.join(results_img_directory, os.path.basename(input_path))

    render_factor = 35

    image_colorizer = get_image_colorizer(artistic=True)

    image_colorizer.plot_transformed_image(path=input_path, figsize=(20,20),
    render_factor=render_factor, display_render_factor=True, compare=False)

def colorize_video(input_path):

    #output_path = os.path.join(results_video_directory, os.path.basename(input_path))

    render_factor = 35

    video_colorizer = get_video_colorizer()

    filename = os.path.basename(input_path)
    video_colorizer.colorize_from_file_name(file_name=filename, render_factor=render_factor)
        