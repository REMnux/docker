# Name: de4js
# Website: https://lelinhtinh.github.io/de4js/
# Description: Web-based javascript deobfuscator and unpacker
# Category: Dynamically Reverse-Engineer Code: Scripts
# Author: Thanh Than Thien (lelinhtinh)
# License: MIT License (https://github.com/lelinhtinh/de4js/blob/master/LICENSE)
# Notes: 
#
# This Dockerfile is built for use with ruby installed in Alpine Linux 2.7
# base on the original instructions documented in the official Dockerfile found here:
# https://github.com/lelinhtinh/de4js/blob/master/Dockerfile
#
# To run this image after installing Docker, you can use the following command:
# sudo docker run -d --rm -p 4000:4000 -p 35729:35729 --name de4js remnux/de4js
# Then browse to http://localhost:4000/de4js/

FROM ruby:2.7-alpine
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="5 Oct 2020"

RUN apk add --no-cache build-base gcc bash cmake git
WORKDIR /srv/jekyll
RUN git clone https://github.com/lelinhtinh/de4js

WORKDIR /srv/jekyll/de4js
RUN gem install bundler
RUN bundle install --gemfile /srv/jekyll/de4js/Gemfile
CMD ["bundle","exec","jekyll","serve","--force_polling","--host","0.0.0.0","--port","4000","--config","_config.yml,_config_development.yml","--livereload"]
