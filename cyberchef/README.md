This Docker image encapsulates the [CyberChef multi-purpose analysis tool][1] by GCHQ,
which is a web-based app for "encryption, encoding, compression and data analysis."

To run this image in the background after installing Docker,
use the following command:

`sudo docker run -d -p 8080:80 remnux/cyberchef`

Then, connect to http://localhost:8080 using your web browser.
To stop the container, use Docker's `ps` and `stop` commands.

  [1]: https://github.com/gchq/CyberChef
