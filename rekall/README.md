# Rekall Memory Forensic Framework

This Dockerfile represents a Docker image that encapsulates the [Rekall Memory Forensic Framework][1]. To run this image after installing Docker, use a command like this:

    sudo docker run --rm -it -v ~/files:/home/nonroot/files remnux/rekall bash

then run "`rekall`" in the container with the desired parameters.

Before running the command above, create the "files" directory on your host and make it world-accessible (e.g., "`chmod a+xwr ~/files`").

To use Rekall's web console, invoke the container with the `-p` parameter to give your host access to the container's TCP port 8000 like this:

    sudo docker run --rm -it -p 8000:8000 -v ~/files:/home/nonroot/files remnux/rekall

Then connect to http://localhost:8000 using a web browser from your host.


  [1]: http://www.rekall-forensic.com
