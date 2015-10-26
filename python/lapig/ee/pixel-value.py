import ee

ee.Initialize();

longitude = -55.43
latitude = -18.23
date1 = '1985-01-01' 
date2 = '1995-01-01'
pixelResolution = 30
collectionId = "LT5_L1T_SR";
expresion = "(b('B4') - b('B3')) / (b('B4') + b('B3'))"

def calculateIndex(image):
  return image.expression(expresion);

point = ee.Geometry.Point([longitude, latitude]);
timeSeries = ee.ImageCollection(collectionId).filterDate(date1, date2).map(calculateIndex);
result = timeSeries.getRegion(point,pixelResolution).getInfo();

for r in result:
	print(r[0], r[4])