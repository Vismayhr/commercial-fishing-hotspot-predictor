import pandas as pd
import numpy as np
import logging
import pandas as pd
from .filepaths import full_dataset_filepath, unvisited_polygons_data_filepath
from .canadas_coordinates import *
from .dataset_meta_data import *
from .polygon_grid import PolygonGrid
import datetime
import pickle

class Data():
	def __init__(self):
		self.dataset = pd.read_csv(full_dataset_filepath, header=0)
		self.polygon_grid = PolygonGrid()
		self.X_test = self.create_empty_df()
		self.unvisited_polygons = self.get_unvisited_polygon_data()
		print(f"Loaded the dataset and other required data...", flush=True)


	def create_empty_df(self):
		print(f"Creating an empty DataFrame to store the results...", flush=True)
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
		return df


	def update_df_with_user_input(self, user_input):
		self.X_test['year'] = str(user_input.year)
		self.X_test['week'] = float(user_input.week)


	def perform_feature_encoding(self):
		print(f"Repeating the feature engineering steps done on the train dataset...")
		# One Hot Encode the year values (2012 - 2017)
		self.one_hot_encode_year()

		# Do Sin, Cos encoding for week as it is a cyclic value
		max_week = 53
		self.encode_cyclic_values(max_week, 'week')


	def one_hot_encode_year(self):
		print(f"1) One hot encoding of year column", flush=True)
		# Create columns for the possible years
		for year in valid_years:
			if(year == self.X_test['year'][0]):
				self.X_test[year] = 1
			else:
				self.X_test[year] = 0


	def encode_cyclic_values(self, max_val, col_name):
		print(f"2) Sin and cos encoding for week values...", flush=True)

		# Sine transformation
		self.X_test['week_sin'] = np.sin(2 * np.pi * self.X_test['week'] / max_val)

	    # Cos transformation
		self.X_test['week_cos'] = np.cos(2 * np.pi * self.X_test['week'] / max_val)


	def get_unvisited_polygon_data(self):
		with open(unvisited_polygons_data_filepath, 'rb') as f:
			data = pickle.load(f)
		return(data)

	def query_for_past_date(self, year, week):
		query_result = self.dataset[(self.dataset['year']==year) & (self.dataset['week']==week)]
		response = {}
		response['year'] = year
		response['week'] = week
		response['result'] = []
		start_time = datetime.datetime.now()
		print(f"Querying data for each polygon on the map...", flush=True)
		for index, row in query_result.iterrows():
			data = {}
			data['lat1'] = row['polygon_south_latitude']
			data['lon1'] = row['polygon_west_longitude']

			data['lat2'] = row['polygon_south_latitude']
			data['lon2'] = row['polygon_west_longitude'] + 1.0

			data['lat3'] = row['polygon_south_latitude'] + 1.0
			data['lon3'] = row['polygon_west_longitude'] + 1.0

			data['lat4'] = row['polygon_south_latitude'] + 1.0
			data['lon4'] = row['polygon_west_longitude']

			if(row['polygon_id'] in self.unvisited_polygons):
				data['value'] = 0
				data['jan'] = 0
				data['apr'] = 0
				data['aug'] = 0
				data['dec'] = 0
			else:
				data['value'] = round(row['vessel_count'])
				data['jan'] = round(np.average(self.dataset[(self.dataset['year']==year) & (self.dataset['week'].between(1,4)) & (self.dataset['polygon_id']==row['polygon_id'])]['vessel_count']))
				data['apr'] = round(np.average(self.dataset[(self.dataset['year']==year) & (self.dataset['week'].between(13,16)) & (self.dataset['polygon_id']==row['polygon_id'])]['vessel_count']))
				data['aug'] = round(np.average(self.dataset[(self.dataset['year']==year) & (self.dataset['week'].between(29,32)) & (self.dataset['polygon_id']==row['polygon_id'])]['vessel_count']))
				data['dec'] = round(np.average(self.dataset[(self.dataset['year']==year) & (self.dataset['week'].between(49,53)) & (self.dataset['polygon_id']==row['polygon_id'])]['vessel_count']))

			response['result'].append(data)
		end_time = datetime.datetime.now()
		print(f"Serving {row['polygon_id']} polygons took {(end_time - start_time).total_seconds()} seconds...", flush=True)
		return response