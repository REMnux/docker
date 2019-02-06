FROM ubuntu:18.04
MAINTAINER @axpatito

USER root
RUN apt-get update -yqq && apt-get install -yqq --no-install-recommends \
  git \
  gcc \
  python3-dev \
  python3-pip \
  libssl-dev \
  swig \
  libffi-dev \
  ssdeep \
  libfuzzy-dev \
  unrar \
  p7zip-full \
  exiftool \
  clamav-daemon \
  tor \
  libdpkg-perl \
  bsdmainutils

RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot
RUN git clone https://github.com/viper-framework/viper && \
  cd viper && \
  rm viper/modules/clamav.py && \
  git submodule init && \
  git submodule update && \
  mkdir /home/nonroot/workdir

USER root
WORKDIR /home/nonroot/viper
RUN pip3 install setuptools wheel --upgrade
RUN pip3 install .
WORKDIR /tmp
RUN apt-get install -yqq curl automake libtool make gcc libssl-dev libjansson-dev libmagic-dev
RUN curl -SL "https://github.com/VirusTotal/yara/archive/v3.8.1.tar.gz" | tar -xzC . && \
  cd yara-3.8.1 && \
  ./bootstrap.sh && \
  ./configure --enable-cuckoo --enable-magic --enable-dotnet && \
  make && \
  make install && \
  ldconfig && \
  pip3 install yara-python
RUN touch /var/log/viper.log && \
  chown nonroot /var/log/viper.log && \
  chgrp nonroot /var/log/viper.log && \
  mkdir -p /etc/viper && \
  chown nonroot /etc/viper && \
  chgrp nonroot /etc/viper

USER nonroot
EXPOSE 8080
WORKDIR /home/nonroot/viper
RUN cp viper.conf.sample /etc/viper/viper.conf && \
  sed -i 's/storage_path.*$/storage_path=\/home\/nonroot\/workdir/' /etc/viper/viper.conf && \
  sed -i 's/log_file.*$/log_file=\/var\/log\/viper.log/' /etc/viper/viper.conf && \
  sed -i 's/host = .*$/host = 0.0.0.0/' /etc/viper/viper.conf && \
  sed -i 's/#admin_username.*$/admin_username=admin/' /etc/viper/viper.conf && \
  sed -i 's/#admin_password.*$/admin_password=admin/' /etc/viper/viper.conf
CMD viper-web
