# -- python imports --
from PIL import Image
from pathlib import Path
import numpy as np
import geopandas as gpd
from shapely.geometry import Point,Polygon
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto

# -- project imports --
import _init_paths
from pyutils.vgi import *
from pyutils.projections import project_sampling_areas

def load_plot_layout(root):
    fn = Path("Simpson_plots_2019.shp")
    path = root / fn
    plot_layout = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return plot_layout    

def load_sampling_areas(root):
    fn = Path("Sampling_areas_test.shp")
    path = root / fn
    sampling_areas = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return sampling_areas

def gps_to_crs(gps_coord,crs):
    # keys = ["Longitude","Latitude","Alititude"]
    keys = ["Longitude","Latitude"]
    point = Point([gps_coord[k] for k in keys])
    gps_coord = gpd.GeoDataFrame({'col1': ['name'], 'geometry':[point]})    
    gps_coord = gps_coord.set_crs("EPSG:4326")
    gps_coord = gps_coord.to_crs(crs)
    gps_coord = np.squeeze(np.array(gps_coord['geometry'][0].xy))
    return gps_coord

def main():

    # -- plot layouts --
    root = Path("./data/plot_layer/")
    plot_layout = load_plot_layout(root)
    plot_layout = plot_layout.to_crs('EPSG:32616')

    # -- sampling area layer --
    root = Path("./data/sampling_areas/")
    sampling_areas = load_sampling_areas(root)
    sampling_areas = sampling_areas.to_crs('EPSG:32616')

    # -- load example image --
    img_path = "./data/NEPAC_L4_170801_200ft/DJI_1930.JPG"
    gps_coord = gpsphoto.getGPSData(img_path)
    gps_coord = gps_to_crs(gps_coord,'EPSG:32616')
    raw_img = np.array(Image.open(img_path))
    print("Image at {}".format(gps_coord))

    # -- plot sampling area and plot layout --
    fig,ax = plt.subplots(figsize=(8,8))
    plot_layout.plot(ax=ax,alpha=0.5)
    sampling_areas.plot(column='Sarea_ID',ax=ax)
    plt.savefig("./output/sample_and_plot_layer_proj.png",transparent=True,bbox_inches='tight')
    plt.close("all")

    # -- plot --
    # fig,ax = plt.subplots(figsize=(8,8))
    # # sampling_areas['geometry'] = proj_sampling_areas['proj_geometry']
    # geo_df.plot(column='Sarea_ID',ax=ax)
    # plt.savefig("./sample_and_plot_layer_proj.png",
    #             transparent=False,bbox_inches='tight')

    # print(sampling_areas.columns)
    # print(sampling_areas['geometry'].iloc[0])

if __name__ == "__main__":
    main()

