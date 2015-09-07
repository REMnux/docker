# Collaborative Research Into Threats (CRITs) by MITRE

This Docker image encapsulates the [Collaborative Research Into Threats](https://crits.github.io/) (CRITs)  malware and threat repository by The MITRE Corporation.

To run this image after installing Docker, use a command like this, replacing “~/crits-data" with the path to the location for storing CRITs data, indefinitely:

    sudo docker run --rm -it -v ~/crits-data:/home/nonroot/workdir -p 8443:8443 remnux/crits 

Before running CRITs, create the ~/crits-data directory and make it world-accessible ("`chmod a+xwr`").

After launching the container, give it some time to start up. Then, when you see the info about temporary logon credentials, connect to https://localhost:8443 using your web browser.
