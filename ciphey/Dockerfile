# Name: Ciphey 
# Website: https://github.com/Ciphey/Ciphey
# Description: Automatically recognize and decode/decrypt common encoding and encryption techniques.
# Author: Brandon Skerritt: https://twitter.com/brandon_skerrit
# License: MIT License: https://github.com/Ciphey/Ciphey/blob/master/license
# Notes: ciphey
#
# To run Ciphey using this Docker container, create a directory where you'll store
# your input and output files. Then, use a command like this to open a shell inside
# the container where you can run "ciphey" and have your directory mapped as
# /home/nonroot/workdir inside the container:
#
# docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/ciphey
#
# The password for the container's user nonroot is nonroot. The remnux/ciphey image is
# hosted on its its Docker Hub page.

FROM ubuntu:18.04
LABEL version="1.0"
LABEL description="Ciphey - An Automated Decoding and Decryption Tool"
LABEL maintainer="Lenny Zeltser"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

USER root

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python3-pip sudo && \
  rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && \
    python3 -m pip install ciphey

RUN groupadd -r nonroot && \
  useradd -m -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && \
  chown -R nonroot:nonroot /home/nonroot && \
  usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENV USER nonroot
CMD ["/bin/bash"]