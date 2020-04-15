import torch
torch.cuda.current_device() #command for turning CUDA on

import os
from os.path import join 

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import UploadForm

from app_utils import generate_random_filename
from app_utils import clean_me, clean_directory, create_directory
from app_utils import convertToJPG
from app_utils import extract_raw_images
from app_utils import build_video

from deoldify.network import colorize_image, colorize_video
from esrgan.network import esrgan_img, esrgan_video

torch.backends.cudnn.benchmark=True
os.environ['CUDA_VISIBLE_DEVICES']='0'

file_image_ext = ('.jpg', '.jpeg', '.png', '.gif')
file_video_ext = ('.mp4')

results_img_directory = '/usr/src/app/results/image/'
results_video_directory = '/usr/src/app/results/video/'

class Index(View):
    template = 'index.html'

    def get(self, request):
        data = dict()
        data['form'] = UploadForm()

        return render(request, self.template, data)

    def post(self, request):
        #clean_directory(results_img_directory)
        #clean_directory(results_video_directory)

        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            for file in request.FILES.getlist('files'):
                file_full_name = generate_random_filename(file.name)
                file_name, file_ext = os.path.splitext(file_full_name)
                file_type = 'image' if file_ext in file_image_ext else 'video'
                file_path = join((results_img_directory if file_type == 'image' else results_video_directory), file_full_name)
                
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                dain = False #val_form.dain
                deoldify = form.cleaned_data['deoldify']
                esrgan = form.cleaned_data['esrgan']

                if file_type == 'image' and file_ext != '.jpg':
                    convertToJPG(file_path)
                    clean_me(file_path)
                    file_path = join(os.path.dirname(file_path), file_name + '.jpg')

                if file_type == 'video':
                    extract_raw_images(file_path)
                    if dain:
                        pass
                    if deoldify:
                        colorize_video(file_path)
                    if esrgan:
                        esrgan_video(file_path)
                    build_video(file_path)
                else:
                    if dain:
                        pass
                    if deoldify:
                        colorize_image(file_path)
                    if esrgan:
                        esrgan_img(file_path)
            return HttpResponseRedirect('/success')
        
        else:
            data = dict()
            data['form'] = UploadForm()
            data['answer'] = "Something gone wrong, try again"

            return render(request, self.template, data)

class Success(View):
    template = 'success.html'

    def get(self, request):
        return render(request, self.template)