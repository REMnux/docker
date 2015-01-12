a Docker experiment: Ubuntu trusty plus all of the libraries and base data files needed to run 
a handy Python program from the excellent Malware Analyst Cookbook: pescanner. 

With inspiration and forks from @lennyzeltser and [REMnux](https://github.com/remnux/docker) .

Includes:

 - Ubuntu trusty base
 - apt in python-magic, yara, python-yara, pip, clamav (all in multiverse) 
 - pip in pefile 
 - manually install capabilities.yara, userdb.txt, and pescanner.py

Sources:

 - http://code.google.com/p/pefile/
 - http://code.google.com/p/malwarecookbook/source/browse/trunk/3/5/capabilities.yara
 - http://code.google.com/p/reverse-engineering-scripts/downloads/detail?name=UserDB.TXT&can=2&q=
 - http://code.google.com/p/malwarecookbook/source/browse/trunk/3/8/pescanner.py

Refs:

 - Malware Analyst Cookbook: http://www.malwarecookbook.com/
 - REMnux reverse engineering malware distribution: http://zeltser.com/remnux/
 
Usage
-----

To run this image after building or importing it use a command like this to scan a specific files, replacing
"~/workdir" with the path to your working directory on the underlying host:

```
sudo docker run -it -v ~/workdir:/home/nonroot/workdir adricnet/mac-pescanner /opt/pescanner.py [target file]
```

Before running the application, create ~/workdir on your host and make it world-accessible ("chmod a+xwr").
