#
# This Docker image encapsulates the pescanner Python program 
# from the excellent Malware Analyst Cookbook, its requirements, and helpful data files as well as clamav.
#
# To run this image after building or importing it use a command like this, replacing
# "~/workdir" with the path to your working directory on the underlying host:
#
# sudo docker run -it -v ~/docker/mac-pescanner:/home/nonroot/workdir mac-pescanner python2.7 /opt/pescanner.py *.exe
#
# Before running the application, create ~/workdir on your host and make it
# world-accessible ("chmod a+xwr"). By default it will scan all of the files 
# in the folder shared with it and output the results.
#
# Sources:
#
#    http://code.google.com/p/pefile/
#    http://code.google.com/p/malwarecookbook/source/browse/trunk/3/5/capabilities.yara
#    http://code.google.com/p/reverse-engineering-scripts/downloads/detail?name=UserDB.TXT
#    http://code.google.com/p/malwarecookbook/source/browse/trunk/3/8/pescanner.py
#
# Refs:
#
#    Malware Analyst Cookbook: http://www.malwarecookbook.com/
#    REMnux Docker docs: https://remnux.org/docs/containers/create-docker-images/

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
  curl -SL http://code.google.com/p/malwarecookbook/source/browse/trunk/3/5/capabilities.yara > /usr/local/etc/capabilities.yara && \
  curl -SL https://code.google.com/p/reverse-engineering-scripts/downloads/detail?name=UserDB.TXT > /usr/local/etc/UserDB.txt && \
  mkdir /home/nonroot/workdir && \
  chown nonroot:nonroot /home/nonroot/workdir

USER nonroot
WORKDIR /home/nonroot/workdir
CMD ["/usr/bin/python2.7 /opt/pescanner.py /home/nonroot/workdir/*"]
