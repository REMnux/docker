Automatically recognize and decode/decrypt common encoding and encryption techniques.

[Ciphey](https://github.com/Ciphey/Ciphey) is designed to automatically recognize and decode/decrypt common encoding and encryption techniques. It was created by Brandon Skerritt and is licensed under MIT License. According the author, the tool uses "natural language processing & artifical intelligence, along with some common sense."

To run Ciphey using this Docker container, create a directory where you'll store your input and output files. Then, use a command like this to open a shell inside the container where you can run `ciphey` and have your directory mapped as `/home/nonroot/workdir` inside the container:

```
docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/ciphey
```

The password for the container's user `nonroot` is `nonroot`. The remnux/ciphey image is hosted on its [Docker Hub page](https://hub.docker.com/repository/docker/remnux/ciphey).
