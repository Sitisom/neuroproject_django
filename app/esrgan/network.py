import torch

import os
from os.path import join

import fastai
import cv2
import numpy

from . import RRDBNet_arch as arch

from app_utils import get_name

results_img_directory = '/usr/src/app/results/image/'
results_video_directory = '/usr/src/app/results/video/'
model_directory = '/usr/src/app/models/'

bwframes_root = join(results_video_directory, "bwframes")


torch.backends.cudnn.benchmark=True
os.environ['CUDA_VISIBLE_DEVICES']='0'

def esrgan_img(input_path):
    _interpolate(input_path, results_img_directory)

def esrgan_video(input_path):
    build_folder = join(bwframes_root, get_name(input_path)) + '/'
    files = [f for f in os.listdir(build_folder) if os.path.isfile(join(build_folder, f))]

    for filename in files:
        _interpolate(join(build_folder, filename), build_folder)

def _interpolate(input_path, output_path):
    model_path = model_directory + 'RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
    device = torch.device('cpu') #paste in CPU or CUDA

    model = arch.RRDBNet(3, 3, 64, 23, gc=32) #creating model for image processing
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device)

    filename = os.path.basename(input_path)

    # read images
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(numpy.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()

    output = numpy.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite(output_path + filename, output)