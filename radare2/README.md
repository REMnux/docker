This Docker image encapsulates the [Radare2](http://radare.org/) reverse-engineering framework.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/radare2

Then run `r2` or other Radare2 commands inside the container. Before running the application, create ~/workdir on your host.
