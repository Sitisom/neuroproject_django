import os
import shutil
from os.path import join
import requests
import random
import _thread as thread
from uuid import uuid4

import numpy as np
import skimage
import ffmpeg
import cv2
from skimage.filters import gaussian
from PIL import Image
from pathlib import Path

video_workfolder = '/usr/src/app/results/video'
result_folder = video_workfolder
bwframes_root = join(video_workfolder, "bwframes")
audio_root = join(video_workfolder, "audio")
build_root = join(video_workfolder, "buildframes")

def randomString(stringLength=16):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_name(source_path):
    return os.path.splitext(os.path.basename(source_path))[0]

def extract_raw_images(source_path):
    bwframes_folder = join(bwframes_root, get_name(source_path))
    bwframe_path_template = join(bwframes_folder, '%5d.jpg')
    create_directory(bwframe_path_template)

    ffmpeg.input(source_path).output(
            bwframe_path_template, format='image2', vcodec='mjpeg', qscale=0
        ).run(capture_stdout=True)

def get_fps(source_path):
        probe = ffmpeg.probe(str(source_path))
        stream_data = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
            None,
        )
        return stream_data['avg_frame_rate']

def build_video(source_path):
        colorized_path = join(result_folder, get_name(source_path) + '_build.mp4')

        fps = get_fps(source_path)

        build_folder = join(bwframes_root, get_name(source_path)) + '/'
        bwframe_path_template = join(build_folder, '%5d.jpg')

        ffmpeg.input(
            str(bwframe_path_template),
            format='image2',
            vcodec='mjpeg',
            framerate=fps,
        ).output(str(colorized_path), crf=17, vcodec='libx264').run(capture_stdout=True)

def compress_image(image, path_original):
    size = 1920, 1080
    width = 1920
    height = 1080

    name = os.path.basename(path_original).split('.')
    first_name = os.path.join(os.path.dirname(path_original), name[0] + '.jpg')

    if image.size[0] > width and image.size[1] > height:
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(first_name, quality=85)
    elif image.size[0] > width:
        wpercent = (width/float(image.size[0]))
        height = int((float(image.size[1])*float(wpercent)))
        image = image.resize((width,height), PIL.Image.ANTIALIAS)
        image.save(first_name,quality=85)
    elif image.size[1] > height:
        wpercent = (height/float(image.size[1]))
        width = int((float(image.size[0])*float(wpercent)))
        image = image.resize((width,height), Image.ANTIALIAS)
        image.save(first_name, quality=85)
    else:
        image.save(first_name, quality=85)


def convertToJPG(path_original):
    img = Image.open(path_original)
    name = os.path.basename(path_original).split('.')
    first_name = os.path.join(os.path.dirname(path_original), name[0] + '.jpg')

    if img.format == "JPEG":
        image = img.convert('RGB')
        compress_image(image, path_original)
        img.close()

    elif img.format == "GIF":
        i = img.convert("RGBA")
        bg = Image.new("RGBA", i.size)
        image = Image.composite(i, bg, i)
        compress_image(image, path_original)
        img.close()

    elif img.format == "PNG":
        try:
            image = Image.new("RGB", img.size, (255,255,255))
            image.paste(img,img)
            compress_image(image, path_original)
        except ValueError:
            image = img.convert('RGB')
            compress_image(image, path_original)
        
        img.close()

    elif img.format == "BMP":
        image = img.convert('RGB')
        compress_image(image, path_original)
        img.close()



def blur(image, x0, x1, y0, y1, sigma=1, multichannel=True):
    y0, y1 = min(y0, y1), max(y0, y1)
    x0, x1 = min(x0, x1), max(x0, x1)
    im = image.copy()
    sub_im = im[y0:y1,x0:x1].copy()
    blur_sub_im = gaussian(sub_im, sigma=sigma, multichannel=multichannel)
    blur_sub_im = np.round(255 * blur_sub_im)
    im[y0:y1,x0:x1] = blur_sub_im
    return im



def download(url, filename):
    data = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(data)

    return filename


def generate_random_filename(source_filename):
    filename = str(uuid4())
    filename = filename + os.path.splitext(source_filename)[1]
    return filename


def clean_me(filename):
    if os.path.exists(filename):
        os.remove(filename)


def clean_all(files):
    for me in files:
        clean_me(me)


def create_directory(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def clean_directory(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



def get_model_bin(url, output_path):
    if not os.path.exists(output_path):
        create_directory(output_path)
        cmd = "wget -O %s %s" % (output_path, url)
        print(cmd)
        os.system(cmd)

    return output_path


#model_list = [(url, output_path), (url, output_path)]
def get_multi_model_bin(model_list):
    for m in model_list:
        thread.start_new_thread(get_model_bin, m)

