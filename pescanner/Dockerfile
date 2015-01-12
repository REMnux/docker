#
# This Dockerfile represents a Docker image that encapsulates the pescanner tool
# created by Michael Ligh and distributed with the book Malware Analyst Cookbook.
# We're using the version of pescanner that was revised by Glenn P. Edwards Jr.,
# because it also calculates imphash.
#
# This Dockerfile is based on the one contributed to the REMnux collection by
# Adric Net. (http://adric.net/)
#
# To run this image after installing Docker, use a command like this, replacing
# "~/workdir" with the path to your working directory on the underlying host:
#
# sudo docker run --rm -it -v ~/workdir:/home/nonroot/workdir remnux/pescanner bash
#
# This will launch the bash shell in the container, at which point you can run the "pescanner"
# command to scan the desired file.
#
# Before running the container, create ~/workdir on your host and make it world-accessible ("chmod a+xwr").
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
    python-yara \
    subversion \
    python-dev \
    libffi-dev \
    libfuzzy-dev && \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot && \
  mkdir /home/nonroot/workdir && \
  chown nonroot:nonroot /home/nonroot/workdir
  
RUN svn checkout http://libdasm.googlecode.com/svn/trunk/ libdasm && \
  cd libdasm && \
  make && \
  make install && \
  ldconfig && \
  cd pydasm && \
  python setup.py install && \
  cd ../.. && \
  rm -rf libdasm

RUN svn checkout http://pefile.googlecode.com/svn/trunk/ pefile && \
  cd pefile && \
  python setup.py install && \
  cd .. && \
  rm -rf pefile && \
  pip install ssdeep

RUN curl -SL https://raw.githubusercontent.com/hiddenillusion/AnalyzePE/master/pescanner.py > /usr/local/bin/pescanner.py && \
  chmod +x /usr/local/bin/pescanner.py && \
  ln -s /usr/local/bin/pescanner.py /usr/local/bin/pescanner && \
  ln -s /usr/bin/clamscan /usr/bin/clamscanx && \
  curl -SL https://malwarecookbook.googlecode.com/svn/trunk/3/5/capabilities.yara > /usr/local/etc/capabilities.yara && \
  curl -SL https://reverse-engineering-scripts.googlecode.com/files/UserDB.TXT > /usr/local/etc/UserDB.txt && \
  sed -i 's/\/path\/to\/rules.yara/\/usr\/local\/etc\/capabilities.yara/' /usr/local/bin/pescanner.py && \
  sed -i 's/\/path\/to\/userdb.txt/\/usr\/local\/etc\/UserDB.txt/' /usr/local/bin/pescanner.py

RUN freshclam

USER nonroot
WORKDIR /home/nonroot/workdir
CMD ["pescanner"]
