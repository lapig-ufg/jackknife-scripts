#!/bin/bash

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

bricks=( )

for b in "${bricks[@]}"; do

	echo "Clear $b"

	setfattr -x trusted.glusterfs.volume-id $b &> /dev/null
	setfattr -x trusted.gfid $b  &> /dev/null
	rm -rf $b/.glusterfs  &> /dev/null
done