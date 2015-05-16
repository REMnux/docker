This Dockerfile represents a Docker image that encapsulates the [Maltrieve](https://github.com/krmaxwell/maltrieve) tool created by Kyle Maxwell ([@krmaxwell](https://github.com/krmaxwell)) for retrieving malware samples.

This Dockerfile is based heavily on [the one from Kyle's Maltrieve repository](https://github.com/krmaxwell/maltrieve/blob/master/docker/Dockerfile), which is maintained by Michael Boman.

To run this image after installing Docker, use a command like this, replacing
"~/archive" with the path to your working directory on the underlying host.
This is where the downloaded malware samples will be deposited.

    sudo docker run --rm -it -v ~/archive:/archive remnux/maltrieve 

This will launch Maltrieve without any parameters, directing the tool to retrieve
malware samples and save them to the ~/archive directory.

If you wish to specify command-line parameters to Maltrieve, then launch it like this:

    sudo docker run --rm -it -v ~/archive:/archive remnux/maltrieve bash

This will launch the bash shell in the container, at which point you can run the command
"maltrieve", specifying optional command-line parameters if you wish.

Before running the container, create ~/archive on your host and make it world-accessible
(`chmod a+xwr`).
