#!/bin/bash

REDIS='redis-cli --raw -h su-redis'

SCRIPT_NAME=$(basename $0)
MODIS_TILES='h13v11,h12v08,h14v09,h14v10,h13v12,h10v08,h10v09,H10V10,h11v08,h11v09,h11v10,h12v11,h13v08,h12v09,h12v10,h14v11,h13v09,h13v10'
MODIS_DIR='/data/lapig/GEO/MODIS'

SCRIPT_START_DATE='2000-02-01'

DATE_FORMAT='%Y-%m-%d'

function get_params() {
	
	while getopts $SCRIPT_OPTS opt; do
		if [ $opt = '?' ]; then 
			echo "Invalid option -$OPTARG"
			exit
		else
			eval "$opt=$OPTARG" &> /dev/null
		fi
	done

}

SCRIPT_OPTS=":p:d:"
get_params $@

if [ "$p" = '' ]; then
	echo 'The option -p is mandatory'
	exit
else
	MODIS_PRODUCT=$p
fi

if [ "$d" = '' ]; then
	REDIS_KEY="$SCRIPT_NAME::$MODIS_PRODUCT"
	#$REDIS DEL $REDIS_KEY # Delete Key

	if [ "$($REDIS EXISTS $REDIS_KEY)" = '1' ]; then
		SCRIPT_START_DATE=$($REDIS GET $REDIS_KEY)
	fi

	NEXT_MONTH_DATE=$(date -d "$SCRIPT_START_DATE+1 month" +$DATE_FORMAT)
	SCRIPT_END_DATE=$(date -d "$NEXT_MONTH_DATE-1 day" +$DATE_FORMAT)
	$REDIS SET $REDIS_KEY $NEXT_MONTH_DATE &> /dev/null
else
	SCRIPT_START_DATE="$d"
	SCRIPT_END_DATE=$(date -d "$(date -d "$SCRIPT_START_DATE+1 month" +$DATE_FORMAT)-1 day" +$DATE_FORMAT)
fi

SCRIPT_DIR=$MODIS_DIR/$MODIS_PRODUCT/$(date -d "$SCRIPT_START_DATE" +'%Y-%m')

mkdir -p $SCRIPT_DIR
modis_download.py -x -f $SCRIPT_END_DATE -e $SCRIPT_START_DATE -p $MODIS_PRODUCT -t $MODIS_TILES $SCRIPT_DIR

if [ "$d" = '' ] && [ $(date -d $SCRIPT_END_DATE +'%y%m%d') -le $(date +'%y%m%d')  ]; then
	nohup download-modis.sh $@ >& /dev/null &
fi