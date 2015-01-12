This Dockerfile represents a Docker image that encapsulates the [pescanner](https://code.google.com/p/malwarecookbook/source/browse/trunk/3/8/pescanner.py) tool created by Michael Ligh for performing static analysis of suspicious Windows PE files. The image is using the version of the tool that was [modified by Glenn P. Edwards Jr.](https://github.com/hiddenillusion/AnalyzePE/blob/master/pescanner.py) to introduce imphash support. The original version was distributed with the book [Malware Analyst Cookbook](http://www.malwarecookbook.com/). The Dockerfile was contributed to the [REMnux](https://REMnux.org) collection by [Adric Net](http://adric.net/). The Docker image built by this file includes: 

 - Ubuntu base
 - apt in python-magic, yara, python-yara, pip, clamav (all in multiverse) 
 - capabilities.yara, userdb.txt, pescanner.py, pefile
 - pydams via libdasm (needed for imphash calculations)
 
To run this image after installing Docker, use a command like this, replacing *~/workdir* with the path to your working directory on the underlying host:

```
sudo docker run --rm -it -v ~/workdir:/home/nonroot/workdir remnux/pescanner bash
```

This will launch the bash shell in the container, at which point you can run the "pescanner" command to scan the desired file. Before running the application, create *~/workdir* on your host and make it world-accessible (`chmod a+xwr`).
