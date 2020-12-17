
# -- python imports --
import numpy as np
import pandas as pd
import geopandas as gpd
from easydict import EasyDict as edict
from shapely.geometry import Point,Polygon

# -- project imports --
from .utm import project

def load_image_coordinates(image_info):
    lat,lon = image_info['Latitude'].to_numpy(),image_info['Longitude'].to_numpy()    
    geom = [Point([lon_i,lat_i,0]) for lat_i,lon_i in zip(lat,lon)]
    geo_df = gpd.GeoDataFrame(crs = 'EPSG:4326', # this is your coordinate system
                              geometry = geom)
    geo_df = geo_df.to_crs('EPSG:32616')
    coords = geo_df['geometry'].to_numpy()
    coords = np.array([[np.array(p.x),np.array(p.y)] for p in coords])
    return coords

def project_sampling_areas(sampling_areas):
    polygons = sampling_areas['geometry']
    projs = []
    for poly in polygons:
        lon,lat = poly.boundary.xy
        lat,lon = np.array(lat),np.array(lon)
        coords = np.c_[lat,lon]
        new_coords = []
        for p in coords:
            z,l,x,y = project(p)
            new_coords.append((x,y,0))
        proj_poly = Polygon(new_coords)
        projs.append(proj_poly)
    projs = pd.DataFrame({'proj_geometry':projs})
    return projs

def project_gps(info):
    lat,lon = info['Latitude'].to_numpy(),info['Longitude'].to_numpy()    
    coords = np.c_[lat,lon]
    proj = edict()
    proj.z,proj.l,proj.x,proj.y = [],[],[],[]
    for p in coords: 
        z,l,x,y = project(p)
        proj.z.append(z),proj.l.append(l),proj.x.append(x),proj.y.append(y)
    proj = pd.DataFrame(proj)
    return proj

