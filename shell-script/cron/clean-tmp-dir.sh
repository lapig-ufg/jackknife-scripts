#!/bin/bash

MAX_DAYS=7
TMP_DIR='/data/TEMP'

cd $TMP_DIR
find -name '*' -type f -ctime 7 -exec ls "{}" \;
find -depth -type d -empty -delete