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
# This docker provides the capability for distributed operations and MongoDB output, 
# containing the following packages: mongodb, mongodb-dev, python-pymongo,
# rabbitmq-server, python-pika.
#
# This file was originally based on ideas from Spenser Reinhardt's Dockerfile
# (https://registry.hub.docker.com/u/sreinhardt/honeynet/dockerfile),
# on instructions outlined by M. Fields (@shakey_1) and 
# on the installation script created by Payload Security
# (https://github.com/PayloadSecurity/VxCommunity/blob/master/bash/thuginstallation.sh)

FROM ubuntu:18.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="31 Jul 2020"
LABEL updated_by="digitalsleuth"

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    sudo \
    python \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-wheel \ 
    libboost-dev \
    libboost-python-dev \
    libboost-system-dev \
    python3-pip \
    libxml2-dev \
    libxslt1-dev \
    tesseract-ocr \
    git \
    libtool \
    libgraphviz-dev \
    automake \
    graphviz \
    libfuzzy-dev \
    libfuzzy2 \
    libjpeg-dev \
    libffi-dev \
    pkg-config \
    autoconf  \
    mongodb  \
    mongodb-dev  \
    python-pymongo  \
    rabbitmq-server \
    python-pika && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools pytesseract
WORKDIR /usr/local/src

RUN pip3 install https://github.com/area1/stpyv8/releases/download/v8.4.371.19/stpyv8-8.4.371.19-cp36-cp36m-linux_x86_64.whl

RUN git clone --depth 1 https://github.com/buffer/libemu.git && \
    cd libemu && \
    autoreconf -v -i && \
    ./configure && \
    make install && \
    cd .. && \
    ldconfig

RUN pip3 install thug && \
    git clone --depth 1 https://github.com/buffer/thug.git && \
    mkdir /etc/thug && \
    cd /etc/thug && \
    mkdir rules personalities scripts plugins hooks && \
    cd /usr/local/src/thug && \
    cp -R thug/Classifier/rules/* /etc/thug/rules/ && \
    cp -R thug/DOM/personalities/* /etc/thug/personalities && \
    cp thug/DOM/thug.js /etc/thug/scripts && \
    cp thug/DOM/storage.js /etc/thug/scripts && \
    cp thug/DOM/date.js /etc/thug/scripts && \
    cp thug/DOM/eval.js /etc/thug/scripts && \
    cp thug/DOM/write.js /etc/thug/scripts && \
    cp conf/thug.conf /etc/thug

RUN groupadd -r thug && \
    useradd -m -d /home/thug -g thug -s /sbin/nologin -c "Thug User" thug && \
    mkdir -p /tmp/thug/logs && \
    chown -R thug:thug /home/thug /tmp/thug/logs && \
    usermod -a -G sudo thug &&  echo 'thug:thug' | chpasswd

USER thug
ENV HOME /home/thug
ENV USER thug
WORKDIR /home/thug
VOLUME ["/tmp/thug/logs"]
ENTRYPOINT ["thug"]
