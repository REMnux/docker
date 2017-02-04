#
# This Docker image encapsulates the Collaborative Research Into Threats (CRITs)
# malware and threat repository by The MITRE Corporation from https://crits.github.io/
#
# To run this image after installing Docker, use a command like this, replacing “~/crits-data"
# with the path to the location for storing CRITs data, indefinitely:
#
# sudo docker run --rm -it -v ~/crits-data:/home/nonroot/workdir -p 8443:8443 remnux/crits 
#
# Before running CRITs, create the ~/crits-data directory and make it world-accessible
# (“chmod a+xwr").
#

FROM ubuntu:16.04
MAINTAINER Zod (@wzod)

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C

USER root
RUN apt-get -qq update && \
  apt-get install -y software-properties-common && \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 && \
  echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/mongodb.list && \
  apt-add-repository -y universe && \
  apt-get -qq update && apt-get install -y --fix-missing \
  apache2 \
  build-essential \
  curl \
  git \
  libevent-dev \
  libz-dev \
  libjpeg-dev \
  libfuzzy-dev \
  libldap2-dev \
  libpcap-dev \
  libpcre3-dev \
  libsasl2-dev \
  libssl-dev \
  libtool \
  libxml2-dev \
  libxslt1-dev \
  libyaml-dev \
  mongodb-org \
  numactl \
  p7zip-full \
  python-dev \
  python-pip \
  ssdeep \
  swig \
  supervisor \
  upx \
  vim \
  wget \
  zip \
  libapache2-mod-wsgi && \
  cp /etc/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
  ldconfig

# Setup supervisord to manage apache and mongod
RUN sed -i 's/^\[supervisord\]$/&\nnodaemon\=true\nlogfile\=\/data\/log\/supervisord\.log\npidfile\=\/data\/run\/supervisord\.pid\n\n\[program\:apache2\]\ncommand\=\/bin\/bash\ \-c\ \"source \/etc\/apache2\/envvars\ \&\&\ exec\ \/usr\/sbin\/apache2\ \-DFOREGROUND\"\nuser\=nonroot\nstdout\_logfile\=\/data\/log\/supervisor\/\%\(program\_name\)s\.log\nstderr\_logfile\=\/data\/log\/supervisor\/\%\(program\_name\)s\.log\nautostart\=true\nautorestart\=true\n\n\[program\:mongod\]\ncommand\=\/usr\/bin\/mongod\nstdout\_logfile\=\/data\/log\/supervisor\/\%\(program\_name\)s\.log\nstderr\_logfile\=\/data\/log\/supervisor\/\%\(program\_name\)s\.log\nautostart\=true\nautorestart\=true\n/' /etc/supervisor/conf.d/supervisord.conf

# Create nonroot account
RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -m -s /sbin/nologin -c "Nonroot User" nonroot

# Setup CRITs
RUN bash -c 'mkdir -pv /data/{db,lock/apache2,log/apache2,log/supervisor,run/apache2,ssl/certs,ssl/private}' && \
  cd /data/ && \
  git clone https://github.com/crits/crits.git && \
  cd crits/ && \
  pip install -r requirements.txt

# For better perfomance, include the following modifications from the host (i.e. outside of Docker container).
#  echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse && \
#  echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle && \
#  sed -i '$ i\echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse\necho 1 > /proc/sys/net/ipv4/tcp_tw_recycle\n' /etc/rc.local && \

# Setup environment
RUN cd /data/crits/ && \
  touch /data/crits/logs/crits.log && \
  touch /data/log/startup.log && \
  ln -f -s /data/crits/logs/crits.log /data/log/crits.log && \
  chgrp -R nonroot logs && \
  chmod 664 /data/crits/logs/crits.log && \
  sed -i 's/^nonroot.*$/&www\-data/' /etc/group && \

  cp crits/config/database_example.py crits/config/database.py && \
  SC=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)' | fold -w 50 | head -n 1) && \
  SE=$(echo ${SC} | sed -e 's/\\/\\\\/g' | sed -e 's/\//\\\//g' | sed -e 's/&/\\\&/g') && \
  sed -i -e "s/^\(SECRET_KEY = \).*$/\1\'${SE}\'/1" crits/config/database.py

