#
# This Docker image encapsulates the Volatility Framework (version 2.4) by The 
# Volatility Foundation from http://www.volatilityfoundation.org/#!releases/component_71401
#
# To run this image after installing Docker, use the following command:
# sudo docker run --rm -it -v ~/memdumps:/home/nonroot/memdumps remnux/volatility bash
#

FROM ubuntu:14.04
MAINTAINER Zod (@wzod)

USER root
RUN apt-get -qq update && apt-get install -y \
  git \
  python2.7 \
  python-pil \
  wget && \
  ln -fs /usr/bin/python2.7 /usr/bin/python && \
  cd /home && \
  git clone https://github.com/4n6k/4n6k_volatility_installer.git && \
  cd 4n6k_volatility_installer && \

  groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot && \
  cd /home/nonroot && \
  mv /home/4n6k_volatility_installer . && \
  cd 4n6k_volatility_installer && \
  chmod +x 4n6k_volatility_installer.sh && \
  ./4n6k_volatility_installer.sh /home/nonroot/ && \
  cd /home/nonroot/ && \
  wget -O readme https://api.github.com/repos/sans-dfir/sift-files/contents/volatility && grep "download_url" readme | awk '{print $2}' | sed s/,//g | xargs -I% wget % && \
  mv *.py /home/nonroot/volatility-2.4/volatility/plugins/ && \
  rm -vf readme && \
  rm -vf /home/nonroot/volatility-2.4/volatility/plugins/mimikatz.py && \
  rm -vrf /home/nonroot/4n6k_volatility_installer && \
  rm -vrf /home/nonroot/volatility_setup && \

  apt-get remove -y --purge automake build-essential libtool && \
  apt-get autoremove -y --purge && \
  apt-get clean -y && \
  rm -rf /var/lib/apt/lists/*

USER nonroot
ENV HOME /home/nonroot
ENV USER nonroot
WORKDIR /home/nonroot/volatility-2.4
