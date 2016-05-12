#!/bin/bash

source /usr/local/rvm/scripts/rvm
/etc/init.d/postgresql start
/opt/msf/msfupdate --git-branch master
/bin/bash -c "cd /tmp/data && bash"