# Setup Apache web server
RUN /etc/init.d/apache2 stop && \
  rm -rf /etc/apache2/sites-available/* && \
  cp /data/crits/extras/*.conf /etc/apache2 && \
  cp -r /data/crits/extras/sites-available /etc/apache2 && \
  rm /etc/apache2/sites-enabled/* && \
  ln -f -s /etc/apache2/sites-available/default-ssl /etc/apache2/sites-enabled/default-ssl && \
  mkdir -pv /etc/apache2/conf.d/i && \
  usermod -a -G nonroot www-data

# Setup self-signed cert and perform initial setup
RUN cd /tmp && \
  openssl req -nodes -newkey rsa:4096 -keyout new.cert.key -out new.cert.csr -subj "/CN=CRITs/O=REMnux/C=US" && \
  openssl x509 -in new.cert.csr -out new.cert.cert -req -signkey new.cert.key -days 1825 && \
  cp new.cert.cert /data/ssl/certs/crits.crt && \ 
  cp new.cert.key  /data/ssl/private/crits.plain.key && \
  chown -R nonroot /data/ && \
  a2enmod ssl && \

  export "LANG=en_US.UTF-8" && \
  sed -i "/export\ LANG\=C/ s/C/en\_US\.UTF\-8/" /etc/apache2/envvars && \
  sed -i '$ i\\n0 * * * *       root    cd /data/crits/ && /usr/bin/python manage.py mapreduces\n0 * * * *       root    cd /data/crits/ && /usr/bin/python manage.py generate_notifications' /etc/crontab && \
  sed -i 's/^CustomLog \/var/CustomLog\ \/data/' /etc/apache2/apache2.conf && \
  sed -i 's/^ErrorLog\ \/var/ErrorLog\ \/data/' /etc/apache2/apache2.conf && \
  sed -i 's/\/var/\/data/' /etc/apache2/envvars && \
  sed -i 's/www\-data/nonroot/' /etc/apache2/envvars && \
  sed -i 's/\ 443/\ 8443/' /etc/apache2/ports.conf && \
  sed -i 's/\/var/\/data/' /etc/apache2/sites-available/default && \
  sed -i 's/443/8443/' /etc/apache2/sites-available/default-ssl && \
  sed -i 's/\/etc/\/data/' /etc/apache2/sites-available/default-ssl && \ 
  sed -i 's/\/var/\/data/' /etc/apache2/sites-available/default-ssl && \
  sed -i 's/\/var/\/data/' /etc/supervisor/conf.d/supervisord.conf && \
  sed -i -e :a -e '$d;N;2,3ba' -e 'P;D'  /etc/supervisor/conf.d/supervisord.conf && \
  sed -i 's/\/var/\/data/' /etc/supervisor/supervisord.conf && \
  sed -i 's/\$CWD/\/data\/log\//' /etc/supervisor/supervisord.conf && \
  sed -i 's/\$CWD/\/data\/log\//' /etc/supervisor/conf.d/supervisord.conf

RUN ldconfig && \
  apt-get remove -y --purge build-essential libtool && \
  apt-get autoremove -y --purge && \
  apt-get clean -y && \
  rm -rf /tmp/* && \
  rm -rf /var/lib/apt/lists/*

USER nonroot
ENV HOME /home/nonroot
ENV USER nonroot
WORKDIR /data/crits

# Expose ports 8443 and 27017 from the container to the host
EXPOSE 8443 27017

ENTRYPOINT /usr/bin/supervisord --user=nonroot -c /etc/supervisor/conf.d/supervisord.conf & > /data/log/startup.log; sleep 5; rm /data/db/mongod.lock; /usr/bin/mongod --fork --logpath /data/crits/logs/mongodb.log --logappend --nohttpinterface --dbpath /data/db --smallfiles && python /data/crits/manage.py create_default_collections && python /data/crits/manage.py users -a -A -e "nonroot@crits.local" -f "Nonroot" -l "User" -o "REMnux" -u "nonroot" > /dev/null && python /data/crits/manage.py setconfig allowed_hosts "*" && printf "\n" && echo "To access CRITS user interface, go https://localhost:8443 and use the following credentials:" && printf "\n" && echo "Username: nonroot" && echo -n "Password: " && python /data/crits/manage.py users -u nonroot -r 2> /dev/null | grep ^New | awk -F:\  '{print $2}' && printf "\n" && echo "Please change the temporary password upon successful login to the web interface by clicking on 'Nonroot User' near the top left panel and selecting 'Change Password'." && printf "\n" && echo "If changes made to the CRITs application require a restart of the web server, run 'service apache2 stop' and supervisor will automatically restart the web server for you." && printf "\n" && /bin/bash
