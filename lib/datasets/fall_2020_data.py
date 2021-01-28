

# -- python --
import glob
import numpy as np
import geopandas as gpd
from pathlib import Path
from easydict import EasyDict as edict
from shapely.geometry import Point,Polygon


def load_plot_layout(root):
    path = root / Path("./plot_layer/Simpson_plots_2019.shp")
    plot_layout = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return plot_layout    

def load_jpg_filenames(root=Path("./data")):
    root = root / Path("./NEPAC_L4_170801_200ft/")
    path = root / Path("./*JPG")
    filenames = list(glob.glob(str(path)))
    return filenames

def load_large_tif_filename(root=Path("./data")):
    filename = root / Path("./400ft7575NSRGB190712a_Orthomosaic_export_MonNov02172531071557.tif")
    return filename

def load_sampling_areas(root):
    path = root / Path("./sampling_areas/Sampling_areas_test.shp")
    sampling_areas = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return sampling_areas


def find_reference_point(plot_layout):
    max_lat,min_lat,max_lon,min_lon = -np.inf,np.inf,-np.inf,np.inf
    for region in plot_layout['geometry']:
        lon,lat = np.array(region.boundary.xy,dtype=np.float64)
        prop_max_lat = lat.max()
        prop_min_lat = lat.min()
        prop_max_lon = lon.max()
        prop_min_lon = lon.min()
        if prop_max_lat > max_lat: max_lat = prop_max_lat
        if prop_min_lat < min_lat: min_lat = prop_min_lat
        if prop_max_lon > max_lon: max_lon = prop_max_lon
        if prop_min_lon < min_lon: min_lon = prop_min_lon
    ref = edict()
    ref.max_lat,ref.min_lat,ref.max_lon,ref.min_lon = max_lat,min_lat,max_lon,min_lon
    return ref

def normalize_to_reference(geom,ref,pixel_scale):
    nmlz_geom = []
    lat_delta,lon_delta = ref.max_lat - ref.min_lat, ref.max_lon - ref.min_lon
    for poly in geom:
        lon,lat = np.array(poly.boundary.xy,dtype=np.float64)
        z = np.zeros(lon.shape[0])
        lat -= ref.max_lat
        lon -= ref.min_lon
        # lat *= 14961.
        # lon *= 22530.
        # lat /= lat_delta
        # lon /= lon_delta
        # lat /= (22530. / lat_delta)
        # lon /= (14961. / lon_delta)
        nmlz_poly = Polygon(np.c_[lon,lat,z])
        nmlz_geom.append(nmlz_poly)
    # nmlz_geom = pd.Series(nmlz_geom)
    return nmlz_geom
