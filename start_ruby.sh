#!/bin/bash

source /etc/profile.d/rvm.sh
cd /home/toor/workspace/wpscan
./wpscan.rb -t 20 --batch  --follow-redirection -c /home/toor/workspace/wpscan/conf.json  --url $1
