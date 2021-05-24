# This is a RetDec docker built on Ubuntu 20.04 LTS
# The RetDec source sofware can be found at:
# https://github.com/avast/retdec
#
# RetDec is a retargetable machine-code compiler
# based on LLVM.
#
# To use this docker, issue the following command:
# sudo docker run -it --rm -v <path_to_binary>:/tmp/files remnux/retdec /bin/bash
#
# Where <path_to_binary> is the local path where your binary files
# of interest are located
#
# Commands available with RetDec include:
#
# retdec-ar-extractor	 retdec-config	 retdec-fileinfo.py
# retdec-macho-extractor retdec-unpacker retdec-archive-decompiler.py
# retdec-config.py	 retdec-getsig	 retdec-pat2yara
# retdec-unpacker.py	 retdec-bin2llvmir retdec-decompiler.py
# retdec-idb2pat	 retdec-signature-from-library-creator.py 
# retdec-utils.py	 retdec-bin2pat	 retdec-fileinfo
# retdec-llvmir2hll      retdec-stacofin retdec-yarac
#
# User/Pass: retdec/retdec
#

FROM ubuntu:20.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="24 May 2021"
LABEL updated_by="digitalsleuth"

USER root
RUN apt-get update && apt-get upgrade -y && apt-get install wget curl sudo xz-utils python3 rsync graphviz -y && \
rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/src

RUN wget https://github.com/avast/retdec/releases/download/v4.0/retdec-v4.0-ubuntu-64b.tar.xz && \
tar -xvf retdec-v4.0-ubuntu-64b.tar.xz && \
rsync -a retdec/ /usr/local/ && \
rm -rf retdec*

RUN wget https://github.com/upx/upx/releases/download/v3.96/upx-3.96-amd64_linux.tar.xz && \
tar -xvf upx-3.96-amd64_linux.tar.xz && \
mv upx-3.96-amd64_linux/upx /usr/local/bin && \
rm -rf upx-3.96-amd64_linux*

RUN groupadd -r retdec && \
    useradd -m -d /home/retdec -g retdec -s /usr/sbin/nologin -c "RETDEC User" retdec && \
    mkdir -p /tmp/files && \
    chown -R retdec:retdec /home/retdec /tmp/files && \
    usermod -a -G sudo retdec && echo 'retdec:retdec' | chpasswd

USER retdec
ENV HOME /home/retdec
ENV USER retdec
WORKDIR /home/retdec
VOLUME ["/tmp/files"]
