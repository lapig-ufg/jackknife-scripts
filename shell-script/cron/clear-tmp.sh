#!/bin/bash

cd /data/lapig/TMP/
find -mindepth 1 -maxdepth 1 ! -newermt $(date -d 'last month' +'%Y/%m/%d') -delete
