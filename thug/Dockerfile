# This Docker image encapsulates Thug, a low-interaction honeyclient,
# which was created by Angelo Dell'Aera and is available at
# https://github.com/buffer/thug
#
# To run this image after installing Docker, you have a number of options:
#
# sudo docker run --rm  -v <local_folder>:/tmp/thug/logs remnux/thug <variables>
#
#   This will allow you to run thug as a 'headless' application without
#   having to enter the docker. Variables can be passed on the command-line
#   (such as -F to enable file logging). Logs are stored in /tmp/thug/logs
#   by default. Your <local_folder> should be made world-accessible to ensure
#   no permissions issues: e.g. "chmod a+xwr ~/logs"
# 
# sudo docker run --rm -it --entrypoint "/bin/bash" remnux/thug
#
#   This will enter you into the docker where you can run "thug" with 
#   the desired parameters (such as -F to enable file logging).
#
# sudo docker run --rm -it -v <local_folder>:/tmp/thug/logs --entrypoint "/bin/bash" remnux/thug
#
#   This is essentially a combination of both of the above, allowing you entry into 
#   the docker, and storage of log files in your host environment.
#
# To support distributed operations and MongoDB output, install the following
# packages into the image using "apt-get mongodb mongodb-dev python-pymongo
# rabbitmq-server python-pika"
#
# This file was originally based on ideas from Spenser Reinhardt's Dockerfile
# (https://registry.hub.docker.com/u/sreinhardt/honeynet/dockerfile),
# on instructions outlined by M. Fields (@shakey_1), 
# on the installation script created by Payload Security
# (https://github.com/PayloadSecurity/VxCommunity/blob/master/bash/thuginstallation.sh),
# and the official Dockerfile by Angelo Dell'Aera at https://github.com/buffer/thug/blob/master/docker/Dockerfile

FROM ubuntu:22.10
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="17 Dec 2022"
LABEL updated_by="lennyzeltser"

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    sudo \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    python-is-python3 \
    libboost-dev \
    libboost-iostreams-dev \
    libboost-python-dev \
    libboost-system-dev \
    python3-pip \
    libxml2-dev \
    libxslt-dev \
    tesseract-ocr \
    git \
    wget \
    unzip \
    libtool \
    graphviz-dev \
    automake \
    libffi-dev \
    graphviz \
    libfuzzy-dev \
    libfuzzy2 \
    libjpeg-dev \
    libffi-dev \
    pkg-config \
    clang \
    autoconf && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools pytesseract pygraphviz
WORKDIR /tmp
RUN wget https://github.com/cloudflare/stpyv8/releases/download/v10.8.168.22/stpyv8-ubuntu-22.04-python-3.10.zip && \
    unzip stpyv8-ubuntu-22.04-python-3.10.zip && \
    pip3 install stpyv8-ubuntu-22.04-3.10/stpyv8-10.8.168.22-cp310-cp310-linux_x86_64.whl && \
    mkdir -p /usr/share/stpyv8 && \
    mv stpyv8-ubuntu-22.04-3.10/icudtl.dat /usr/share/stpyv8 && \
    rm -rf stpyv8-ubuntu-22.04*

WORKDIR /usr/local/src
RUN git clone --depth 1 https://github.com/buffer/libemu.git && \
    cd libemu && \
    autoreconf -v -i && \
    ./configure && \
    make install && \
    cd .. && \
    rm -rf libemu && \
    ldconfig

RUN python3 -m pip install thug && \
    git clone --depth 1 https://github.com/buffer/thug.git && \
    mkdir /etc/thug && \
    cp -R thug/conf/* /etc/thug && \
    rm -rf thug

RUN groupadd -r thug && \
    useradd -m -d /home/thug -g thug -s /usr/sbin/nologin -c "Thug User" thug && \
    mkdir -p /tmp/thug/logs && \
    chown -R thug:thug /home/thug /tmp/thug/logs && \
    usermod -a -G sudo thug &&  echo 'thug:thug' | chpasswd

USER thug
ENV HOME /home/thug
ENV USER thug
WORKDIR /home/thug
VOLUME ["/tmp/thug/logs"]
ENTRYPOINT ["thug"]
