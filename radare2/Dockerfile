# Name: radare2
# Website: https://www.radare.org/n/radare2.html
# Description: Examine binary files, including disassembling and debugging. Includes r2ai and decai plugins for LLM-powered analysis (API key or local Ollama required), plus the r2ghidra plugin for Ghidra decompilation via the pdg command.
# Category: Dynamically Reverse-Engineer Code: General
# Author: https://github.com/radareorg/radare2/blob/master/AUTHORS.md
# License: GNU Lesser General Public License (LGPL) v3: https://github.com/radareorg/radare2/blob/master/COPYING
# Notes: r2, rasm2, rabin2, rahash2, rafind2, r2agent, r2ai, decai, pdg
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
#
# The image is built for amd64 and arm64.

FROM ubuntu:24.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="15 Oct 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

# When changing R2VER, update the SHA-256 hashes of that version's release files too.
ARG R2VER=6.2.4
ARG R2_AMD64_SHA256=7019eedc0e0e87d1f53d6b8f5fc62b898567679c5efdce7fbfc557c9e7655e90
ARG R2_ARM64_SHA256=bbf48ee7bd5d8282f65a297dcabd34c9961a500e62d6b036679caab187b32ef1
ARG R2DEV_AMD64_SHA256=cec4832762c4d0a029f78e724ce6a0d83cf8f04fe8ae5f69b50486983c08e347
ARG R2DEV_ARM64_SHA256=09e4e50be48e3dc79b541a37f3bf1ee6ef21e33c5005b9cf232fa41952d74ade
# r2ghidra_${R2VER}_amd64.deb and, because r2ghidra publishes no arm64 .deb,
# r2ghidra-${R2VER}-linux-arm-64.zip
ARG R2GHIDRA_AMD64_SHA256=e5c184cc6943f5e99bcb1ecc2f3bdf200e58865eea01edfbfb787b0e476ea385
ARG R2GHIDRA_ARM64_SHA256=a8ac843c4e23e6cbf3c4e0975d84215f4706172109130fa0ee2229bc56faec26

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    sudo \
    wget \
    git && \
    rm -rf /var/lib/apt/lists/*

# Install radare2 plus the r2ghidra plugin (Ghidra decompiler, provides the pdg command).
# On arm64, r2ghidra comes from the binary bundle that upstream builds for r2pm. Its files
# go where the amd64 .deb puts them: the plugin and its Sleigh files in radare2's plugin
# directory, and sleighc and r2fidb in /usr/local/bin.
RUN set -e; \
    ARCH=$(dpkg --print-architecture); \
    case "$ARCH" in \
      amd64) R2_SHA256=$R2_AMD64_SHA256; R2GHIDRA_SHA256=$R2GHIDRA_AMD64_SHA256 ;; \
      arm64) R2_SHA256=$R2_ARM64_SHA256; R2GHIDRA_SHA256=$R2GHIDRA_ARM64_SHA256 ;; \
      *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;; \
    esac; \
    wget -q -O /tmp/radare2.deb \
      https://github.com/radareorg/radare2/releases/download/${R2VER}/radare2_${R2VER}_${ARCH}.deb; \
    echo "$R2_SHA256  /tmp/radare2.deb" | sha256sum -c -; \
    apt-get update; \
    apt-get install -y /tmp/radare2.deb; \
    if [ "$ARCH" = amd64 ]; then \
      wget -q -O /tmp/r2ghidra.deb \
        https://github.com/radareorg/r2ghidra/releases/download/${R2VER}/r2ghidra_${R2VER}_amd64.deb; \
      echo "$R2GHIDRA_SHA256  /tmp/r2ghidra.deb" | sha256sum -c -; \
      apt-get install -y /tmp/r2ghidra.deb; \
    else \
      wget -q -O /tmp/r2ghidra.zip \
        https://github.com/radareorg/r2ghidra/releases/download/${R2VER}/r2ghidra-${R2VER}-linux-arm-64.zip; \
      echo "$R2GHIDRA_SHA256  /tmp/r2ghidra.zip" | sha256sum -c -; \
      DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends unzip; \
      unzip -q /tmp/r2ghidra.zip -d /tmp/r2ghidra; \
      PLUGDIR=$(r2 -H R2_LIBR_PLUGINS); \
      mkdir -p "$PLUGDIR"; \
      cp -a /tmp/r2ghidra/plugins/core_ghidra.so /tmp/r2ghidra/plugins/r2ghidra_sleigh "$PLUGDIR/"; \
      install -m 755 /tmp/r2ghidra/bin/sleighc /tmp/r2ghidra/bin/r2fidb /usr/local/bin/; \
      apt-get remove --purge -y unzip; \
      rm -rf /tmp/r2ghidra /tmp/r2ghidra.zip; \
    fi; \
    apt-get remove --purge -y libradare2-common 2>/dev/null || true; \
    rm -f /tmp/radare2.deb /tmp/r2ghidra.deb; \
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
RUN set -e; \
    ARCH=$(dpkg --print-architecture); \
    case "$ARCH" in \
      amd64) R2DEV_SHA256=$R2DEV_AMD64_SHA256 ;; \
      arm64) R2DEV_SHA256=$R2DEV_ARM64_SHA256 ;; \
      *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;; \
    esac; \
    sudo wget -q -O /tmp/radare2-dev.deb \
      https://github.com/radareorg/radare2/releases/download/${R2VER}/radare2-dev_${R2VER}_${ARCH}.deb; \
    echo "$R2DEV_SHA256  /tmp/radare2-dev.deb" | sha256sum -c -; \
    sudo apt-get update; \
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      gcc make pkg-config libc6-dev curl; \
    sudo dpkg -i /tmp/radare2-dev.deb; \
    r2pm -ci r2ai; \
    r2pm -ci decai; \
    sudo dpkg -r radare2-dev; \
    sudo rm -f /tmp/radare2-dev.deb; \
    sudo apt-get remove --purge -y gcc make pkg-config libc6-dev curl; \
    sudo apt-get autoremove --purge -y; \
    sudo apt-get clean; \
    sudo rm -rf /var/lib/apt/lists/*

ENV HOME=/home/nonroot
ENV USER=nonroot
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
EXPOSE 8080
CMD ["/bin/bash"]
