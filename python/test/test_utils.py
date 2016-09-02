#!/usr/bin/python

import datetime
import traceback
import shapefile

import ee
import ee.mapclient

from lapig.ee import utils

def lc8CountObservations(path, row):

	ee.Initialize();

	filter = ee.Filter.And( ee.Filter.eq('WRS_PATH', path), ee.Filter.eq('WRS_ROW', row) );

	lc8array = utils.imageCollection2Array('LANDSAT/LC8', '2013-04-01', '2015-03-31', filter);

	result = { 
		'path': path, 
		'row': row, 
		'scenes': {
			'total': 0, 
			'months': {
				'2013-04': 0,
				'2013-05': 0,
				'2013-06': 0,
				'2013-07': 0,
				'2013-08': 0,
				'2013-09': 0,
				'2013-10': 0,
				'2013-11': 0,
				'2013-12': 0,
				'2014-01': 0,
				'2014-02': 0,
				'2014-03': 0,
				'2014-04': 0,
				'2014-05': 0,
				'2014-06': 0,
				'2014-07': 0,
				'2014-08': 0,
				'2014-09': 0,
				'2014-10': 0,
				'2014-11': 0,
				'2014-12': 0,
				'2015-01': 0,
				'2015-02': 0,
				'2015-03': 0
			}
		},
		'cloudCover': {
			'total':0,
			'months': {
					'2013-04': 0,
					'2013-05': 0,
					'2013-06': 0,
					'2013-07': 0,
					'2013-08': 0,
					'2013-09': 0,
					'2013-10': 0,
					'2013-11': 0,
					'2013-12': 0,
					'2014-01': 0,
					'2014-02': 0,
					'2014-03': 0,
					'2014-04': 0,
					'2014-05': 0,
					'2014-06': 0,
					'2014-07': 0,
					'2014-08': 0,
					'2014-09': 0,
					'2014-10': 0,
					'2014-11': 0,
					'2014-12': 0,
					'2015-01': 0,
					'2015-02': 0,
					'2015-03': 0
			},
			'days': {}
		}
	}

	print(len(lc8array))

	for i, lc8 in enumerate(lc8array):

		while True:
			try:
				img = lc8['img'];
				imgTime = img.get('system:time_start').getInfo();
				dt = datetime.datetime.utcfromtimestamp(imgTime/1000);
				month = str(dt.strftime('%Y-%m'));
				day = str(dt.strftime('%Y-%m-%d'));

				cloudCover = img.get('CLOUD_COVER').getInfo();
				break;

			except:
				print('error',i);
				traceback.print_exc();

		print(i, cloudCover, month, day);

		if month not in result['scenes']['months']:
			result['scenes']['months'][month] = 0;
			result['cloudCover']['months'][month] = 0;

		result['scenes']['months'][month] += 1;
		result['scenes']['total'] += 1;

		result['cloudCover']['total'] += cloudCover
		result['cloudCover']['days'][day] = cloudCover;
		result['cloudCover']['months'][month] += cloudCover

	if(result['scenes']['total'] > 0):
		result['cloudCover']['total'] = result['cloudCover']['total'] / result['scenes']['total'];

	for month in result['cloudCover']['months']:
		if result['scenes']['months'][month] > 0:
			result['cloudCover']['months'][month] = result['cloudCover']['months'][month] / result['scenes']['months'][month]

	return result;

input2="/data/lapig/GEO/SHP/Cenas_Landsat_BR.shp"
#input2="/data/lapig/GEO/SHP/MT/pa_br_landsat_norte_mt.shp"
output="./lc8_scenes"

sf = shapefile.Reader(input2);
wf = shapefile.Writer(shapefile.POLYGON);

wf.field('path', 'N');
wf.field('row', 'N');

