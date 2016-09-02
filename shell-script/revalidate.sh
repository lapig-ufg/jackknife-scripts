
for TRAINNING in $(echo R1 R5 R10 R15 R20 R25 R30 ); do
	for VALIDATION in $(echo 02 03 04 ); do
		for TILE in $(echo 228068); do
			echo "./classification.py -v $VALIDATION -t $TRAINNING --no-classify --no-download -i $TILE -vp 1000 --prefetched-shp-random-points --only-omission"
		done
	done
done