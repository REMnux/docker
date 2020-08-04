# Name: rekall 
# Website: https://github.com/google/rekall
# Description: Memory analysis framework Category: Examine memory snapshots
# Author: https://github.com/google/rekall/blob/master/AUTHORS.md
# License: https://github.com/google/rekall/blob/master/LICENSE.txt
# Notes: rekall, rekal
#
# This is a rekall docker built on Ubuntu 18.04 LTS
# The rekall software/source can be found either at
# http://www.rekall-forensic.com or
# https://github.com/google/rekall
#
# To use the docker, it is recommended to use the following command
#  sudo docker run --rm -it -v <local_directory>:/home/nonroot/files remnux/rekall
#
# This will load you into the docker as the 'nonroot' user,
# and allow you use run the command 'rekall' with any parameters required.

FROM ubuntu:18.04
LABEL version="2.0"
LABEL description="Rekall docker based on Ubuntu 18.04 LTS"
LABEL maintainer="https://github.com/digitalsleuth"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

USER root
RUN apt-get update && apt-get install -y \
  sudo \
  python3 \
  python3-pip \
  python3-dev \
  libssl-dev \
  software-properties-common \
  libncurses5-dev && \
  add-apt-repository ppa:remnux/stable -y && apt-get update && apt-get install yara -y && \
  rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade setuptools pip wheel readline future==0.16.0 pybindgen pyaff4==0.26.post6 capstone && \
  python3 -m pip install fastchunking pyopenssl && \
  python3 -m pip install -q distorm3 && \
  python3 -m pip install rekall-agent rekall && \
  apt-get autoremove -y --purge && \
  apt-get clean -y

RUN groupadd -r nonroot && \
  useradd -m -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/files && \
  chown -R nonroot:nonroot /home/nonroot && \
  usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot/files
VOLUME ["/home/nonroot/files"]
ENV USER nonroot
CMD ["/bin/bash"]
