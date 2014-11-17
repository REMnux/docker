#
# This Docker image encapsulates the JSDetox malware analysis tool by @sven_t
# from http://www.relentless-coding.com/projects/jsdetox
#
# To run this image after installing Docker, use the following command:
# sudo docker run –rm -p 3000:3000 lennyzeltser/jsdetox
# Then, connect to http://localhost:3000 using your web browser.
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  git \
  ruby \
  ruby-dev \
  bundler \
  build-essential
RUN groupadd -r nonroot -g 433 && \
  useradd -u 431 -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot
RUN git clone https://github.com/svent/jsdetox.git

USER root
WORKDIR /home/nonroot/jsdetox
RUN bundle install

EXPOSE 3000

USER nonroot
WORKDIR /home/nonroot/jsdetox
CMD ./jsdetox -l $HOSTNAME
