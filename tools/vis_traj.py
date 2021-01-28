"""
Visualize the trajectory using yaw, pitch and roll

"""

# -- python --
import glob
import exiftool
import numpy as np
import matplotlib.pyplot as plt
from easydict import EasyDict as edict

# -- project imports --

def main():
    files = []
    img_dir_path = "./data/NEPAC_L4_170801_200ft/*.JPG"
    for filename in glob.glob(img_dir_path):
        files.append(filename)
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(files)

    keys = edict()
    keys.name = ['File:FileName']
    keys.date = ['EXIF:CreateDate']
    keys.gps = ['EXIF:GPSLatitude','EXIF:GPSLongitude']
    keys.gps_ref = ['EXIF:GPSLatitudeRef','EXIF:GPSLongitudeRef']
    keys.gimball_pos = ['XMP:GimbalPitchDegree','XMP:GimbalRollDegree','XMP:GimbalYawDegree']
    keys.flight_pos = ['XMP:FlightPitchDegree','XMP:FlightRollDegree','XMP:FlightYawDegree']
    keys.camera_pos = ['MakerNotes:CameraPitch','MakerNotes:CameraRoll','MakerNotes:CameraYaw']
    vals = edict()
    vals.name,vals.date,vals.gps,vals.gps_ref = [],[],[],[]
    vals.gimball_pos,vals.flight_pos,vals.camera_pos = [],[],[]
    for d in metadata:
        vals.name.append([ d[k] for k in keys.name][0])
        vals.date.append(d[keys.date[0]])
        vals.gps.append([ d[k] for k in keys.gps])
        vals.gps_ref.append([ d[k] for k in keys.gps_ref])
        vals.gimball_pos.append([ d[k] for k in keys.gimball_pos])
        vals.flight_pos.append([ d[k] for k in keys.flight_pos])
        vals.camera_pos.append([ d[k] for k in keys.camera_pos])

    # -- numpify --
    for field in vals.keys():
        if field == "name": continue
        vals[field] = np.array(vals[field])

    # -- sort fields --
    indices = np.argsort(vals.date)
    for field in vals.keys():
        if field == "name": continue
        vals[field] = vals[field][indices]
    
    # -- translate gps to crs --

    # -- plot path --
    print(vals.gps)
    plt.plot(vals.gps[:,0],vals.gps[:,1])
    plt.savefig("./output/gps_traj.png")

if __name__ == "__main__":
    print("HI")
    main()
