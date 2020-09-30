FROM ubuntu:20.04
ENV PATH="/home/docker/layers/bin:${PATH}"
ENV TZ=Europe/Oslo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && \
      apt -y install sudo

RUN apt install -y python3-pip
RUN apt install -y vim nano
RUN apt install -y make

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN printf '\ndocker ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker
WORKDIR /home/docker/

RUN sudo pip3 install pyinstaller
RUN sudo pip3 install pyyaml
RUN sudo pip3 install typeguard

#COPY . layers
RUN sudo chown -R docker:docker .
# RUN layers new level1
# RUN cd level1; layers new ../level2
# RUN touch level1/test1
# RUN touch level1/test2
# RUN touch level2/test3
# RUN touch level2/test4
# RUN cd level1; layers sync
# RUN cd level2; layers mv --up ./test3
# RUN sudo chown -R docker:docker .
# RUN cd layers; make clean build

WORKDIR /home/docker/layers

# RUN sudo mkdir -p /usr/src/
# RUN sudo cp ./layers/dist/layers /usr/bin/

