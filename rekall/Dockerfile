# This is a rekall docker built on Ubuntu 18.04 LTS
# The rekall software/source can be found either at
# http://www.rekall-forensic.com or
# https://github.com/google/rekall
#
# To use the docker, it is recommended to use the following command
#  sudo docker run --rm -it -v <local_directory>:/home/nonroot/files remnux/rekall /bin/bash
#
# This will load you into the docker as the 'nonroot' user,
# and allow you use run the command 'rekall' with any parameters required.

FROM ubuntu:bionic
LABEL version="1.4"
LABEL description="Rekall docker based on Ubuntu 18.04 LTS"
LABEL maintainer="https://github.com/digitalsleuth"

USER root
RUN apt-get update && apt-get install -y \
  virtualenv \
  nano \
  git \
  python \
  python-pip \
  python-dev \
  libssl-dev \
  automake \
  make \
  gcc \
  flex \
  libtool \
  bison \
  pkg-config \
  ncurses-dev && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools pip wheel readline future==0.16.0 pybindgen pyaff4==0.26.post6 && \
  rm /usr/bin/pip && ln -s /usr/local/bin/pip /usr/bin/pip && \
  pip install fastchunking pyopenssl && \
  pip install -q distorm3 && \
  git clone https://github.com/VirusTotal/yara.git && \
  cd yara && \
  bash bootstrap.sh && \
  bash configure && \
  make && \
  make install && \
  make check && \
  echo "/usr/local/lib" >> /etc/ld.so.conf && \
  ldconfig && \
  cd .. && \
  rm -rf yara && \
  pip install rekall-agent rekall && \
  apt-get autoremove -y --purge && \
  apt-get clean -y


RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot
ENV USER nonroot
