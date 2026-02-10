# Name: PyLingual
# Website: https://github.com/syssec-utd/PyLingual
# Description: Decompile Python 3.9+ bytecode to source code using ML
#   transformer models. Complements pycdc and uncompyle6 for newer Python
#   versions where traditional decompilers have limited coverage.
# Category: Statically Analyze Code: Python
# Author: UT Dallas Systems Security (syssec-utd)
# License: GPL-3.0: https://github.com/syssec-utd/PyLingual/blob/main/LICENSE
# Notes: pylingual
#
# To run PyLingual within this Docker container, create a directory where
# you'll store your .pyc files, e.g. ~/workdir. Then, use a command like
# this to launch the container and have your directory mapped as
# /home/nonroot/workdir inside the container:
#
#   docker run --rm -it -v ~/workdir:/home/nonroot/workdir remnux/pylingual
#
# PyLingual downloads ML models from Hugging Face on first use (~1-2 GB per
# Python version). To persist the model cache across container runs:
#
#   docker run --rm -it \
#     -v ~/workdir:/home/nonroot/workdir \
#     -v ~/pylingual-models:/home/nonroot/.cache/huggingface \
#     remnux/pylingual
#
# Then run "pylingual" inside the container. For example:
#   pylingual --version 3.12 input.pyc
#
# The pylingual Docker image is hosted in the REMnux Docker Hub repository.
#
# For documentation on PyLingual, see:
# https://github.com/syssec-utd/PyLingual

FROM python:3.12-slim-bookworm
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="10 Feb 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

USER root

# Install deps, clone PyLingual, build, then remove build-only packages
# in a single layer to avoid shipping dead weight from intermediate layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    ca-certificates && \
    pip3 install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    git clone --depth 1 https://github.com/syssec-utd/PyLingual.git /tmp/pylingual && \
    cd /tmp/pylingual && \
    pip3 install --no-cache-dir . && \
    rm -rf /tmp/pylingual && \
    apt-get purge -y git && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
    useradd -m -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
    mkdir -p /home/nonroot/workdir && \
    chown -R nonroot:nonroot /home/nonroot

USER nonroot
ENV HOME=/home/nonroot
ENV USER=nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
CMD ["/bin/bash"]
