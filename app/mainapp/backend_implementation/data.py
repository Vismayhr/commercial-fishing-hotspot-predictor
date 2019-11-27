import pandas as pd
import numpy as np
import logging
import pandas as pd
from .filepaths import *
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
		filepath = vessel_count_monthly_averages_filepath + str(year) + vessel_count_average_file_extension
		vessel_count_monthly_averages = pickle.load(open(filepath, 'rb'))
		response = {}
		response['year'] = year
		response['week'] = week
		response['result'] = []
		all_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
		start_time = datetime.datetime.now()
		print(f"Querying data for each polygon on the map...", flush=True)
		for polygon in self.polygon_grid.polygons:
			data = {}
			data['lat1'] = float(polygon['bottom_edge'])
			print(f"data[lat1] is of type {type(data['lat1'])}",flush=True)
			data['lon1'] = float(polygon['left_edge'])

			data['lat2'] = float(polygon['bottom_edge'])
			data['lon2'] = float(polygon['right_edge'])

			data['lat3'] = float(polygon['top_edge'])
			data['lon3'] = float(polygon['right_edge'])

			data['lat4'] = float(polygon['top_edge'])
			data['lon4'] = float(polygon['left_edge'])

			if (polygon['polygon_id'] in self.unvisited_polygons):
				data['value'] = 0
				for m in all_months:
					data[m] = 0
			else:
				row = query_result[query_result['polygon_id']==polygon['polygon_id']]
				data['value'] = int(round(row['vessel_count']))
				id = polygon['polygon_id']
				for m in all_months:
					data[m] = int(vessel_count_monthly_averages[id][m])

			response['result'].append(data)
		end_time = datetime.datetime.now()
		print(f"Serving {row['polygon_id']} polygons took {(end_time - start_time).total_seconds()} seconds...", flush=True)
		return response