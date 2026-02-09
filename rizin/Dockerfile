# Name: Rizin
# Website: https://rizin.re
# Description: Examine binary files, including disassembling and debugging.
# Category: Dynamically Reverse-Engineer Code: General
# Author: https://github.com/rizinorg/rizin/blob/master/AUTHORS.md
# License: GNU Lesser General Public License (LGPL) v3: https://github.com/rizinorg/rizin/blob/master/COPYING
# Notes: rizin, rz-asm, rz-bin, rz-hash, rz-find, rz-agent, etc.
#
# To run this image after installing Docker, use the command below, replacing
# "~/workdir" with the path to your working directory on the underlying host.
# Before running the docker, create ~/workdir on your host.
#
# docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/rizin
#
# Then run "rizin" or other Rizin commands (starting with "rz-") inside the container.

FROM ubuntu:24.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="9 Feb 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8
ARG RZVER=v0.8.2

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    sudo \
    wget \
    xz-utils \
    git \
    gcc \
    g++ \
    make \
    pkg-config \
    libc-dev-bin \
    libc6-dev \
    linux-libc-dev \
    meson \
    ninja-build && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O /tmp/rizin-src.tar.xz \
    https://github.com/rizinorg/rizin/releases/download/${RZVER}/rizin-src-${RZVER}.tar.xz && \
    cd /tmp && \
    tar xf rizin-src.tar.xz && \
    cd rizin-${RZVER} && \
    meson setup --prefix=/usr build && \
    meson compile -C build && \
    meson install -C build && \
    echo "/usr/lib64" > /etc/ld.so.conf.d/rizin.conf && \
    cd / && \
    rm -rf /tmp/rizin-* /tmp/rizin-src.tar.xz && \
    apt-get remove --purge -y \
    gcc \
    g++ \
    make \
    pkg-config \
    libc-dev-bin \
    libc6-dev \
    linux-libc-dev \
    meson \
    ninja-build && \
    apt-get autoremove --purge -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    ldconfig

RUN groupadd -r nonroot && \
    useradd -m -d /home/nonroot -g nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
    mkdir -p /home/nonroot/workdir && \
    chown -R nonroot:nonroot /home/nonroot && \
    usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd && \
    echo "nonroot ALL=(ALL) NOPASSWD: ALL" >/etc/sudoers.d/nonroot

USER nonroot
RUN (rz-pm init && rz-pm update) 2>/dev/null || true

ENV HOME=/home/nonroot
ENV USER=nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
EXPOSE 8080
CMD ["/bin/bash"]
