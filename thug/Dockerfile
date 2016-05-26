#
# This Docker image encapsulates Thug, a low-interaction honeyclient,
# which was created by Angelo Dell'Aera (angelodellaera) and is
# available at https://github.com/buffer/thug.
#
# The file below is based on ideas from Spenser Reinhardt's Dockerfile
# (https://registry.hub.docker.com/u/sreinhardt/honeynet/dockerfile),
# on instructions outlined by M. Fields (@shakey_1) and 
# on the installation script created by Payload Security
# (https://github.com/PayloadSecurity/VxCommunity/blob/master/bash/thuginstallation.sh)
#
# To run this image after installing Docker, use a command like this:
#
# sudo docker run --rm -it remnux/thug bash
#
# then run ./thug.py with the desired parameters (such as -F to enable
# file logging).
#
# To share the "logs" directory between your host and the container,
# create a "logs" directory on your host and make it world-accessible
# (e.g., "chmod a+xwr ~/logs"). Then run the tool like this:
#
# sudo docker run --rm -it -v ~/logs:/home/thug/logs remnux/thug bash
# 
# If you'd like to share an additional directory (e.g., "files"), supply the
# mapping using another -v parameter such as "-v ~/files:/home/thug/files",
# but remember to make the directory on your host world-accessible.
#
# To support distributed operations and MongoDB output, install the folloging
# packages into the image using "apt-get": mongodb, mongodb-dev, python-pymongo,
# rabbitmq-server, python-pika. Also, remove the "sed" command that disables
# logging in the thug\src\Logging\logging.conf file.
#


FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    python-socksipy \
    build-essential \
    python-dev \
    python-setuptools \
    libboost-python-dev \
    libboost-all-dev \
    subversion \
    curl \
    python-pip \
    libxml2-dev \
    libxslt-dev \
    git \
    libtool \
    graphviz-dev \
    automake \
    libffi-dev \
    autoconf && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /home
RUN git clone https://github.com/buffer/libemu.git && \
  cd libemu && \
  autoreconf -v -i && \
  export CFLAGS=-Wno-error && \
  ./configure --prefix=/opt/libemu && \
  make install && \
  ldconfig -n /opt/libemu && \
  touch /etc/ld.so.conf.d/libemu.conf && \
  echo "/opt/libemu/lib/" > /etc/ld.so.conf.d/libemu.conf && \
  ldconfig && \
  cd .. && \
  rm -rf libemu

RUN pip install -q jsbeautifier \
      rarfile \
      beautifulsoup4 \
      pefile \
      six \
      html5lib \
      chardet \
      requests \
      PySocks \
      cssutils \
      zope.interface \
      pyparsing \
      python-magic \
      graphviz \
      lxml \
      pylibemu && \
   pip install -q --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" \
      pygraphviz

RUN curl -sSL "https://github.com/plusvic/yara/archive/v3.4.0.tar.gz" | tar -xzC . && \
  cd yara-3.4.0 && \
  ./bootstrap.sh && \
  ./configure && \
  make && \
  make install && \
  cd yara-python/ && \
  python setup.py build && \
  python setup.py install && \
  cd ../.. && \
  rm -rf yara-3.4.0 && \
  ldconfig

RUN curl -sSL https://github.com/REMnux/docker/raw/master/dependencies/ssdeep-2.13.tar.gz |  tar -xzC .  && \
  cd ssdeep-2.13 && \
  ./configure && \
  make install && \
  cd .. && \
  rm -rf ssdeep-2.13 && \
  BUILD_LIB=1 pip install ssdeep

RUN groupadd -r thug && \
  useradd -r -g thug -d /home/thug -s /sbin/nologin -c "Thug User" thug

WORKDIR /home
RUN git clone https://github.com/buffer/pyv8.git && \
  cd pyv8 && \
  python setup.py build && \
  python setup.py install && \
  cd .. && \
  rm -rf pyv8

RUN git clone https://github.com/buffer/thug.git && \
  chmod a+x thug/src/thug.py && \
  mkdir thug/logs && \
  mkdir thug/files && \
  sed -i 's/\tTrue/\tFalse/g' thug/src/Logging/logging.conf && \
  chown -R thug:thug /home/thug

USER thug
ENV HOME /home/thug
ENV USER thug
WORKDIR /home/thug/src
CMD ["./thug.py"]
