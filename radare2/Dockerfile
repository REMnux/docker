# Name: radare2
# Website: https://www.radare.org/n/radare2.html
# Description: Examine binary files, including disassembling and debugging.
# Category: Dynamically Reverse-Engineer Code: General
# Author: https://github.com/radareorg/radare2/blob/master/AUTHORS.md
# License: GNU Lesser General Public License (LGPL) v3: https://github.com/radareorg/radare2/blob/master/COPYING
# Notes: r2, rasm2, rabin2, rahash2, rafind2, r2agent
#
# This Dockerfile is modified for use in Ubuntu 18.04, but is based on 
# the instructions documented in the official Radare2 Dockerfile file at
# https://github.com/radareorg/radare2/blob/master/Dockerfile
#
# To run this image after installing Docker, use the command below, replacing
# "~/workdir" with the path to your working directory on the underlying host.
# Before running the docker, create ~/workdir on your host.
#
# docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/radare2
#
# Then run "r2" or other Radare2 commands inside the container.
#
# Running 'r2agent -a' will enable the web-based interface on port 8080 by default.
# To access this, add '-p 8080:8080' to the above docker command (before 'remnux/radare2')
# Then browse to your http://YOUR_IP:8080. 

FROM ubuntu:18.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="4 Aug 2020"
LABEL updated_by="digitalsleuth"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

USER root
RUN apt-get update && apt-get install -y \
  sudo \
  ccache \
  wget \
  build-essential \
  git && \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -m -d /home/nonroot -g nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && \
  chown -R nonroot:nonroot /home/nonroot && \
  usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd

RUN git clone https://github.com/radare/radare2.git && \
  cd radare2 && \
  ./sys/install.sh && \
  r2pm init && \
  r2pm update

USER nonroot
ENV HOME /home/nonroot
ENV USER nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
EXPOSE 8080
CMD ["/bin/bash"]
