# Thug Low-Interaction Honeyclient

This Docker image encapsulates [Thug][1], a low-interaction honeyclient, which was created by Angelo Dell'Aera (angelodellaera).

The file below is based on ideas from [Spenser Reinhardt's Dockerfile][2] and on instructions outlined by [M. Fields][3].

To run this image after installing Docker, use a command like this:

    sudo docker run --rm -it remnux/thug bash

then run `./thug.py` with the desired parameters.

To share the "logs" directory between your host and the container, create a "logs" directory on your host and make it world-accessible (e.g., "`chmod a+xwr ~/logs`"). Then run the tool like this:

    sudo docker run --rm -it -v ~/logs:/home/thug/logs remnux/thug bash

If you'd like to share an additional directory (e.g., "files"), supply the mapping using another `-v` parameter such as "`-v ~/files:/home/thug/files`", but remember to make the directory on your host world-accessible.

To support distributed operations and MongoDB output, install the folloging packages into the image using "`apt-get`": mongodb, mongodb-dev, python-pymongo, rabbitmq-server, python-pika. Also, remove the "`sed`" command that disables
logging in the thug\src\Logging\logging.conf file.

  [1]: https://github.com/buffer/thug
  [2]: https://registry.hub.docker.com/u/sreinhardt/honeynet/dockerfile
  [3]: https://twitter.com/shakey_1
