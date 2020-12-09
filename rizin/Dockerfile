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

ARG with_arm32_as
ARG with_arm64_as
ARG with_ppc_as

ENV RZ_VERSION ${RZ_VERSION}

RUN echo -e "Building versions:\n\
  RZ_VERSION=$RZ_VERSION"

# Build rizin in a volume to minimize space used by build
VOLUME ["/mnt"]

USER root
# Install all build dependencies
# Install bindings
# Build and install rizin on master branch
# Remove all build dependencies
# Cleanup
RUN DEBIAN_FRONTEND=noninteractive dpkg --add-architecture i386 && \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
  curl \
  wget \
  gcc \
  git \
  bison \
  pkg-config \
  make \
  glib-2.0 \
  libc6:i386 \
  libncurses5:i386 \
  libstdc++6:i386 \
  gnupg2 \
  python3-pip \
  ${with_arm64_as:+binutils-aarch64-linux-gnu} \
  ${with_arm32_as:+binutils-arm-linux-gnueabi} \
  ${with_ppc_as:+binutils-powerpc64le-linux-gnu} && \
  pip3 install 'git+https://github.com/rizinorg/rz-pipe#egg=rzpipe&subdirectory=python' && \
  cd /mnt && \
  git clone -b "$RZ_VERSION" -q --depth 1 --recurse-submodules https://github.com/rizinorg/rizin.git && \
  cd rizin && \
  ./configure && \
  make && \
  make install && \
  apt-get install -y xz-utils && \
  apt-get remove --purge -y \
  bison \
  python3-pip \
  glib-2.0 && \
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
USER nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENV HOME /home/nonroot

# Setup rz-pm
RUN rz-pm init && \
  rz-pm update && \
  chown -R nonroot:nonroot /home/nonroot/.config

EXPOSE 8080
CMD ["/bin/bash"]