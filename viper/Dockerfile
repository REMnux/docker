#
# This Docker image encapsulates the Viper binary analysis and management
# framework by Claudio Guarnieri from http://viper.li
#
# To run this image after installing Docker, use a command like this, replacing "~/viper-workdir"
# with the path to the location of your Viper Viper data directory:
#
# sudo docker run --rm -it -v ~/viper-workdir:/home/nonroot/workdir lennyzeltser/viper
#
# Before running Viper, create the  ~/viper-workdir and make it world-accessible ("chmod a+xwr").
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
  python-socksipy && \
  rm -rf /var/lib/apt/lists/*
RUN pip install SQLAlchemy \
  PrettyTable \
  python-magic
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
  sed -i 's/~\/.viperhistory/\/home\/nonroot\/workdir\/viperhistory/' /home/nonroot/viper/viper/core/ui/console.py && \
  mkdir /home/nonroot/workdir

USER root
WORKDIR /home/nonroot/viper
RUN chmod a+xr viper.py &&\
  pip install -r requirements.txt 

USER nonroot
WORKDIR /home/nonroot/workdir
CMD ["../viper/viper.py"]
