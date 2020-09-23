FROM ubuntu:20.04

ENV TZ=Europe/Oslo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && \
      apt -y install sudo

RUN apt install -y python3-pip

RUN apt install -y vim nano

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN printf '\ndocker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker
WORKDIR /home/docker/

RUN sudo mkdir -p /usr/src/layers
RUN sudo chown docker /usr/src/layers
COPY . /usr/src/layers
COPY layers /usr/bin

# Install layers

#


