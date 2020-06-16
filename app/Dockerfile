# pull official base image
From nvcr.io/nvidia/pytorch:19.04-py3

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get -y update \
    && apt-get install -y netcat postgresql postgresql-contrib python-psycopg2 libpq-dev gcc python3-dev musl-dev ffmpeg

RUN mkdir -p /root/.torch/models
RUN mkdir -p /usr/src/app/models

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

#building extension for dain
#COPY ./dain/my_package/build.sh /usr/src/app/dain/my_package
#RUN CUDA_VISIBLE_DEVICES=0 /usr/src/app/dain/my_package/build.sh
#COPY . /usr/src/app/

#COPY ./dain/PWCNet/correlation_package_pytorch1_0/build.sh /usr/src/app/dain/PWCNet/correlation_package_pytorch1_0
#RUN CUDA_VISIBLE_DEVICES=0 /usr/src/app/dain/PWCNet/correlation_package_pytorch1_0/build.sh
#COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]