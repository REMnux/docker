This Docker image encapsulates the [Rizin](https://rizin.re) reverse-engineering framework.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/rizin

Then run `rizin` or other Rizin commands (starting with `rz-`) inside the container. Before running the application, create ~/workdir on your host.
