# Name: Binary Refinery
# Website: https://github.com/binref/refinery
# Description: Transform binary data through a collection of standalone
#   command-line tools that comprise the Binary Refinery toolkit, chaining
#   the individual tools as necessary.
# Author: Jesko Huettenhain
# License: 3-Clause BSD License: https://github.com/binref/refinery/blob/master/LICENSE
# Notes:
#
# To run Binary Refinery tools within this Docker container, create a directory
# where you'll store your input files, e.g. ~/workdir. Then, use a command like
# this to launch the container and have your directory mapped as
# /home/nonroot/workdir inside the container:
#
#   docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/binary-refinery
#
# The binary-refinery Docker image is hosted in the REMnux Docker Hub repository.
#
# For documentation on Binary Refinery, including the listing of its tools, see:
# https://binref.github.io and https://github.com/binref/refinery

FROM python:3.12-slim-bookworm
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="9 Feb 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir --upgrade binary-refinery[all] && \
    groupadd -r nonroot && \
    useradd -m -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
    mkdir -p /home/nonroot/workdir && \
    chown -R nonroot:nonroot /home/nonroot

USER nonroot
ENV HOME=/home/nonroot
ENV USER=nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
CMD ["/bin/bash"]
