import pandas as pd
import numpy as np
import logging
import pandas as pd
from .filepaths import full_dataset_filepath
from .canadas_coordinates import *
from .dataset_columns import *
from .polygon_grid import PolygonGrid
import datetime

class Data():
	def __init__(self):
		self.dataset = pd.read_csv(full_dataset_filepath, header=0)
		self.polygon_grid = PolygonGrid()
		self.X_test = self.create_empty_df()

	def create_empty_df(self):
		print(f"Creating the DataFrame X_test...", flush=True)
		cols = self.dataset.columns.tolist()
		# Drop the vessels_count column as it corresponds to the target column
		cols.remove('vessel_count')
		df = pd.DataFrame(columns=cols)
		
		# Set the default values in the polygon i.e polygon id, latitude and longitude
		for index, polygon in enumerate(self.polygon_grid.polygons):
			id = polygon['polygon_id']
			lat = polygon['bottom_edge']
			lon = polygon['left_edge']
			df.loc[index] = [0, 0, id, lat, lon]
		print(f"End time: {datetime.datetime.now()}")
		return df

	def update_df_with_user_input(self, user_input):
		self.X_test['year'] = user_input.year
		self.X_test['week'] = user_input.week



