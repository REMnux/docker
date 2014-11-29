# Viper Binary Analysis and Management Framework

This Dockerfile represents a Docker image that encapsulates the [Viper][1] binary analysis and management framework by Claudio Guarnieri ([@botherder][2]).  To run this image after installing Docker, use a command like this, replacing "~/viper-workdir" with the path to the location of your Viper Viper data directory.

    sudo docker run --rm -it -v ~/viper-workdir:/home/nonroot/workdir remnux/viper

Before running Viper, create the  ~/viper-workdir and make it world-accessible ("`chmod a+xwr`").

  [1]: http://viper.li
  [2]: https://twitter.com/botherder
