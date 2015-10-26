#!/bin/bash

#parallel -a 01-generate-points.sh
./02-classify.sh
./03-convert.sh
./04-merge-classify.sh
./06-validate.sh