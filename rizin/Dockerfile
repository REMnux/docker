# Name: Rizin
# Website: https://rizin.re
# Description: Examine binary files, including disassembling and debugging.
# Category: Dynamically Reverse-Engineer Code: General
# Author: https://github.com/rizinorg/rizin/blob/master/AUTHORS.md
# License: GNU Lesser General Public License (LGPL) v3: https://github.com/rizinorg/rizin/blob/master/COPYING
# Notes: rizin, rz-asm, rz-bin, rz-hash, rz-find, rz-agent, etc.
#
# This Dockerfile is based on the official Rizin Dockerfile file from
# the following URL, adjusted to use Ubuntu instead of Debian:
# https://github.com/rizinorg/rizin/blob/dev/Dockerfile
#
# To run this image after installing Docker, use the command below, replacing
# "~/workdir" with the path to your working directory on the underlying host.
# Before running the docker, create ~/workdir on your host.
#
# docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/rizin/workdir remnux/rizin
#
# Then run "rizin" or other Rizin commands (starting with "rz-") inside the container.
#
# Running 'rz-agent -a' will enable the web-based interface on port 8080 by default.
# To access this, add '-p 8080:8080' to the above docker command (before 'remnux/rizin')
# Then browse to your http://YOUR_IP:8080. 

FROM ubuntu:20.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="8 Dec 2020"
LABEL updated_by="Lenny Zeltser"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

# Rizin branch version
ARG RZ_VERSION=dev

# rz-pipe python version
ARG RZ_PIPE_PY_VERSION=master

ARG with_arm32_as
ARG with_arm64_as
ARG with_ppc_as

ENV RZ_PIPE_PY_VERSION ${RZ_PIPE_PY_VERSION}

RUN echo -e "Building versions:\n\
	RZ_PIPE_PY_VERSION=${RZ_PIPE_PY_VERSION}"

USER root

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  curl \
  cmake \
	gcc \
	cpp \
	g++ \
	git \
	make \
	libc-dev-bin libc6-dev linux-libc-dev \
	python3-pip \
	python3-setuptools \
	python3-wheel \
	${with_arm64_as:+binutils-aarch64-linux-gnu} \
	${with_arm32_as:+binutils-arm-linux-gnueabi} \
	${with_ppc_as:+binutils-powerpc64le-linux-gnu} && \
	pip3 install meson ninja && \
	cd /tmp && \
	git clone -b "$RZ_PIPE_PY_VERSION" https://github.com/rizinorg/rz-pipe && \
	pip3 install ./rz-pipe/python && \
  git clone -b "$RZ_VERSION" -q --depth 1 --recurse-submodules https://github.com/rizinorg/rizin.git && \
	cd rizin && \
	meson --prefix=/usr /tmp/build && \
	meson compile -C /tmp/build && \
	meson install -C /tmp/build && \
	rm -rf /tmp/build && \
	pip3 uninstall -y meson ninja && \
	apt-get remove --purge -y \
	cmake \
	cpp \
	g++ \
	python3-pip \
	python3-setuptools \
	python3-wheel && \
  apt-get autoremove --purge -y && \
  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV RZ_ARM64_AS=${with_arm64_as:+aarch64-linux-gnu-as}
ENV RZ_ARM32_AS=${with_arm32_as:+arm-linux-gnueabi-as}
ENV RZ_PPC_AS=${with_ppc_as:+powerpc64le-linux-gnu-as}

# Create non-root user
RUN groupadd -r nonroot && \
  useradd -m -d /home/nonroot -g nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && \
  chown -R nonroot:nonroot /home/nonroot && \
  usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd

# Initilise base user
#USER nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENV HOME /home/nonroot
ENV LD_LIBRARY_PATH=/usr/lib64

# Setup rz-pm
RUN rz-pm init && \
  rz-pm update && \
  chown -R nonroot:nonroot /home/nonroot/.config

EXPOSE 8080
CMD ["/bin/bash"]