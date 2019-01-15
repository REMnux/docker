#
# This Docker image encapsulates the CyberChef analysis tool by GCHQ
# from https://github.com/gchq/CyberChef
#
# To run this image in the background after installing Docker,
# use the following command:
#
# sudo docker run -d -p 8080:8080 remnux/cyberchef
#
# Then, connect to http://localhost:8080 using your web browser.
# To stop the container, use Docker's "ps" and "stop" commands.
#

FROM node:latest

MAINTAINER Omri Moyal (@GelosSnake)

WORKDIR /install/
USER root

RUN apt-get update && \
  apt-get install -y git && \
  rm -rf /var/lib/apt/lists/* && \
  npm install -g grunt-cli && \ 
  git clone https://github.com/gchq/CyberChef && \
  cd CyberChef && \
  npm install

EXPOSE 8080
WORKDIR /install/CyberChef
ENTRYPOINT ["grunt"]
CMD ["dev"]
