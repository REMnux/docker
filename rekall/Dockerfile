#
# This Docker image encapsulates the Rekall Memory Forensic Framework,
# which is available at http://www.rekall-forensic.com.
#
# To run this image after installing Docker, use a command like this:
#
# sudo docker run --rm -it -v ~/files:/home/nonroot/files remnux/rekall bash
#
# then run "rekall" in the container with the desired parameters.
#
# Before running the command above, create the "files" directory on your host and 
# make it world-accessible (e.g., "chmod a+xwr ~/files").
#
# To use Rekall's web console, invoke the container with the -p parameter to give
# your host access to the container's TCP port 8000 like this:
# 
# sudo docker run --rm -it -p 8000:8000 -v ~/files:/home/nonroot/files remnux/rekall
#
# Then connect to http://localhost:8000 using a web browser from your host.
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  python-dev \
  python-pip \
  libtool \
  automake \
  bison \
  git && \

  pip install -q distorm3 && \
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

  pip install -q gevent-websocket \
    flask-sockets \
    codegen \
    acora \
    pyelftools \
    pycrypto && \

  pip install rekall && \

  apt-get remove -y --purge git automake libtool byacc && \
  apt-get autoremove -y --purge && \
  apt-get clean -y && \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
ENV HOME /home/nonroot
ENV USER nonroot
WORKDIR /home/nonroot
CMD rekall webconsole --port 8000 --host $HOSTNAME
