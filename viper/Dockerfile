# Name: Viper
# Website: https://github.com/viper-framework/viper
# Description: Organize and query a collection of malware samples.
# Category: Gather and Analyze Data
# Author: Claudio Guarnieri: https://nex.sx
# License: BSD 3-Clause License: https://github.com/viper-framework/viper/blob/master/LICENSE
# Notes: viper
#
# This Docker image encapsulates the Viper binary analysis and management
# framework by Claudio Guarnieri.
#	
# To run this image after installing Docker, use a command like this to launch the	
# docker, replacing "~/workdir" with the path to the location of the data to analyse:	
#	
# sudo docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/viper	
# To run the 'clamav' plugin, the clamav-daemon must be running. You can enable this by
# running: sudo service clamav-daemon start
# Before running Viper, create the  ~/workdir and make it world-accessible ("chmod a+xwr").	

FROM ubuntu:20.04
LABEL version="3.0"
LABEL description="Viper Framework Docker"
LABEL maintainer="https://github.com/digitalsleuth"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

USER root
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git \
  sudo \
  gcc \
  python3-dev \
  python3-pip \
  libssl-dev \
  libffi-dev \
  unrar-free \
  p7zip-full \
  tor \
  libdpkg-perl \
  libusb-1.0-0 \
  libimage-exiftool-perl \
  swig \
  ssdeep \
  clamav-daemon \
  libfuzzy-dev && \
  rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install setuptools wheel --upgrade && \
  python3 -m pip install viper-framework && \
  freshclam

RUN groupadd -r nonroot && \
  useradd -m -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && mkdir /home/nonroot/.viper && \
  chown -R nonroot:nonroot /home/nonroot && \
  usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd

USER nonroot
WORKDIR /home/nonroot/.viper
RUN git clone https://github.com/viper-framework/viper-modules.git modules
WORKDIR /home/nonroot/.viper/modules
RUN git submodule init && git submodule update && \
  sed -i 's/verify-sigs @ //g' requirements.txt && \
  sed -i 's/PyMISPGalaxies @ //g' requirements.txt

USER root
WORKDIR /home/nonroot/.viper/modules
RUN python3 -m pip install -U -r requirements.txt && python3 -m pip install 'lief>=0.11.0'

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENV USER nonroot
CMD ["/bin/bash"]
