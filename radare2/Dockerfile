# Name: radare2
# Website: https://www.radare.org/n/radare2.html
# Description: Examine binary files, including disassembling and debugging.
# Category: Dynamically Reverse-Engineer Code: General
# Author: https://github.com/radareorg/radare2/blob/master/AUTHORS.md
# License: GNU Lesser General Public License (LGPL) v3: https://github.com/radareorg/radare2/blob/master/COPYING
# Notes: r2, rasm2, rabin2, rahash2, rafind2, r2agent
#
# To run this image after installing Docker, use the command below, replacing
# "~/workdir" with the path to your working directory on the underlying host.
# Before running the docker, create ~/workdir on your host.
#
# docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/radare2
#
# Then run "r2" or other Radare2 commands inside the container.
#
# Running 'r2agent -a' will enable the web-based interface on port 8080 by default.
# To access this, add '-p 8080:8080' to the above docker command (before 'remnux/radare2')
# Then browse to your http://YOUR_IP:8080. 

FROM ubuntu:20.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="13 Apr 2022"
LABEL updated_by="Corey Forman"
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ARG R2VER=5.6.6

USER root
RUN apt-get update && apt-get install -y \
  sudo \
  wget \
  git && \
  rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
  useradd -m -d /home/nonroot -g nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
  mkdir -p /home/nonroot/workdir && \
  chown -R nonroot:nonroot /home/nonroot && \
  usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd && \
			echo "nonroot ALL=(ALL) NOPASSWD: ALL" >/etc/sudoers.d/nonroot && \
  mkdir /usr/local/radare2 && \
  chown nonroot:nonroot /usr/local/radare2
  
RUN wget -O /tmp/radare2_${R2VER}_amd64.deb https://github.com/radareorg/radare2/releases/download/${R2VER}/radare2_${R2VER}_amd64.deb && \
  dpkg -i /tmp/radare2_${R2VER}_amd64.deb && \
  r2pm init && \
  r2pm update && \
  rm /tmp/radare2_${R2VER}_amd64.deb

USER root
RUN chown -R root:root /usr/local/radare2

USER nonroot
ENV HOME /home/nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
EXPOSE 8080
CMD ["/bin/bash"]
