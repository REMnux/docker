# Rekall Memory Forensic Framework

This Dockerfile represents a Docker image that encapsulates the [Rekall Memory Forensic Framework][1]. To run this image after installing Docker, use a command like this:

    sudo docker run --rm -it -v <local_directory>:/home/nonroot/files remnux/rekall

then run `rekall` in the container with the desired parameters.

Before running the command above, you can create the desired <local_directory> on your host.

  [1]: http://www.rekall-forensic.com
