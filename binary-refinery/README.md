Transform binary data through a collection of standalone command-line tools that comprise [the Binary Refinery™ toolkit](https://github.com/binref/refinery), chaining the individual tools as necessary.

To run Binary Refinery™ tools within this Docker container, create a directory where you'll store your input files, e.g. ~/workdir. Then, use a command like this to launch the container and have your directory mapped as /home/nonroot/workdir inside the container:

```
docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/binary-refinery
```

The binary-refinery Docker image is hosted in the REMnux Docker Hub repository.

For documentation on Binary Refinery, including the listing of its tools, see: https://binref.github.io and https://github.com/binref/refinery
