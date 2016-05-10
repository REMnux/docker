#
# This Docker image encapsulates the Radare2 reverse-engineering
# framework available at http://radare.org.
#
# To run this image after installing Docker, use a command like this, replacing
# "~/workdir" with the path to your working directory on the underlying host:
#
# sudo docker run --rm -it -v ~/workdir:/home/nonroot/workdir remnux/radare2 bash
#
# Then run "r2" or other Radare2 commands inside the container.
#
# Before running the application, create ~/workdir on your host and make it
# world-accessible ("chmod a+xwr").
#
# This Dockerfile is based on the instructions documented in the official
# Radare2 Dockerfile file at
# https://github.com/radare/radare2/blob/master/doc/Dockerfile.
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  software-properties-common \
  python-all-dev \
  curl \
  swig \
  flex \
  bison \
  git \
  gcc \
  g++ \
  make \
  pkg-config \
  glib-2.0 \
  python-gobject-dev \
  valgrind \
  gdb && \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

ENV VALA_TAR vala-0.26.1
WORKDIR /opt

RUN curl -SL https://download.gnome.org/sources/vala/0.26/${VALA_TAR}.tar.xz | \
  tar -JxC . && \
  cd ${VALA_TAR}; ./configure --prefix=/usr && \
  make && \
  make install && \
  cd .. && \
  rm -rf ${VALA_TAR} && \
  git clone https://github.com/radare/radare2.git && \
  cd radare2 && \
  ./sys/install.sh && \
  mkdir /home/nonroot/workdir && \
  chown nonroot:nonroot /home/nonroot/workdir

USER nonroot
WORKDIR /home/nonroot/workdir
CMD ["r2"]
