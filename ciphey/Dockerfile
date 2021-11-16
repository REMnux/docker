# Name: Ciphey 
# Website: https://github.com/Ciphey/Ciphey
# Description: Automatically recognize and decode/decrypt common encoding and encryption techniques.
# Author: Brandon Skerritt: https://twitter.com/brandon_skerrit
# License: MIT License: https://github.com/Ciphey/Ciphey/blob/master/license
# Notes: ciphey
#
# To run Ciphey using this Docker container, create a directory where you'll store
# your input files, e.g. ~/workdir/input.txt. Then, use a command like this to run "ciphey" 
# and have your directory mapped as /home/nonroot/workdir inside the container:
#
#   docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/ciphey -f input.txt 
#
# Or for a text input:
#
#   docker run -it --rm remnux/ciphey "=MXazlHbh5WQgUmchdHbh1EIy9mZgQXarx2bvRFI4VnbpxEIBBiO4VnbNVkU"
#
# The remnux/ciphey image is hosted on its Docker Hub page.

FROM python:3.8.12-slim-buster
LABEL version="1.1"
LABEL description="Ciphey - An Automated Decoding and Decryption Tool"
LABEL maintainer="Lenny Zeltser"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

USER root

RUN pip3 install --upgrade pip && \
  pip3 install --upgrade ciphey && \
  groupadd -r nonroot && \
  useradd -m -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && \
  chown -R nonroot:nonroot /home/nonroot 

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENV USER nonroot
ENTRYPOINT ["/usr/local/bin/ciphey"]
CMD ["--help"]
