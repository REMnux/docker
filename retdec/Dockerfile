# Name: RetDec
# Website: https://github.com/avast/retdec
# Description: Retargetable machine-code decompiler based on LLVM.
# Category: Statically Reverse-Engineer Code: General
# Author: Avast Software (https://www.avast.com)
# License: MIT License: https://github.com/avast/retdec/blob/master/LICENSE
# Notes: retdec-decompiler, retdec-fileinfo, retdec-unpacker, etc.
#
# To run this image after installing Docker, use the command below, replacing
# "~/workdir" with the path to your working directory on the underlying host.
# Before running the docker, create ~/workdir on your host.
#
# docker run --rm -it -v ~/workdir:/home/retdec/workdir remnux/retdec
#
# Then run RetDec commands (starting with "retdec-") inside the container.

FROM ubuntu:24.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="9 Feb 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8
ARG RETDEC_VERSION=v5.0
ARG UPX_VERSION=5.1.0

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    sudo \
    wget \
    xz-utils \
    python3 \
    graphviz && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O /tmp/retdec.tar.xz \
    https://github.com/avast/retdec/releases/download/${RETDEC_VERSION}/RetDec-${RETDEC_VERSION}-Linux-Release.tar.xz && \
    mkdir -p /tmp/retdec && \
    tar xf /tmp/retdec.tar.xz -C /tmp/retdec && \
    cp -a /tmp/retdec/bin /tmp/retdec/lib /tmp/retdec/share /usr/local/ && \
    rm -rf /tmp/retdec* && \
    wget -q -O /tmp/upx.tar.xz \
    https://github.com/upx/upx/releases/download/v${UPX_VERSION}/upx-${UPX_VERSION}-amd64_linux.tar.xz && \
    tar xf /tmp/upx.tar.xz -C /tmp && \
    mv /tmp/upx-${UPX_VERSION}-amd64_linux/upx /usr/local/bin/ && \
    rm -rf /tmp/upx*

RUN groupadd -r retdec && \
    useradd -m -d /home/retdec -g retdec -s /usr/sbin/nologin -c "RetDec User" retdec && \
    mkdir -p /home/retdec/workdir && \
    chown -R retdec:retdec /home/retdec && \
    usermod -a -G sudo retdec && echo 'retdec:retdec' | chpasswd && \
    echo "retdec ALL=(ALL) NOPASSWD: ALL" >/etc/sudoers.d/retdec

USER retdec
ENV HOME=/home/retdec
ENV USER=retdec
WORKDIR /home/retdec/workdir
VOLUME ["/home/retdec/workdir"]
CMD ["/bin/bash"]
