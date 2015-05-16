#
# This Dockerfile represents a Docker image that encapsulates the Maltrieve tool
# created by Kyle Maxwell (@krmaxwell) for retrieving malware samples.
#
# This Dockerfile is based heavily on the one from Kyle's Maltrieve repository at
# https://github.com/krmaxwell/maltrieve/blob/master/docker/Dockerfile, which is
# maintained by Michael Boman.
#
# To run this image after installing Docker, use a command like this, replacing
# "~/archive" with the path to your working directory on the underlying host.
# This is where the downloaded malware samples will be deposited.
#
# sudo docker run --rm -it -v ~/archive:/archive remnux/maltrieve 
#
# This will launch Maltrieve without any parameters, directing the tool to retrieve
# malware samples and save them to the ~/archive directory.
#
# If you wish to specify command-line parameters to Maltrieve, then launch it like this:
#
# sudo docker run --rm -it -v ~/archive:/archive remnux/maltrieve bash
#
# This will launch the bash shell in the container, at which point you can run the command
# "maltrieve", specifying optional command-line parameters if you wish.
#
# Before running the container, create ~/archive on your host and make it world-accessible
# ("chmod a+xwr").
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  gcc \
  git \
  libpython2.7-stdlib \
  python2.7 \
  python2.7-dev \
  python-pip \
  python-setuptools \
  libffi-dev \
  libssl-dev && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --upgrade pip

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  mkdir /home/nonroot/archive && \
  ln -s /home/nonroot/maltrieve/archive /archive

WORKDIR /home/nonroot/
RUN git clone https://github.com/krmaxwell/maltrieve.git && \
  cd maltrieve && \
  git checkout dev && \
  pip install -e . && \
  pip install requests[security] && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot/maltrieve
CMD ["maltrieve"]
