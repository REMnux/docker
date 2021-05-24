# RetDec Retargetable machine-code decompiler

This is a RetDec docker built on Ubuntu 20.04 LTS that encapsulates [RetDec][1], a Retargetable Decompiler, created by Avast.

The original source for the software can be 

To use this docker, issue the following command:

`sudo docker run -it --rm -v <path_to_binary>:/tmp/files remnux/retdec /bin/bash`

Where <path_to_binary> is the local path where your binary files of interest are located

Commands available with RetDec include:

`retdec-ar-extractor    retdec-config   retdec-fileinfo.py`
`retdec-macho-extractor retdec-unpacker retdec-archive-decompiler.py`
`retdec-config.py       retdec-getsig   retdec-pat2yara`
`retdec-unpacker.py     retdec-bin2llvmir retdec-decompiler.py`
`retdec-idb2pat         retdec-signature-from-library-creator.py`
`retdec-utils.py        retdec-bin2pat  retdec-fileinfo`
`retdec-llvmir2hll      retdec-stacofin retdec-yarac`

Username and Password for the Docker are: retdec/retdec

  [1]: https://github.com/avast/retdec
