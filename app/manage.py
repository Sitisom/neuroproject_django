#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from app_utils import create_directory, get_model_bin


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neuro.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Creating required directories
    results_img_directory = '/usr/src/app/results/image/'
    create_directory(results_img_directory)

    results_video_directory = '/usr/src/app/results/video/'
    create_directory(results_video_directory)

    model_directory = '/usr/src/app/models/'
    create_directory(model_directory)

    # Downloading required models
    artistic_model_url = 'https://www.dropbox.com/s/zkehq1uwahhbc2o/ColorizeArtistic_gen.pth?dl=0'
    get_model_bin(artistic_model_url, os.path.join(model_directory, 'ColorizeArtistic_gen.pth'))

    video_model_url = 'https://www.dropbox.com/s/336vn9y4qwyg9yz/ColorizeVideo_gen.pth?dl=0'
    get_model_bin(video_model_url, os.path.join(model_directory, 'ColorizeVideo_gen.pth'))

    esrgan_RRDB_model_url = 'https://www.dropbox.com/s/37u51p6uyk4vnec/RRDB_ESRGAN_x4.pth?dl=0'
    get_model_bin(esrgan_RRDB_model_url, os.path.join(model_directory, 'RRDB_ESRGAN_x4.pth'))

    dain_model_url = 'https://www.dropbox.com/s/7xw79j6r00xz0vv/DAIN.pth?dl=0'
    get_model_bin(dain_model_url, os.path.join(model_directory, 'DAIN.pth'))

    main()
