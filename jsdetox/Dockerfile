#
# This Docker image encapsulates the JSDetox malware analysis tool by @sven_t
# from http://www.relentless-coding.com/projects/jsdetox
#
# To run this image after installing Docker, use the following command:
# sudo docker run -d --rm --name jsdetox -p 3000:3000 remnux/jsdetox
# Then, connect to http://localhost:3000 using your web browser.
# To stop jsdetox, use: 
# sudo docker stop jsdetox
# 
# Updated for Ubuntu 20.04
# Changes: Update version of therubyracer from 0.9.8 to 0.12.3
#          Update docker to 20.04
#          Install and specify bundler version 1.17.3 for focal

FROM ubuntu:20.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="22 May 2021"

USER root
RUN apt-get update && apt-get install -y \
  git \
  ruby \
  ruby-dev \
  bundler \
  zlib1g-dev \
  build-essential && \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot
RUN git clone https://github.com/svent/jsdetox.git

USER root
RUN gem install bundler -v "1.17.3"
WORKDIR /home/nonroot/jsdetox
RUN sed "s/, '0.9.8'/, '0.12.3'/g" -i Gemfile
RUN bundle _1.17.3_ install

USER nonroot
EXPOSE 3000
WORKDIR /home/nonroot/jsdetox
CMD ./jsdetox -l $HOSTNAME 2>/dev/null
