# Name: Sogen
# Website: https://github.com/momo5502/sogen
# Description: Emulate Windows user-mode programs on Linux by running the real
#   Windows system DLLs on an emulated CPU, with API and syscall tracing, a GDB
#   server that anti-debugging checks can't see, snapshots, and deterministic runs.
# Category: Dynamically Reverse-Engineer Code: General
# Author: Maurice Heumann (momo5502)
# License: GPL-2.0: https://github.com/momo5502/sogen/blob/main/LICENSE
# Notes: analyzer
#
# Sogen needs an "emulation root": a directory with the Windows system DLLs,
# registry hives, and API set map that the emulated program will see. The image
# doesn't include one, because Microsoft owns those files. When the
# container starts without a root, it explains the two ways to get one:
#
#   get-sogen-root        Download the prebuilt root from sogen.dev (about
#                         180 MB, 520 MB unpacked) into the working directory
#   create-root.bat       Build your own on a Windows system with the script
#                         from the Sogen repository
#
# To run Sogen within this Docker container, create a directory where you'll
# store your samples and the emulation root, e.g. ~/workdir. Then launch the
# container with that directory mapped as /home/nonroot/workdir:
#
#   docker run --rm -it -v ~/workdir:/home/nonroot/workdir remnux/sogen
#
# Inside the container, run get-sogen-root once. After that, analyze a sample
# with a command like this (the analyzer finds the root in the working
# directory on its own and maps the file into the emulated c: drive):
#
#   analyzer sample.exe
#
# To debug the emulated program with GDB or IDA from the host, publish the
# debug port on loopback when you start the container, then run the analyzer
# with -d and --bind 0.0.0.0:
#
#   docker run --rm -it -p 127.0.0.1:28960:28960 -v ~/workdir:/home/nonroot/workdir remnux/sogen
#   analyzer -d --bind 0.0.0.0 --port 28960 sample.exe
#
# The emulated program runs offline by default. Add --network live to the
# analyzer command to let it use the container's network.
#
# The sogen Docker image is hosted in the REMnux Docker Hub repository.
#
# For documentation on Sogen, see the project wiki:
# https://github.com/momo5502/sogen/wiki

# Sogen publishes no releases, so the image builds the analyzer from a pinned
# commit. The Rust parts (the icicle backend), the SDL3 GUI and audio
# backends, the Python bindings, and the Steam bridge stay off: the image is a
# headless command-line tool with the Unicorn backend. AVX2 stays off so the
# binary runs on any x86-64 CPU and under emulation. The build uses Ubuntu's
# GCC 13, the compiler of Sogen's own ubuntu-24.04 CI job with these flags.
# Ubuntu's Clang 18 rejects a CPU-feature builtin in the KVM backend.
FROM ubuntu:24.04 AS build
ARG SOGEN_COMMIT=a4b7b2dbf3e1febe6741ee02aaffdb21aae29a17

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    cmake \
    g++ \
    git \
    ninja-build \
    pkg-config \
    python3 && \
    rm -rf /var/lib/apt/lists/*

# Shallow clone of the pinned commit plus the submodules the headless build
# needs. deps/FEX, deps/SDL, and deps/nanobind stay out: FEX is the arm64 JIT
# backend, SDL is the GUI layer, and nanobind is for the Python bindings.
RUN git init -q /src && \
    cd /src && \
    git remote add origin https://github.com/momo5502/sogen.git && \
    git fetch -q --depth 1 origin "${SOGEN_COMMIT}" && \
    git checkout -q FETCH_HEAD && \
    git submodule update -q --init --recursive --depth 1 --jobs 4 \
      deps/CLI11 \
      deps/Vulkan-Headers \
      deps/base64 \
      deps/capstone \
      deps/flatbuffers \
      deps/googletest \
      deps/gtest-parallel \
      deps/mbedtls \
      deps/minidump_cpp \
      deps/reflect \
      deps/reproc \
      deps/sogen-linux-files \
      deps/unicorn \
      deps/zstd

RUN cmake -S /src -B /src/build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DSOGEN_ENABLE_RUST_CODE=OFF \
      -DSOGEN_ENABLE_SDL3=OFF \
      -DSOGEN_ENABLE_AVX2=OFF \
      -DSOGEN_ENABLE_PYTHON_BINDINGS=OFF \
      -DSOGEN_ENABLE_STEAM=OFF && \
    cmake --build /src/build --target analyzer

# The analyzer loads the CPU backends as shared libraries from its own
# directory ($ORIGIN runpath), so they travel with it.
RUN mkdir -p /out/opt/sogen && \
    install -m 755 /src/build/artifacts/analyzer /src/build/artifacts/*.so /out/opt/sogen/ && \
    install -m 644 /src/LICENSE /out/opt/sogen/LICENSE && \
    echo "${SOGEN_COMMIT}" > /out/opt/sogen/COMMIT

FROM ubuntu:24.04
LABEL maintainer="Lenny Zeltser (@lennyzeltser, www.zeltser.com)"
LABEL updated="17 Oct 2026"
LABEL updated_by="lennyzeltser"

ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

USER root

# curl and unzip serve get-sogen-root.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    unzip && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /out/opt/sogen /opt/sogen
COPY --chmod=755 analyzer get-sogen-root entrypoint.sh /usr/local/bin/

RUN groupadd -r nonroot && \
    useradd -m -r -g nonroot -d /home/nonroot -s /bin/bash -c "Nonroot User" nonroot && \
    mkdir -p /home/nonroot/workdir && \
    chown -R nonroot:nonroot /home/nonroot

USER nonroot
ENV HOME=/home/nonroot
ENV USER=nonroot
# The analyzer wrapper and get-sogen-root use this path for the emulation root.
ENV SOGEN_ROOT=/home/nonroot/workdir/root
WORKDIR /home/nonroot/workdir
VOLUME ["/home/nonroot/workdir"]
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/bash"]
