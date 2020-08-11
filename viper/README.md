# Viper Binary Analysis and Management Framework

This Dockerfile represents a Docker image that encapsulates the [Viper][1] binary analysis and management framework by Claudio Guarnieri ([@botherder][2] - [homepage][3]).

To run this image after installing Docker, use a command like this to launch the container, replacing "~/workdir" with the path to the location of the data to analyse:

    sudo docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/viper

To run the "clamav" Viper plugin, the clamav-daemon must be running in the container. You can enable this by running:

    sudo service clamav-daemon start

  [1]: https://github.com/viper-framework/viper
  [2]: https://twitter.com/botherder
  [3]: https://nex.sx/
