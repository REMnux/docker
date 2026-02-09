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
# This Dockerfile mirrors the approach of the REMnux salt state for Thug.

FROM ubuntu:24.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="9 Feb 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    sudo \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    libboost-dev \
    libboost-iostreams-dev \
    libboost-python-dev \
    libboost-system-dev \
    libgraphviz-dev \
    graphviz \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libfuzzy-dev \
    libfuzzy2 \
    libjpeg-dev \
    libssl-dev \
    libmagic-dev \
    tesseract-ocr \
    git \
    wget \
    autoconf \
    automake \
    libtool && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment mirroring salt state /opt/thug virtualenv
RUN python3 -m venv /opt/thug

# Bootstrap pip and core packages per salt state
RUN /opt/thug/bin/pip install \
    "pip>=24.1.2" \
    "setuptools>=70.0.0,<82" \
    "wheel>=0.38.4" \
    "importlib-metadata>=8.0.0"

# Install pre-dependency packages per salt state
RUN /opt/thug/bin/pip install \
    yara-python \
    pytesseract \
    pycparser \
    six \
    cffi \
    pygraphviz

# Install STPyV8 v12.0.267.14 manylinux wheel per salt state
WORKDIR /tmp
RUN wget -q https://github.com/cloudflare/stpyv8/releases/download/v12.0.267.14/stpyv8-12.0.267.14-cp312-cp312-manylinux_2_31_x86_64.whl && \
    /opt/thug/bin/pip install stpyv8-12.0.267.14-cp312-cp312-manylinux_2_31_x86_64.whl && \
    rm -f stpyv8-12.0.267.14-cp312-cp312-manylinux_2_31_x86_64.whl

# Build libemu from source (salt state installs from REMnux apt repo)
WORKDIR /usr/local/src
RUN git clone --depth 1 https://github.com/buffer/libemu.git && \
    cd libemu && \
    autoreconf -v -i && \
    ./configure && \
    make install && \
    cd .. && \
    rm -rf libemu && \
    ldconfig

# Install ssdeep per salt state (requires --no-build-isolation)
RUN /opt/thug/bin/pip install ssdeep==3.4 --no-build-isolation

# Install Thug and configure per salt state
RUN git clone --depth 1 https://github.com/buffer/thug.git /usr/local/src/thug && \
    /opt/thug/bin/pip install thug && \
    mkdir -p /etc/thug && \
    cp -R /usr/local/src/thug/thug/conf/* /etc/thug && \
    rm -rf /usr/local/src/thug

# Create symlink per salt state
RUN ln -sf /opt/thug/bin/thug /usr/local/bin/thug

RUN groupadd -r thug && \
    useradd -m -d /home/thug -g thug -s /usr/sbin/nologin -c "Thug User" thug && \
    mkdir -p /tmp/thug/logs && \
    chown -R thug:thug /home/thug /tmp/thug/logs && \
    usermod -a -G sudo thug && echo 'thug:thug' | chpasswd

USER thug
ENV HOME=/home/thug
ENV USER=thug
WORKDIR /home/thug
VOLUME ["/tmp/thug/logs"]
ENTRYPOINT ["thug"]
