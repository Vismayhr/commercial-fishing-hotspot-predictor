import pandas as pd
import numpy as np
import logging
from .filepaths import full_dataset_filepath, holed_dataset_filepath
from .canadas_coordinates import *
from .dataset_columns import *

class Data():
	def __init__(self):

		# Determine the number of points to calculate for and plot w.r.t longitudes & latitudes 
		# across Canada with a resolution of 0.5 degees (latitude and longitude)
		self.longitudnal_points = abs(western_most_longitude - eastern_most_longitude) * 2
		self.latitudnal_points = abs(southern_most_latitude - northern_most_latitude) * 2

		# Create grid maps of the coordinates with a resolution of 0.5 degrees 
		self.longitude_grid = np.linspace(western_most_longitude, eastern_most_longitude, self.longitudnal_points, endpoint=False)
		self.latitude_grid = np.linspace(southern_most_latitude, northern_most_latitude, self.latitudnal_points, endpoint=False)
