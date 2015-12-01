#
# This Docker image encapsulates the Viper binary analysis and management
# framework by Claudio Guarnieri from http://viper.li
#
# To run this image after installing Docker, use a command like this to launch the
# Viper web interface, replacing "~/viper-workdir" with the path to the location of
# your Viper Viper data directory:
#
#  sudo docker run --rm -p 9090:9090 -v ~/viper-workdir:/home/nonroot/workdir remnux/viper
#
# Before running Viper, create the  ~/viper-workdir and make it world-accessible ("chmod a+xwr").
#
# If you want to launch the Viper command-line tool instead of its web interface, run
# Bash in the container like this, then issue the desired ./viper.py command:
#
# sudo docker run --rm -it -v ~/viper-workdir:/home/nonroot/workdir remnux/viper bash
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    python-dev \
    python-pip \
    curl \
    libtool \
    autoconf \
    python-socksipy \
    python-numpy \
    python-scipy \
    bison \
    byacc \
    python-m2crypto \
    python-levenshtein \
    libimage-exiftool-perl && \
  rm -rf /var/lib/apt/lists/*
RUN pip install SQLAlchemy \
  PrettyTable \
  python-magic \
  beautifulsoup \
  fuzzywuzzy \
  scikit-learn
RUN curl -SL http://sourceforge.net/projects/ssdeep/files/ssdeep-2.12/ssdeep-2.12.tar.gz/download | \
  tar -xzC .  && \
  cd ssdeep-2.12 && \
  ./configure && \
  make install && \
  pip install pydeep && \
  cd .. && \
  rm -rf ssdeep-2.12
RUN groupadd -r nonroot && \
  useradd -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot
RUN git clone https://github.com/botherder/viper.git && \
  mv viper/viper.conf.sample viper/viper.conf && \
  sed -i 's/store_path =/store_path =\/home\/nonroot\/workdir/' viper/viper.conf && \
  sed -i 's/data\/yara/\/home\/nonroot\/viper\/data\/yara/g' viper/modules/yarascan.py && \
  rm viper/modules/clamav.py && \
  mkdir /home/nonroot/workdir

USER root
WORKDIR /home/nonroot/viper
RUN chmod a+xr viper.py && \
  pip install -r requirements.txt

RUN curl -SL "https://github.com/plusvic/yara/archive/v3.4.0.tar.gz" | tar -xzC . && \
 cd yara-3.4.0 && \
  ./bootstrap.sh && \
  ./configure && \
  make && \
  make install && \
  cd yara-python/ && \
  python setup.py build && \
  python setup.py install && \
  cd ../.. && \
  rm -rf yara-3.4.0 && \
  ldconfig

RUN git clone git://github.com/smarnach/pyexiftool.git && \
  cd pyexiftool && \
  python setup.py install && \
  cd .. && \
  rm -rf pyexiftool

USER nonroot
EXPOSE 9090
WORKDIR /home/nonroot/viper
CMD ./web.py -H $HOSTNAME
