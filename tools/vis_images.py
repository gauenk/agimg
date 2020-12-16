# -- python imports --
import glob
from easydict import EasyDict as edict
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto
from shapely.geometry import Point,Polygon

# -- project imports --
import _init_paths
from pyutils.vgi import compute_vgi
from pyutils.misc import get_xyz
from pyutils.utm import project

def load_jpg_filenames():
    root = Path("./data/NEPAC_L4_170801_200ft/")
    path = root/Path("./*JPG")
    filenames = list(glob.glob(str(path)))
    return filenames


def load_sampling_areas(root):
    fn = Path("Sampling_areas_test.shp")
    path = root / fn
    sampling_areas = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return sampling_areas

def image_sampling_area_assignment(img_coords,sampling_polygons):
    # lat,lon = info['x'].to_numpy(),info['y'].to_numpy()
    # gps = [Point(lon_i,lat_i) for lon_i,lat_i in zip(lon,lat)]
    # polygons = sampling_areas['geometry']
    N,M = len(img_coords),len(sampling_polygons)
    dist_mat = np.zeros((N,M),dtype=np.bool)
    for i,point in enumerate(img_coords):
        for j,poly in enumerate(sampling_polygons):
            dist_mat[i,j] = Point(point).within(poly)
    print(dist_mat.sum())
    return dist_mat

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

def load_image_coordinates(image_info):
    lat,lon = image_info['Latitude'].to_numpy(),image_info['Longitude'].to_numpy()    
    geom = [Point([lon_i,lat_i,0]) for lat_i,lon_i in zip(lat,lon)]
    geo_df = gpd.GeoDataFrame(crs = 'EPSG:4326', # this is your coordinate system
                              geometry = geom)
    geo_df = geo_df.to_crs('EPSG:32616')
    coords = geo_df['geometry'].to_numpy()
    coords = np.array([[np.array(p.x),np.array(p.y)] for p in coords])
    return coords

def main():

    # -- get all filenames --
    filenames = load_jpg_filenames()    

    # -- gather gps data --
    img_path = "./data/NEPAC_L4_170801_200ft/DJI_1930.JPG"
    info = pd.DataFrame([gpsphoto.getGPSData(img_path) for img_path in filenames])
    info['img_path'] = filenames
    img_coords = load_image_coordinates(info) # project

    # # -- project gps data v2; old --
    # projected_info = project_gps(info)
    # info['x'] = projected_info['x']
    # info['y'] = projected_info['y']


    # # -- plot gps data; not equal axis --
    # gps = info.sort_values('Latitude')
    # fig,ax = plt.subplots(figsize=(8,8))
    # ax.plot(gps['Longitude'],gps['Latitude'],'+')
    # plt.savefig("./image_locations_gps_ax-neq.png",transparent=True,dpi=300,bbox_inches='tight')
    # plt.close("all")

    # # -- plot gps data --
    # gps = info.sort_values('Latitude')
    # fig,ax = plt.subplots(figsize=(8,8))
    # ax.axis('equal')
    # ax.plot(gps['Longitude'],gps['Latitude'],'+')
    # plt.savefig("./image_locations_gps.png",transparent=True,dpi=300,bbox_inches='tight')
    # plt.close("all")

    # # -- plot projected data; not equal axis --
    # fig,ax = plt.subplots(figsize=(8,8))
    # ax.axis('equal')
    # ax.plot(coords[:,0],coords[:,1],'+')
    # plt.savefig("./output/image_locations_proj.png",transparent=True,dpi=300,bbox_inches='tight')
    # plt.close("all")
    
    # # -- plot projected data --
    # fig,ax = plt.subplots(figsize=(8,8))
    # ax.axis('equal')
    # ax.plot(gps['y'],gps['x'],'+')
    # plt.savefig("./image_locations_proj.png",transparent=True,dpi=300,bbox_inches='tight')
    # plt.close("all")

    # -- gather flight and gimbal info --
    
    # -- load sampling areas
    root = Path("./data/sampling_areas/")
    sampling_areas = load_sampling_areas(root)
    sampling_areas = sampling_areas.to_crs('EPSG:32616')

    fig,ax = plt.subplots(figsize=(8,8),dpi=100)
    sampling_areas.plot(column='Sarea_ID',ax=ax)
    ax.plot([612873.327],[4390070.685],'+')
    ax.plot(img_coords[:,0],img_coords[:,1],'x')
    plt.savefig("./output/sampling_and_img_proj.png")
    print(sampling_areas['geometry'])

    # coord = sampling_areas['geometry'].iloc[0]
    # print(coord)

    # -- assign raw image to sampling area --
    distances = image_sampling_area_assignment(img_coords,sampling_areas['geometry'])
    print(distances.sum())


if __name__ == "__main__":
    main()
