#
# This Docker image encapsulates the CyberChef analysis tool by GCHQ
# from https://github.com/gchq/CyberChef
#
# To run this image in the background after installing Docker,
# use the following command:
#
# sudo docker run -d -p 8080:80 remnux/cyberchef
#
# Then, connect to http://localhost:8080 using your web browser.
# To stop the container, use Docker's "ps" and "stop" commands.
#

FROM ubuntu:16.04

MAINTAINER Matt Georgy (mgeorgy@gmail.com)

LABEL version="1.0"

ENV DEBIAN_FRONTEND noninteractive

################### Version Information ####################
# 1.0:  Initial Release
############################################################

################ Baseline OS INSTALLATION ##################
RUN apt-get update && apt-get -y dist-upgrade && apt-get clean
############################################################

############## Support Package INSTALLATION ################
RUN apt-get install -y curl python-software-properties git build-essential apache2
############################################################

############### Node.js & NPM INSTALLATION #################
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get install -y nodejs
############################################################

################# Grunt NPM INSTALLATION ###################
RUN npm install -g grunt-cli
############################################################

################## Clone CyberChef Repo ####################
RUN git clone https://github.com/gchq/CyberChef.git
WORKDIR /CyberChef
RUN npm install
############################################################

################## Run Grunt Prod Build ####################
RUN grunt prod
############################################################

################## Copy Production Build ###################
RUN cp -r /CyberChef/build/prod/* /var/www/html/
############################################################

EXPOSE 80

ENV APACHE_RUN_USER    www-data
ENV APACHE_RUN_GROUP   www-data
ENV APACHE_PID_FILE    /var/run/apache2.pid
ENV APACHE_RUN_DIR     /var/run/apache2
ENV APACHE_LOCK_DIR    /var/lock/apache2
ENV APACHE_LOG_DIR     /var/log/apache2
ENV LANG               C

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
