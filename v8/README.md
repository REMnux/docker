# Google's V8 JavaScript Engine

This Dockerfile represents a Docker image that encapsulates the command-line tool "d8" from [Google's V8 JavaScript Engine][1].

To run this image after installing Docker, use a command like this, replacing "~/files" with the path to the location of the files you'd like to examine within the container:

    sudo docker run --rm -it -v ~/files:/home/nonroot/files remnux/v8 bash

Before running the image, create the  ~/files directory and make it world-accessible ("`chmod a+xwr`").

Once you've activated the container using the command above, you can run the command-line version of V8 by typing the "d8" command (e.g., "`d8 -f ~/files/file.js`"). To use the pre-defined JavaScript definitions, supply a command like "`d8 -f ~/def.js ~/files/file.js`".


  [1]: https://code.google.com/p/v8
