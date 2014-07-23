#!/bin/bash

#echo $PWD
source /etc/profile.d/rvm.sh
cd ..
cd WhatWeb
./whatweb $1 -a=3
