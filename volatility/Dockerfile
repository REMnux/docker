#
# This Docker image encapsulates the Volatility Framework (version 2.5) by The 
# Volatility Foundation from http://www.volatilityfoundation.org/#!releases/component_71401
#
# To run this image after installing Docker, use the following command:
# sudo docker run --rm -it -v ~/memdumps:/home/nonroot/memdumps remnux/volatility bash
#
# Before running Volatility, create the ~/memdumps directory and make it world-accessible
# (“chmod a+xwr").

FROM ubuntu:14.04
MAINTAINER Zod (@wzod)

# Install packages from apt repository
USER root
RUN apt-get -qq update && apt-get install -y \
  automake \
  build-essential \
  git \
  ipython \
  libbz2-dev \
  libc6-dev \
  libfreetype6-dev \
  libgdbm-dev \
  libjansson-dev \
  libjpeg8-dev \
  libmagic-dev \
  libreadline-gplv2-dev \
  libtool \
  python2.7 \
  python-dev \
  python-pillow \
  python-pip \
  tar \
  unzip \
  wget \
  zlib1g \
  zlib1g-dev && \
  
# Ensure we're using Python 2.7
ln -fs /usr/bin/python2.7 /usr/bin/python
  
# Install additional dependencies
RUN pip install distorm3 \
  openpyxl \
  pycrypto \
  pytz

# Retrieve remaining dependencies
RUN cd /tmp && \
  wget -O yara-v3.4.0.tar.gz "https://github.com/plusvic/yara/archive/v3.4.0.tar.gz" && \
  wget -O volatility-2.5.tar.gz "https://github.com/volatilityfoundation/volatility/archive/2.5.tar.gz" && \

# Verify hashes
  echo -e "b28ad483d4c0baf4b0b6a9162fcb497f6a822294be8b88621f678c15ed433d3d  volatility-2.5.tar.gz\\n528571ff721364229f34f6d1ff0eedc3cd5a2a75bb94727dc6578c6efe3d618b  yara-v3.4.0.tar.gz" > sha256sum.out && \
  sha256sum -c sha256sum.out && \

# If hashes OK, install Yara and prepare Volatility setup
  tar vxzf volatility-2.5.tar.gz && \
  tar vxzf yara-v3.4.0.tar.gz && \
  cd yara-3.4.0 && \
  ./bootstrap.sh && \
  ./configure && \
  make && \
  make install && \

  cd yara-python/ && \
  python setup.py build && \
  python setup.py install

# Add nonroot user and setup environment
RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  mv -vf /tmp/volatility-2.5 /home/nonroot && \

# Setup Volatility
  cd /home/nonroot/volatility-2.5 && \
  chmod +x vol.py && \
  ln -fs /home/nonroot/volatility-2.5/vol.py /usr/local/bin/ && \
  chown -R nonroot:nonroot /home/nonroot

# Clean up
RUN apt-get remove -y --purge automake build-essential libtool && \
  apt-get autoremove -y --purge && \
  apt-get clean -y && \
  rm -rf /var/lib/apt/lists/*

USER nonroot
ENV HOME /home/nonroot
ENV USER nonroot
WORKDIR /home/nonroot/volatility-2.5
