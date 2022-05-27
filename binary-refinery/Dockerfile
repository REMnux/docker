# Name: Binary Refinery 
# Website: https://github.com/binref/refinery
# Description: Transform binary data through a collection of standalone command-line tools that comprise the Binary Refinery™ toolkit, chaining the individual tools as necessary.
# Author: Jesko Hüttenhain
# License: 3-Clause BSD License: https://github.com/binref/refinery/blob/master/LICENSE
# Notes: 
#
# To run Binary Refinery™ tools within this Docker container, create a directory where you'll store
# your input files, e.g. ~/workdir. Then, use a command like this to launch the container 
# and have your directory mapped as /home/nonroot/workdir inside the container:
#
#   docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/binary-refinery
#
# The binary-refinery Docker image is hosted in the REMnux Docker Hub repository.
#
# For documentation on Binary Refinery, including the listing of its tools, see:
# https://binref.github.io and https://github.com/binref/refinery

FROM python:3.8.12-slim-buster
LABEL version="1.0"
LABEL description="The Binary Refinery™ is a collection of Python scripts that implement transformations of binary data such as compression and encryption. "
LABEL maintainer="Lenny Zeltser"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

USER root

RUN pip3 install --upgrade pip && \
  pip3 install --upgrade binary-refinery[all] && \
  groupadd -r nonroot && \
  useradd -m -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && \
  chown -R nonroot:nonroot /home/nonroot 

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENV USER nonroot
CMD "/bin/bash"