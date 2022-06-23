import ee
import numpy
from matplotlib import pyplot as plot

# Authenticate in Google Earth Engine and verify if credentials are populated
ee.Authenticate()
ee.Initialize()

# Constant definitions
DATASET_NAME = 'MODIS/006/MOD44W'  # Name of dataset to extract water bodies information
STARTING_DATE = '2000-01-01'  # First element of the dataset
ENDING_DATE = '2015-05-01'  # Last element of the dataset
BAND = 'water_mask'  # Dataset band we are interested in

# User parameters
scale = 100  # Scale in meters
lat, lon = 20.24, -103.06  # Center coordinates
dx = 0.8  # Rectangle length
dy = 0.3  # Rectangle width

point = ee.Geometry.Point(lon, lat)
region = ee.Geometry.Rectangle([lon - dx/2, lat - dy/2, lon + dx/2, lat + dy/2])  # (xmin, ymin, xmax, ymax)

# Get dataset collection, filter by band and date, sort by time
dataset = ee.ImageCollection(DATASET_NAME)
waterMask = dataset.select(BAND).filterDate(STARTING_DATE, ENDING_DATE).sort('time')

# Get data of ImageCollection for the given region
image_data_list = waterMask.getRegion(point, scale).getInfo()

# Get list of ids
list_of_ids = []
if len(image_data_list) > 1:
    mask_index = image_data_list[0].index('id')
    for i in range(1, len(image_data_list)):
        date = image_data_list[i][mask_index].replace('_', '-')
        list_of_ids.append(date)
# print(list_of_ids)

# Get list of Image objects
list_of_images = []
for id in list_of_ids:
    list_of_images.append(waterMask.filterDate(id).first())
# print(list_of_images)

# Get list of image as Python matrices
list_of_matrices = []
for image in list_of_images:
    list_of_matrices.append(image.sampleRectangle(region).get(BAND).getInfo())
# print(list_of_matrices[0])

# Change Python Matrix to Numpy Matrix for visualization
list_of_nparray = []
for matrix in list_of_matrices:
    list_of_nparray.append(numpy.array(matrix))
# print("Number of matrices: " + str(len(list_of_nparray)))
# print("Shape of a first matrix: " + str(list_of_nparray[0].shape))

# Plot first matrix
plot.imshow(list_of_nparray[0], interpolation='nearest')
plot.show
