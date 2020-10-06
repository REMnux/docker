# de4js JavaScript Deobfuscator and Unpacker

This Dockerfile represents a Docker image that encapsulates the [de4js][1] Javascript deobfuscation tool.
It's based on the original instructions documented in the official [GitHub][2] repository.

To run this image after installing Docker, you can use the following command:

    sudo docker run -d --rm -p 4000:4000 -p 35729:35729 --name de4js remnux/de4js

Then browse to `http://localhost:4000/de4js/`

It's important to remember the trailing slash after the above URL

To stop de4js, use `sudo docker stop de4js`.

  [1]: https://github.com/lelinhtinh/de4js
  [2]: https://github.com/lelinhtinh/de4js/blob/master/Dockerfile
