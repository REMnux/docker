# JSDetox Malware Analysis Tool for JavaScript Deobfuscation

This Dockerfile represents a Docker image that encapsulates the [JSDetox][1] malware analysis tool for JavaScript deobfuscation by [@sven_t][2]. To run JSDetox after installing Docker, use the following command:

    sudo docker run -d --rm --name jsdetox -p 3000:3000 remnux/jsdetox

Then, connect to http://localhost:3000 using your web browser. The startup process will take between 30 seconds to a minute.

To stop JSDetox, use "`sudo docker stop jsdetox`".

  [1]: http://www.relentless-coding.com/projects/jsdetox
  [2]: https://twitter.com/sven_t
