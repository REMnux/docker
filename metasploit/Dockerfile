#
# This Docker image file encapsulates Metasploit Framework, which is distributed
# from https://github.com/rapid7/metasploit-framework
#
# To run this image after installing Docker, use a command like this:
#
# sudo docker run --rm -it -p 443:443 -v ~/.msf4:/root/.msf4 -v /tmp/msf:/tmp/data remnux/metasploit
#
# The -p parameter exposes the ports on which you expect to receive inbound connections from
# reverse shells and such. Once the app starts, run the desired Metasploit command, such as
# "msfconsole" inside its container.
#
# After running the image, you'll have files from your Metasploit session in the ~/.msf4 and
# /tmp/msf directories on your host. The next time you run the app, it will pick up from where
# it left off by reading the files in those locations. If you wish to start from scratch,
# remove those directories ("sudo rm -rf ~/.msf4 /tmp/msf").
#
# In addition to including Metasploit Framework, the image also includes Nmap and tmux.
#

FROM ubuntu:14.04
MAINTAINER Phocean <jc@phocean.net>

WORKDIR /opt
USER root

# Base packages
RUN apt-get update && apt-get -y install \
  git build-essential zlib1g zlib1g-dev \
  libxml2 libxml2-dev libxslt-dev locate curl \
  libreadline6-dev libcurl4-openssl-dev git-core \
  libssl-dev libyaml-dev openssl autoconf libtool \
  ncurses-dev bison curl wget xsel postgresql \
  postgresql-contrib postgresql-client libpq-dev \
  libapr1 libaprutil1 libsvn1 \
  libpcap-dev libsqlite3-dev libgmp3-dev \
  nasm tmux vim nmap \
  && rm -rf /var/lib/apt/lists/*

# startup script and tmux configuration file
RUN curl -sSL https://github.com/REMnux/docker/raw/master/metasploit/scripts/init.sh --output /usr/local/bin/init.sh && \
  chmod a+xr /usr/local/bin/init.sh && \
  curl -sSL https://github.com/REMnux/docker/raw/master/metasploit/conf/tmux.conf --output /root/.tmux.conf

# Get Metasploit
RUN git clone https://github.com/rapid7/metasploit-framework.git msf
WORKDIR msf

# Install PosgreSQL
RUN curl -sSL https://github.com/REMnux/docker/raw/master/metasploit/scripts/db.sql --output /tmp/db.sql
RUN /etc/init.d/postgresql start && su postgres -c "psql -f /tmp/db.sql"
RUN curl -sSL https://github.com/REMnux/docker/raw/master/metasploit/conf/database.yml --output /opt/msf/config/database.yml

# RVM
RUN curl -sSL https://rvm.io/mpapis.asc | gpg --import
RUN curl -L https://get.rvm.io | bash -s stable 
RUN /bin/bash -l -c "rvm requirements"
RUN /bin/bash -l -c "rvm install 2.3.1"
RUN /bin/bash -l -c "rvm use 2.3.1 --default"
RUN /bin/bash -l -c "source /usr/local/rvm/scripts/rvm"
RUN /bin/bash -l -c "gem install bundler --no-ri --no-rdoc"
RUN /bin/bash -l -c "source /usr/local/rvm/scripts/rvm && which bundle"
RUN /bin/bash -l -c "which bundle"

# Get dependencies
RUN /bin/bash -l -c "BUNDLEJOBS=$(expr $(cat /proc/cpuinfo | grep vendor_id | wc -l) - 1)"
RUN /bin/bash -l -c "bundle config --global jobs $BUNDLEJOBS"
RUN /bin/bash -l -c "bundle install"

# Symlink tools to $PATH
RUN for i in `ls /opt/msf/tools/*/*`; do ln -s $i /usr/local/bin/; done
RUN ln -s /opt/msf/msf* /usr/local/bin

# settings and custom scripts folder
VOLUME /root/.msf4/
VOLUME /tmp/data/

# Starting script (DB + updates)
CMD /usr/local/bin/init.sh
