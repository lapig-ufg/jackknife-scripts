#!/bin/bash

dbPath=$1
tableName=$2

echo " \
BEGIN;
ALTER TABLE $tableName ADD COLUMN \"bbox\" char(255); \
UPDATE $tableName SET bbox = ( \
	SELECT ST_MinX(cities.geometry) || ',' || ST_MinY(cities.geometry) || ',' || ST_MaxX(cities.geometry) || ',' || ST_MaxY(cities.geometry) \
	FROM cities \
	WHERE cities.COD_MUN = $tableName.COD_MUN); \
CREATE INDEX "$tableName"_nm_uf ON $tableName(NM_UF);
COMMIT; \
" | spatialite $dbPath