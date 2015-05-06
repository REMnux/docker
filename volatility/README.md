# The Volatility Framework for Memory Forensics

This Dockerfile represents a Docker image that encapsulates the [Volatility Framework][1] for memory forensics by the Volatility Foundation. To run this image after installing Docker, use a command like this:

    sudo docker run --rm -it -v ~/memdumps:/home/nonroot/memdumps remnux/volatility bash

then run `vol.py` in the container with the desired parameters.

Before running the command above, create the "memdumps" directory on your host and make it world-accessible (e.g., `chmod a+xwr ~/memdumps`).


  [1]: http://www.volatilityfoundation.org/#!releases/component_71401
