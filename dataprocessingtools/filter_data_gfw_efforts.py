# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:53:32 2020

@author: s.paramonov
"""

# Python = 3.7

import os
import geopandas as gpd
import numpy as np

# Check path before starting code
fao_areas_dir = os.path.join('..','FAO','FAO_AREAS')
areas_filename = os.path.join(fao_areas_dir,'FAO_AREAS.shp')

from shapely.geometry import shape
from shapely.geometry import Point
import geojson
import pandas as pd

zones= gpd.GeoDataFrame.from_file(areas_filename)     

# Norway sea:
II = zones[(zones['F_SUBAREA'] == '27.2')  ]
watch_poly = II['geometry'].to_json()

pp = geojson.loads(watch_poly)

for feature in pp['features']:
    pg = shape(feature['geometry'])

iia1_bbox = pg.bounds

# template: 2012-01-01
# period = august
# data: 1/100 degree

datatype = 100
data_templ = 'daily-csvs-'+str(datatype)+'-v1'

daily_eff_dir = os.path.join('..','Data','gfs_activities','efforts',data_templ,'fishing_effort','daily_csvs')
filelist = os.listdir(daily_eff_dir)

years = ['2012','2013','2014','2015','2016']
test_year = years[4]
test_month = '08'
from datetime import date
daysofmonth =  (date(2012, 9, 1) - date(2012, 8, 1)).days

fishpoints = []
for yi in range (len(years)):
    year = years[yi]
    print(year)
    for i in range(daysofmonth):
        test_day = format((i+1), '02d')
        
        getday = year+'-'+test_month+'-'+test_day
        day_filename = os.path.join(daily_eff_dir,getday+'.csv')
        df = pd.read_csv(day_filename)
        lats = (df['lat_bin'].values)/100
        lons = (df['lon_bin'].values)/100
        lats = lats.tolist()
        lons = lons.tolist()
        pointscoords = list(zip(lats, lons))
        
    for pp in pointscoords:
        if (pg.contains(Point(pp))):
            fishpoints.append(pp)
    
print("totally fishing points in zone:",len(fishpoints))    
