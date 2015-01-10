#
# This Docker image encapsulates the pescanner Python program 
# from the excellent Malware Analyst Cookbook. 
# 
# More info and references are in the README on [GitHub](https://github.com/adricnet/docker)
#
# To run this image after installing Docker, use a command like this, replacing
# "~/workdir" with the path to your working directory on the underlying host:
#
# sudo docker run -it -v ~/workdir:/home/nonroot/workdir adricnet/mac-pescanner /opt/pescanner.py [target file]
#
# Before running the application, create ~/workdir on your host and make it
# world-accessible ("chmod a+xwr").
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  software-properties-common \
  tar \
  curl \
  python-pip \
  python-magic \
  clamav \
  yara \
  python-yara  && \
  rm -rf /var/lib/apt/lists/*

RUN pip install pefile

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

RUN curl -SL https://malwarecookbook.googlecode.com/svn/trunk/3/8/pescanner.py > /opt/pescanner.py && \
  chmod +x /opt/pescanner.py
  curl -SL http://code.google.com/p/malwarecookbook/source/browse/trunk/3/5/capabilities.yara > /usr/local/etc/capabilities.yara && \
  curl -SL https://code.google.com/p/reverse-engineering-scripts/downloads/detail?name=UserDB.TXT > /usr/local/etc/UserDB.txt && \
  mkdir /home/nonroot/workdir && \
  chown nonroot:nonroot /home/nonroot/workdir

USER nonroot
WORKDIR /home/nonroot/workdir
CMD ["/opt/pescanner.py"]
