#
# This Docker image encapsulates the Viper binary analysis and management
# framework by Claudio Guarnieri from http://viper.li
#
# To run this image after installing Docker, use a command like this, replacing "user/viper" with
# the path to the location of your Viper "binaries" and "projects" directories:
#
# sudo docker run --rm -it \
#    -v /home/user/viper/binaries:/home/nonroot/viper/binaries \
#    -v /home/user/viper/projects:/home/nonroot/viper/projects lennyzeltser/viper
#
# Before running Viper, create the  "binaries" and "projects" directories and make them
# world-accessible ("chmod a+xwr").
#

FROM ubuntu:14.04
MAINTAINER Lenny Zeltser (@lennyzeltser, www.zeltser.com)

USER root
RUN apt-get update && apt-get install -y \
  git \
  gcc \
  python-dev \
  python-pip \
  wget \
  python-socksipy
RUN pip install SQLAlchemy \
  PrettyTable \
  python-magic
RUN wget http://sourceforge.net/projects/ssdeep/files/ssdeep-2.12/ssdeep-2.12.tar.gz/download && \
  tar xvfz download && \
  cd ssdeep-2.12 && \
  ./configure && \
  make install && \
  pip install pydeep && \
  cd .. && \
  rm -rf ssdeep-2.12
RUN groupadd -r nonroot -g 433 && \
  useradd -u 431 -r -g nonroot -d /home/nonroot -s /sbin/nologin -c "Nonroot User" nonroot && \
  mkdir /home/nonroot && \
  chown -R nonroot:nonroot /home/nonroot

USER nonroot
WORKDIR /home/nonroot
RUN git clone https://github.com/botherder/viper.git

USER root
WORKDIR /home/nonroot/viper
RUN chmod a+xr viper.py &&\
  pip install -r requirements.txt 

USER nonroot
WORKDIR /home/nonroot/viper
ENTRYPOINT ["./viper.py"]
CMD [""]
