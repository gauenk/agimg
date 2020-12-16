
# -- python imports --
import ast
import exifread
import numpy as np



def np_divide_ignore(num,den):
    with np.errstate(divide='ignore',invalid='ignore'):
        result = np.true_divide(num,den)
        result[result == np.inf] = 0
        result = np.nan_to_num(result)
    return result
        

def get_xyz(img_path):
    with open(img_path,'rb') as f:
        tags = exifread.process_file(f)
    for tag in tags.keys():
        if 'GPS GPSLatitude' == tag:
            print("Key: %s, value %s" % (tag, tags[tag]))
            print(type(tags[tag]))
            a = ast.literal_eval(str(tags[tag]))
            print(a,type(a))
        elif 'GPS GPSLongitude' == tag:
            print("Key: %s, value %s" % (tag, tags[tag]))
        # if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        #     print("Key: %s, value %s" % (tag, tags[tag]))


