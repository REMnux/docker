#
# This Docker image encapsulates the MASTIFF static analysis framework by The MASTIFF Project
# at KoreLogic from https://github.com/KoreLogicSecurity/mastiff
#
# To run this image after installing Docker, use a command like this, replacing "~/mastiff-workdir"
# with the path to the location of your MASTIFFF directory:
#
# sudo docker run --rm -it -v ~/mastiff-workdir:/home/nonroot/workdir remnux/mastiff
#
# Before running MASTIFF, create the  ~/mastiff-workdir and make it world-accessible ("chmod a+xwr").
#

FROM ubuntu:14.04
MAINTAINER Zod (@wzod)

USER root
RUN apt-get -qq update && apt-get install -y \
  automake \
  build-essential \
  exiftool \
  git \
  libmagic-dev \
  libtool \
  make \
  python2.7 \
  python-dev \
  python-magic \
  python-setuptools \
  python-yapsy \
  wget && \
  ln -fs /usr/bin/python2.7 /usr/bin/python && \
  cd /home && \
  git clone https://github.com/wzod/wzod_mastiff_installer.git && \
  cd wzod_mastiff_installer && \

  groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot && \
  cd /home/nonroot && \
  mv /home/wzod_mastiff_installer . && \
  cd wzod_mastiff_installer && \
  chmod +x wzod_mastiff_installer.sh && \
  ./wzod_mastiff_installer.sh /home/nonroot/ && \
  chown -R nonroot:nonroot /home/nonroot && \
  cp /home/nonroot/mastiff-0.6.0/mastiff.conf /home/nonroot/.mastiff.conf && \
  rm -vrf /home/nonroot/wzod_mastiff_installer && \
  rm -vrf /home/nonroot/mastiff_setup && \


  apt-get remove -y --purge automake build-essential libtool && \
  apt-get autoremove -y --purge && \
  apt-get clean -y && \
  rm -rf /var/lib/apt/lists/*

USER nonroot
ENV HOME /home/nonroot
ENV USER nonroot
WORKDIR /home/nonroot/mastiff-0.6.0
