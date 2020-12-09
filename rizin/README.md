This Docker image encapsulates the [Rizin][1] reverse-engineering framework.

To run this image after installing Docker, use a command like this, replacing "~/workdir" with the path to your working directory on the underlying host:

    docker run --rm -it --cap-drop=ALL --cap-add=SYS_PTRACE -v ~/workdir:/home/nonroot/workdir remnux/rizin

Then run `rizin` or other Rizin commands (starting with `rz-`) inside the container. Before running the application, create ~/workdir on your host.

This Dockerfile is based on the instructions documented in the official [Rizin Dockerfile][2] file.


  [1]: https://rizin.re
  [2]: https://github.com/rizinorg/rizin/blob/dev/Dockerfile
