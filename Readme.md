# Neuro-project
Проект собранный с помощью Docker на Django. Данный проект позволяет увеличивать разрешение видео, количество его кадров, а также придать цвет черно-белым картинам. В проекте использованы нейросети:
* [DAIN](https://github.com/baowenbo/DAIN) - не поддерживается
* [ESRGAN](https://github.com/xinntao/ESRGAN)
* [DeOldify](https://github.com/jantic/DeOldify)

## Зависимости и ПО
* Windows не поддерживается! (связано с nvidia-docker2)
* Протестировано на Linux Mint (Ubuntu 18.04)
* [Docker Linux](https://runnable.com/docker/install-docker-on-linux):
```
$ sudo apt-get install docker-engine -y
$ sudo service docker start
```
* [Docker-compose](https://docs.docker.com/compose/install/)
```
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
* [nvidia-docker2](https://github.com/NVIDIA/nvidia-docker/wiki/Installation-(version-2.0))
```
$ sudo apt-get install nvidia-docker2
$ sudo pkill -SIGHUP dockerd
```

## Запуск проекта
* Клонировать данный репозиторий
```
$ git clone https://github.com/Sitisom/neuroproject_flask.git
```
* В папке с проектом в терминале набрать:
```
$ docker-compose up --build
```
* Локальный сервер будет запущен на http://localhost:8000/