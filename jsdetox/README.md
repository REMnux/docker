= JSDetox Malware Analysis Tool for JavaScript Deobfuscation

This image encapsulates the [JSDetox][1] malware analysis tool for JavaScript deobfuscation by [@sven_t][2]. To run JSDetox after installing Docker, use the following command:

    sudo docker run --rm -p 3000:3000 remnux/jsdetox

Then, connect to http://localhost:3000 using your web browser.

To stop JSDetox, use "`sudo docker ps -l`" to obtain the container ID, then use the "`sudo docker stop *container-id*`" and wait about a minute.

  [1]: http://www.relentless-coding.com/projects/jsdetox
  [2]: https://twitter.com/sven_t
