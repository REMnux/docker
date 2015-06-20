#
# This Docker image encapsulates the command-line tool "d8" from
# Google's V8 JavaScript Engine (https://code.google.com/p/v8).
#
# To run this image after installing Docker, use a command like this,
# replacing "~/files" with the path to the location of the files you'd
# like to examine within the container:
#
# sudo docker run --rm -it -v ~/files:/home/nonroot/files remnux/v8 bash
#
# Before running the image, create the  ~/files directory and make it world-accessible ("chmod a+xwr").
#
# Once you've activated the container using the command above, you can run the command-line
# version of V8 by typing the "d8" command (e.g., "d8 -f ~/files/file.js"). To use the pre-defined
# JavaScript object definitions, supply a command like "d8 -f ~/objects.js ~/files/file.js".
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  curl \
  subversion \
  build-essential \
  python-dev \
  libreadline-dev && \
  rm -rf /var/lib/apt/lists/*
RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot
RUN svn checkout http://v8.googlecode.com/svn/trunk/ v8 && \
  cd v8 && \
  sed -i 's/svn checkout --force/svn checkout --non-interactive --trust-server-cert --force/g' Makefile && \
  make builddeps && \
  make native console=readline && \
  mv out/native/d8 .. && \
  cd .. && \
  rm -rf v8

USER root
RUN mv d8 /usr/local/bin && \
  chown root:root /usr/local/bin/d8 && \
  ln -s /usr/local/bin/d8 /usr/local/bin/v8

USER nonroot
RUN curl -SL https://raw.githubusercontent.com/REMnux/distro/v6/objects.js --output objects.js

CMD ["d8"]
