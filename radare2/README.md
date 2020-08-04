This Docker image encapsulates the [Radare2][1] reverse-engineering framework.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/radare2

Then run `r2` or other Radare2 commands inside the container. Before running the application, create ~/workdir on your host.

This Dockerfile is based on the instructions documented in the official [Radare2 Dockerfile][2] file.


  [1]: http://radare.org/
  [2]: https://github.com/radareorg/radare2/blob/master/Dockerfile
