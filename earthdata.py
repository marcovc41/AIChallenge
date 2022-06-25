import ee
import numpy
from matplotlib import pyplot as plot


def plot_map(data, rows, columns):
    if data is not None and rows > 0 and columns > 0 and rows is not None and columns is not None:
        matrix = data.reshape(rows, columns)
        plot.imshow(matrix, interpolation='nearest')
        plot.show


class EarthData:
    def __init__(self):
        """
        Initialize Google Earth Engine and populate credentials.
        """
        ee.Initialize()
        self.dataset = None
        self.band = []

    def select_dataset(self, dataset_name, start_date, end_date, band):
        """
        Select specific Google Earth Engine dataset filtered by band, dates and sorted in time.

        :param dataset_name: Google Earth Dataset
        :param start_date: To filter dataset by start date (inclusive)
        :param end_date: To filter dataset by end date (exclusive)
        :param band: Band of image collection
        """

        dataset = ee.ImageCollection(dataset_name)  # Get image collection
        data_masked = dataset.select(band).filterDate(start_date, end_date).sort('time')  # Filter dataset
        self.dataset = data_masked
        self.band = band

    def get_dataset(self, lat, lon, dx, dy):
        """
        Return list of images from dataset, cropped to a rectangle shape specified by
        Latitude and Longitude earth coordinates and rectangle width and length.

        :pre: Requires to call select_dataset() first
        :param lat: Latitude coordinate of crop region center
        :param lon: Longitude location of crop region center
        :param dx: Rectangle length for cropping dataset
        :param dy: Rectangle width for cropping dataset
        :return: (list of dates, list of flatten matrices,
        """

        default_scale = 100  # default map scale to use
        point = ee.Geometry.Point(lon, lat)
        region = ee.Geometry.Rectangle(
            [lon - dx / 2, lat - dy / 2, lon + dx / 2, lat + dy / 2])  # (xmin, ymin, xmax, ymax)

        dataset_info = self.dataset.getRegion(point, default_scale).getInfo()  # Get dataset info

        dataset_inputs = []
        dataset_outputs = []
        if len(dataset_info) > 1:
            mask_index = dataset_info[0].index('id')
            for metadata in range(1, len(dataset_info)):
                date = dataset_info[metadata][mask_index].replace('_', '-')
                image = self.dataset.filterDate(date).first()
                matrix = image.sampleRectangle(region).get(self.band).getInfo()
                np_matrix = numpy.array(matrix)
                rows = np_matrix.shape[0]
                columns = np_matrix.shape[1]
                year = int(date.split("-")[0])
                dataset_inputs.append([year])
                dataset_outputs.append(np_matrix.flatten())
            return dataset_inputs, dataset_outputs, rows, columns

        return None, None, None, None
