# Name: radare2
# Website: https://www.radare.org/n/radare2.html
# Description: Examine binary files, including disassembling and debugging.
# Category: Dynamically Reverse-Engineer Code: General
# Author: https://github.com/radareorg/radare2/blob/master/AUTHORS.md
# License: GNU Lesser General Public License (LGPL) v3: https://github.com/radareorg/radare2/blob/master/COPYING
# Notes: r2, rasm2, rabin2, rahash2, rafind2, r2agent, r2ai, decai
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
# Then browse to http://YOUR_IP:8080.

FROM ubuntu:24.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="10 Feb 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8
ARG R2VER=6.0.8

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    sudo \
    wget \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O /tmp/radare2_${R2VER}_amd64.deb \
    https://github.com/radareorg/radare2/releases/download/${R2VER}/radare2_${R2VER}_amd64.deb && \
    apt-get update && \
    apt-get install -y /tmp/radare2_${R2VER}_amd64.deb && \
    (apt-get remove --purge -y libradare2-common 2>/dev/null || true) && \
    rm -f /tmp/radare2_${R2VER}_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r nonroot && \
    useradd -m -d /home/nonroot -g nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
    mkdir -p /home/nonroot/workdir && \
    chown -R nonroot:nonroot /home/nonroot && \
    usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd && \
    echo "nonroot ALL=(ALL) NOPASSWD: ALL" >/etc/sudoers.d/nonroot

USER nonroot
RUN r2pm -U

# Install r2ai and decai plugins (build deps removed at end of layer)
RUN sudo wget -q -O /tmp/radare2-dev_${R2VER}_amd64.deb \
    https://github.com/radareorg/radare2/releases/download/${R2VER}/radare2-dev_${R2VER}_amd64.deb && \
    sudo apt-get update && \
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gcc make pkg-config libc6-dev curl && \
    sudo dpkg -i /tmp/radare2-dev_${R2VER}_amd64.deb && \
    r2pm -ci r2ai && \
    r2pm -ci decai && \
    sudo dpkg -r radare2-dev && \
    sudo rm -f /tmp/radare2-dev_${R2VER}_amd64.deb && \
    sudo apt-get remove --purge -y gcc make pkg-config libc6-dev curl && \
    sudo apt-get autoremove --purge -y && \
    sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*

ENV HOME=/home/nonroot
ENV USER=nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
EXPOSE 8080
CMD ["/bin/bash"]
