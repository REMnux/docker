# Viper Binary Analysis and Management Framework

This Dockerfile represents a Docker image that encapsulates the [Viper][1] binary analysis and management framework by Claudio Guarnieri ([@botherder][2]).

To run this image after installing Docker,  use a command like this to launch the Viper web interface, replacing "~/viper-workdir" with the path to the location of	your Viper Viper data directory:	

    sudo docker run --rm -p 8080:8080 -v ~/viper-workdir:/home/nonroot/workdir remnux/viper

Before running Viper, create the  ~/viper-workdir and make it world-accessible ("`chmod a+xwr`").

If you want to launch the Viper command-line tool instead of its web interface, run Bash in the container like this, then issue the desired ./viper-cli command:
	
    sudo docker run --rm -it -v ~/viper-workdir:/home/nonroot/workdir remnux/viper bash

  [1]: http://viper.li
  [2]: https://twitter.com/botherder
