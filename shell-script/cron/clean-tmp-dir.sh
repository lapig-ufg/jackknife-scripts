#!/bin/bash

MAX_DAYS=30
TMP_DIR='/data/lapig/TMP'

cd $TMP_DIR
find -name '*' -ctime +$MAX_DAYS -exec ls "{}" \;
find -name '*' -type d -depth -empty -exec ls "{}" \; #rmdir