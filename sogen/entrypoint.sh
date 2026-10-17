#!/bin/sh
# Explains how to get an emulation root when someone opens a shell in a
# container that has none, then runs the requested command (a shell by
# default). The explanation appears only on a terminal, so scripted runs such
# as "docker run remnux/sogen analyzer ..." see nothing but their own output.

root="${SOGEN_ROOT:-/home/nonroot/workdir/root}"

if [ -t 1 ] && [ ! -f "$root/api-set.bin" ]; then
    cat <<EOF

Sogen needs an emulation root: a directory with the Windows system DLLs,
registry hives, and API set map that the emulated program will see. The
REMnux image doesn't include one, because Microsoft owns those files.
No root was found at $root.

You have two options:

  1. Download the prebuilt root from the Sogen project (about 180 MB,
     520 MB unpacked) into your working directory:

       get-sogen-root

  2. Build your own on a Windows system with create-root.bat from the Sogen
     repository, then copy the resulting "root" directory into your working
     directory:

       https://github.com/momo5502/sogen/wiki/Run-The-Emulator

Once the root is in place, analyze a sample with:

       analyzer sample.exe

EOF
fi

exec "$@"
