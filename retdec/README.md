This Docker image encapsulates [RetDec](https://github.com/avast/retdec), a retargetable machine-code decompiler based on LLVM.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it -v ~/workdir:/home/retdec/workdir remnux/retdec

Then run RetDec commands (starting with `retdec-`) inside the container, such as `retdec-decompiler`, `retdec-fileinfo`, and `retdec-unpacker`. Before running the application, create ~/workdir on your host.
