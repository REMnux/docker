#
# This Docker image encapsulates Thug, a low-interaction honeyclient,
# which was created by Angelo Dell'Aera (angelodellaera) and is
# available at https://github.com/buffer/thug.
#
# The file below is based on ideas from Spenser Reinhardt's Dockerfile
# (https://registry.hub.docker.com/u/sreinhardt/honeynet/dockerfile)
# and on instructions outlined by M. Fields (@shakey_1).
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
    python2.7 \
    python2.7-dev \
    python-html5lib \
    python-pefile \
    python-lxml \
    python-chardet \
    python-httplib2 \
    python-requests \
    python-cssutils \
    python-zope.interface \
    graphviz \
    graphviz-dev \
    python-pyparsing \
    python-pydot \
    python-magic \
    libboost1.54-dev \
    python-networkx \
    libboost-dev \
    g++ \
    build-essential \
    subversion \
    scons \
    git \
    libboost-python-dev \
    libboost-thread-dev \
    libboost-system-dev \
    python-setuptools \
    python-pip \
    autoconf2.13 \
    libtool \
    libemu-dev \
    systemtap-sdt-dev \
    automake \
    libpcre3 \
    libpcre3-dev \
    curl \
    bison \
    libffi-dev \
    python-socksipy && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" -q \
      pygraphviz && \
    pip install -q jsbeautifier \
      rarfile \
      beautifulsoup4 \
      pefile \
      six

RUN groupadd -r thug && \
  useradd -r -g thug -d /home/thug -s /sbin/nologin -c "Thug User" thug

WORKDIR /home
RUN git clone git://github.com/buffer/thug.git && \
  svn checkout http://pyv8.googlecode.com/svn/trunk/ pyv8 && \
  patch -p0 < thug/patches/PyV8-patch1.diff && \
  cd pyv8 && \
  python setup.py build && \
  python setup.py install && \
  cd .. && \
  rm -rf pyv8 v8 && \
  chmod a+x thug/src/thug.py && \
  mkdir thug/logs && \
  mkdir thug/files && \
  sed -i 's/\tTrue/\tFalse/g' thug/src/Logging/logging.conf

WORKDIR /home
RUN git clone git://git.carnivore.it/libemu.git && \
  cd libemu && \
  autoreconf -v -i && \
  export CFLAGS=-Wno-error && \
  ./configure --prefix=/usr/local/libemu && \
  make install && \
  ldconfig -n /usr/local/libemu && \
  cd .. && \
  rm -rf libemu && \
  
  git clone git://github.com/buffer/pylibemu.git && \
  cd pylibemu && \
  python setup.py build && \
  python setup.py install && \
  cd .. && \
  rm -rf pylibemu && \
  echo /opt/libemu/lib/ >> /etc/ld.so.conf.d/libemu.conf && \
  ldconfig && \
  
  git clone https://github.com/plusvic/yara.git && \
  cd yara && \
  bash build.sh && \
  make install && \
  cd yara-python && \
  python setup.py build && \
  python setup.py install && \
  cd ../.. && \
  rm -rf yara && \
  ldconfig && \

  curl -SL http://sourceforge.net/projects/ssdeep/files/ssdeep-2.12/ssdeep-2.12.tar.gz/download | \
  tar -xzC .  && \
  cd ssdeep-2.12 && \
  ./configure && \
  make install && \
  cd .. && \
  rm -rf ssdeep-2.12 && \
  BUILD_LIB=1 pip install ssdeep && \

  chown -R thug:thug /home/thug

USER thug
ENV HOME /home/thug
ENV USER thug
WORKDIR /home/thug/src
CMD ["./thug.py"]
