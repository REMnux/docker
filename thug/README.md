# Thug Low-Interaction Honeyclient

This Dockerfile represents a Docker image that encapsulates [Thug][1], a low-interaction honeyclient, which was created by Angelo Dell'Aera (angelodellaera).

The file below is based on ideas from [Spenser Reinhardt's Dockerfile][2], on instructions outlined by [M. Fields][3] and on the installation script created by [Payload Security][4].

To run this image after installing Docker, you have a number of options:

`sudo docker run --rm  -v <local_folder>:/tmp/thug/logs remnux/thug <variables>`

This will allow you to run thug as a 'headless' application without having to enter the docker. Variables can be passed on the command-line (such as -F to enable file logging). Logs are stored in /tmp/thug/logs by default. Your <local_folder> should be made world-accessible to ensure no permissions issues: e.g. "chmod a+xwr ~/logs"

`sudo docker run --rm -it --entrypoint "/bin/bash" remnux/thug`

This will enter you into the docker where you can run "thug" with the desired parameters (such as -F to enable file logging).

`sudo docker run --rm -it -v <local_folder>:/tmp/thug/logs --entrypoint "/bin/bash" remnux/thug`

This is essentially a combination of both of the above, allowing you entry into the docker, and storage of log files in your host environment.

To support distributed operations and MongoDB output, install the following packages into the image using "apt-get mongodb mongodb-dev python-pymongo rabbitmq-server python-pika"

  [1]: https://github.com/buffer/thug
  [2]: https://registry.hub.docker.com/u/sreinhardt/honeynet/dockerfile
  [3]: https://twitter.com/shakey_1
  [4]: https://github.com/PayloadSecurity/VxCommunity/blob/master/bash/thuginstallation.sh
