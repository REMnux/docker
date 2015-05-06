# MASTIFF Static Analysis Framework 

This Docker image encapsulates the [MASTIFF static analysis framework][1] by The MASTIFF Project at KoreLogic

    sudo docker run --rm -it -v ~/memdumps:/home/nonroot/memdumps remnux/volatility bash

then run mas.py in the container with the desired parameters.

To run this image after installing Docker, use a command like this, replacing "~/mastiff-workdir"  with the path to the location of your MASTIFFF directory:

    sudo docker run --rm -it -v ~/mastiff-workdir:/home/nonroot/workdir remnux/mastiff

Before running MASTIFF, create the  "~/mastiff-workdir" directory and make it world-accessible (`chmod a+xwr`).

  [1]: https://github.com/KoreLogicSecurity/mastiff
