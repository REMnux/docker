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
    # ── Runtime packages (kept) ──
    sudo \
    python3 \
    python3-venv \
    graphviz \
    tesseract-ocr \
    libfuzzy2 \
    # ── Runtime libraries (explicit install protects from autoremove) ──
    libxml2 \
    libxslt1.1 \
    libjpeg-turbo8 \
    libmagic1t64 \
    libboost-iostreams1.83.0 \
    libboost-python1.83.0 \
    libboost-system1.83.0 \
    # ── Build-only packages (purged at end) ──
    build-essential \
    python3-dev \
    python3-pip \
    libboost-dev \
    libboost-iostreams-dev \
    libboost-python-dev \
    libboost-system-dev \
    libgraphviz-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libfuzzy-dev \
    libjpeg-dev \
    libssl-dev \
    libmagic-dev \
    git \
    wget \
    autoconf \
    automake \
    libtool && \
    # ── Create venv and install Python packages ──
    python3 -m venv /opt/thug && \
    /opt/thug/bin/pip install \
    "pip>=24.1.2" \
    "setuptools>=70.0.0,<82" \
    "wheel>=0.38.4" \
    "importlib-metadata>=8.0.0" && \
    /opt/thug/bin/pip install \
    yara-python \
    pytesseract \
    pycparser \
    six \
    cffi \
    pygraphviz && \
    # ── Install STPyV8 wheel ──
    wget -q -P /tmp https://github.com/cloudflare/stpyv8/releases/download/v12.0.267.14/stpyv8-12.0.267.14-cp312-cp312-manylinux_2_31_x86_64.whl && \
    /opt/thug/bin/pip install /tmp/stpyv8-12.0.267.14-cp312-cp312-manylinux_2_31_x86_64.whl && \
    rm -f /tmp/stpyv8-*.whl && \
    # ── Build libemu from source ──
    git clone --depth 1 https://github.com/buffer/libemu.git /tmp/libemu && \
    cd /tmp/libemu && \
    autoreconf -v -i && \
    ./configure && \
    make install && \
    cd / && \
    rm -rf /tmp/libemu && \
    ldconfig && \
    # ── Install ssdeep (needs build tools + libfuzzy-dev) ──
    /opt/thug/bin/pip install ssdeep==3.4 --no-build-isolation && \
    # ── Install Thug and configure ──
    git clone --depth 1 https://github.com/buffer/thug.git /tmp/thug && \
    /opt/thug/bin/pip install thug && \
    mkdir -p /etc/thug && \
    cp -R /tmp/thug/thug/conf/* /etc/thug && \
    rm -rf /tmp/thug && \
    ln -sf /opt/thug/bin/thug /usr/local/bin/thug && \
    # ── Purge build-only packages ──
    apt-get purge -y \
    build-essential \
    python3-dev \
    python3-pip \
    libboost-dev \
    libboost-iostreams-dev \
    libboost-python-dev \
    libboost-system-dev \
    libgraphviz-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libfuzzy-dev \
    libjpeg-dev \
    libssl-dev \
    libmagic-dev \
    autoconf \
    automake \
    libtool \
    git \
    wget && \
    apt-get autoremove --purge -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

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