wf.field('sce_total', 'N');
wf.field('sce_201304', 'N');
wf.field('sce_201305', 'N');
wf.field('sce_201306', 'N');
wf.field('sce_201307', 'N');
wf.field('sce_201308', 'N');
wf.field('sce_201309', 'N');
wf.field('sce_201310', 'N');
wf.field('sce_201311', 'N');
wf.field('sce_201312', 'N');
wf.field('sce_201401', 'N');
wf.field('sce_201402', 'N');
wf.field('sce_201403', 'N');
wf.field('sce_201404', 'N');
wf.field('sce_201405', 'N');
wf.field('sce_201406', 'N');
wf.field('sce_201407', 'N');
wf.field('sce_201408', 'N');
wf.field('sce_201409', 'N');
wf.field('sce_201410', 'N');
wf.field('sce_201411', 'N');
wf.field('sce_201412', 'N');
wf.field('sce_201501', 'N');
wf.field('sce_201502', 'N');
wf.field('sce_201503', 'N');
wf.field('clo_total', 'N', 19, 11);
wf.field('clo_201304', 'N', 19, 11);
wf.field('clo_201305', 'N', 19, 11);
wf.field('clo_201306', 'N', 19, 11);
wf.field('clo_201307', 'N', 19, 11);
wf.field('clo_201308', 'N', 19, 11);
wf.field('clo_201309', 'N', 19, 11);
wf.field('clo_201310', 'N', 19, 11);
wf.field('clo_201311', 'N', 19, 11);
wf.field('clo_201312', 'N', 19, 11);
wf.field('clo_201401', 'N', 19, 11);
wf.field('clo_201402', 'N', 19, 11);
wf.field('clo_201403', 'N', 19, 11);
wf.field('clo_201404', 'N', 19, 11);
wf.field('clo_201405', 'N', 19, 11);
wf.field('clo_201406', 'N', 19, 11);
wf.field('clo_201407', 'N', 19, 11);
wf.field('clo_201408', 'N', 19, 11);
wf.field('clo_201409', 'N', 19, 11);
wf.field('clo_201410', 'N', 19, 11);
wf.field('clo_201411', 'N', 19, 11);
wf.field('clo_201412', 'N', 19, 11);
wf.field('clo_201501', 'N', 19, 11);
wf.field('clo_201502', 'N', 19, 11);
wf.field('clo_201503', 'N', 19, 11);

#result = lc8CountObservations(232, 69)

for rec in sf.shapeRecords():
	rowPath = rec.record[2];
	split = rowPath.split('/');

	path = int(split[0])
	row = int(split[1])
	
	print(row, path);
	
	result = lc8CountObservations(path, row)
	
	wf.poly([rec.shape.points]);
	wf.record(path, row, \
		result['scenes']['total'], \
		result['scenes']['months']['2013-04'], \
		result['scenes']['months']['2013-05'], \
		result['scenes']['months']['2013-06'], \
		result['scenes']['months']['2013-07'], \
		result['scenes']['months']['2013-08'], \
		result['scenes']['months']['2013-09'], \
		result['scenes']['months']['2013-10'], \
		result['scenes']['months']['2013-11'], \
		result['scenes']['months']['2013-12'], \
		result['scenes']['months']['2014-01'], \
		result['scenes']['months']['2014-02'], \
		result['scenes']['months']['2014-03'], \
		result['scenes']['months']['2014-04'], \
		result['scenes']['months']['2014-05'], \
		result['scenes']['months']['2014-06'], \
		result['scenes']['months']['2014-07'], \
		result['scenes']['months']['2014-08'], \
		result['scenes']['months']['2014-09'], \
		result['scenes']['months']['2014-10'], \
		result['scenes']['months']['2014-11'], \
		result['scenes']['months']['2014-12'], \
		result['scenes']['months']['2015-01'], \
		result['scenes']['months']['2015-02'], \
		result['scenes']['months']['2015-03'], \
		result['cloudCover']['total'], \
		result['cloudCover']['months']['2013-04'], \
		result['cloudCover']['months']['2013-05'], \
		result['cloudCover']['months']['2013-06'], \
		result['cloudCover']['months']['2013-07'], \
		result['cloudCover']['months']['2013-08'], \
		result['cloudCover']['months']['2013-09'], \
		result['cloudCover']['months']['2013-10'], \
		result['cloudCover']['months']['2013-11'], \
		result['cloudCover']['months']['2013-12'], \
		result['cloudCover']['months']['2014-01'], \
		result['cloudCover']['months']['2014-02'], \
		result['cloudCover']['months']['2014-03'], \
		result['cloudCover']['months']['2014-04'], \
		result['cloudCover']['months']['2014-05'], \
		result['cloudCover']['months']['2014-06'], \
		result['cloudCover']['months']['2014-07'], \
		result['cloudCover']['months']['2014-08'], \
		result['cloudCover']['months']['2014-09'], \
		result['cloudCover']['months']['2014-10'], \
		result['cloudCover']['months']['2014-11'], \
		result['cloudCover']['months']['2014-12'], \
		result['cloudCover']['months']['2015-01'], \
		result['cloudCover']['months']['2015-02'], \
		result['cloudCover']['months']['2015-03']  \
	);

wf.save(output)