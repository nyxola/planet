import sys
import os
import json
import numpy as np
from Task2 import prep_vec, apply_calibration
from osgeo import gdal, osr


# Initialising the calibration spacing and vector from the input json file
fn = sys.argv[1]
def initialise_info(filen):
    with open(filen, 'r') as f:
        data = f.read()
        obj = json.loads(data)
        calib_space = float(obj['calibration_info']['calibration_spacing'])
        calib_vec = np.array([float(x)
                              for x in obj['calibration_info']
                              ['calibration_vector']])
    return calib_space, calib_vec

# Initialising input matrix
M = [
    [7.10059172, 6.58436214, 6.12244898, 5.70749108, 5.33333333],
    [26.03550296, 24.14266118, 22.44897959, 20.9274673, 19.55555556],
    [73.37278107, 68.03840878, 63.26530612, 58.97740785, 55.11111111],
    [163.31360947, 151.44032922, 140.81632653, 131.27229489, 122.6666667],
    [2.36686391, 2.19478738, 2.04081633, 1.90249703, 1.77777778],
    [49.70414201, 46.09053498, 42.85714286, 39.95243757, 37.33333333]
]


# Run functions to produce the calibrated matrix, some functions are found
# within the __init__.py file which is used by the testing framework
calib_space, calib_vec = initialise_info(fn)
calib_vec_index = prep_vec(calib_space, calib_vec, M)
calib_matrix = apply_calibration(calib_vec_index, M)
calib_matrix = calib_matrix.astype('uint8')

print('Calibrated Matrix:')
print(calib_matrix)


# Writing out a matrix to an image requires three input matrices: an
# original array, and latitude and longitude for every pixel. As the calibrated
# matrix takes the form of the latitude, I am assuming to use this as lat while
# initialising an example array and longitude
array = np.array([
    [0.1, 0.3, 0.5, 0.7, 0.9],
    [0.2, 0.4, 0.6, 0.8, 1.0],
    [0.3, 0.5, 0.7, 0.9, 0.1],
    [0.4, 0.6, 0.8, 1.0, 0.2],
    [0.5, 0.7, 0.9, 0.1, 0.3],
    [0.6, 0.8, 1.0, 0.2, 0.4]
])
lat = calib_matrix
lon = np.array([
    [20.0, 15.0, 25.0, 18.0, 22.0],
    [20.0, 15.0, 25.0, 18.0, 22.0],
    [20.0, 15.0, 25.0, 18.0, 22.0],
    [20.0, 15.0, 25.0, 18.0, 22.0],
    [20.0, 15.0, 25.0, 18.0, 22.0],
    [20.0, 15.0, 25.0, 18.0, 22.0]
])

# Calculating needed variables to perform image transformation
xmin, ymin, xmax, ymax = [lon.min(), lat.min(), lon.max(), lat.max()]
nrows, ncols = np.shape(array)
xres = (xmax-xmin)/float(ncols)
yres = (ymax-ymin)/float(nrows)

# Setting geotransform (top left x, west-east pixel resolution, rotation
# (0 if North is up), top left y, rotation (0 if North is up), north-south pixel
# resolution)
geotransform = [xmin, xres, 0, ymax, 0, -yres]

# Create a file and specify the co-ordinates based on the geotransform
outpath = "./outputs"
raster = gdal.GetDriverByName('GTiff').Create(
    os.path.join(outpath, "rasterimage.tiff"),
    ncols, nrows, 1, gdal.GDT_Float32)
raster.SetGeoTransform(geotransform)

# Specify the co-oridinate encoding
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

# Export co-ordinate system to file and write it to the raster
raster.SetProjection(srs.ExportToWkt())
raster.GetRasterBand(1).WriteArray(array)

print('Image written to ', os.path.join(outpath, "rasterimage.tiff"))
