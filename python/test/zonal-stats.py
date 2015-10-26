#!/usr/bin/python

from rasterstats import zonal_stats

points='/data/lapig/GEO/SHP/Mapa_sintese_pastagem_BR_pontos.shp'
image='/data/lapig/GEO/GARSECT2/pastagem-mt-nodata_b2.tif'

stats = zonal_stats(points, image, stats=['max'])

p={}

print('comecou')

for f in stats:
	value=f['max']
	if value in p:
		p[value] += 1
	else:
		p[value] = 1

print(p);