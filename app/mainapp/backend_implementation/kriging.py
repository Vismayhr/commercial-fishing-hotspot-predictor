import pandas as pd
import numpy as np
import logging
import json
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
from .filepaths import full_dataset_filepath, holed_dataset_filepath
from .canadas_coordinates import *
from .dataset_columns import *
from backend_implementation.holed_data import HoledData
from backend_implementation.full_data import FullData

class Kriging():

	def __init__(self, index, data):
		self.moving_avg_size = 2
		self.sites_output_df = None
		self.data_moving_avg = self.calculate_moving_average(data)
		self.kriging_output  = self.perform_kriging(index, data)
		self.kriging_output_json = self.structure_output_as_json(self.kriging_output)

	def calculate_moving_average(self, data):
		# After experiementing with different sizes, it was found that using a moving  average over every 2 samples 
		# led to the best performing kriging model. Moving average: https://en.wikipedia.org/wiki/Moving_average
		return data.df.rolling(self.moving_avg_size).mean()

	def perform_kriging(self, index, data):
		current_date = str(data.dataset_df['DD-HH'][index]);

		# Since we are using a rolling average, the average of the first moving_avg_size - 1 rows will be NaN.
		# Hence, we use the first non-NaN row from the dataset to determine the magnetic field.
		if index < (self.moving_avg_size - 1):
			index = self.moving_avg_size - 1

		# Perform Ordinary Kriging: https://pykrige.readthedocs.io/en/latest/overview.html#ordinary-kriging-example
		OK = OrdinaryKriging(data.longitudes, data.latitudes, data.df.loc[index], variogram_model='spherical', 
			verbose=False, enable_plotting=False, coordinates_type='geographic')
		z1, ss1 = OK.execute('grid', data.longitude_grid, data.latitude_grid)

		# These values are the indinces (long,lat) which correspond to the magnetic field reading at the site MEA
		index_of_mea_longitude = np.where(data.longitude_grid == mea_longitude)[0][0]
		index_of_mea_latitude = np.where(data.latitude_grid == mea_latitude)[0][0]

		# z1 is a masked array of size len(latitude_grid) x len(longitude_grid) containing the interpolated values.
		# Hence, we access the value at MEA's coordinates as z1[lat][long] instead of z1[long][lat].
		predicted_value = round(z1.data[index_of_mea_latitude][index_of_mea_longitude], 2)

		if isinstance(data, FullData):
			self.sites_output_df = self.build_sites_output_dataframe(index, data, full_dataset_site_names, predicted_value)
			target_value = data.target.loc[index]['MEA']
		else:
			self.sites_output_df = self.build_sites_output_dataframe(index, data, holed_dataset_site_names, predicted_value)
			target_value = r'N/A'

		# Return z1.data, sites_output_df, predicted value and target_value as a dictionary. This information will
		# be passed onto the user's browser, where is will be used to visualise the data on maps.
		return_values = {}
		return_values['prediction_grid'] = z1.data
		return_values['sites_output_df'] = self.sites_output_df
		return_values['predicted_value'] = predicted_value
		return_values['target_value'] = target_value
		return_values['current_date'] = current_date
		return return_values


	def build_sites_output_dataframe(self, index, data, sites, predicted_value):
		sites_df = pd.DataFrame(columns=['site_name', 'magnetic_field_variation', 'longitude', 'latitude'])

		# Create a dataframe containing information about each site and it's magnetic field variation value
		# on the given DD-HH. This information will be visualised on a map in the browser window.
		for site in sites:
			name = site
			value = data.dataset_df[site][index]
			longitude = data.dataset_df[site + "_lon"][index]
			latitude = data.dataset_df[site + "_lat"][index]
			sites_df = sites_df.append(pd.Series([name, value, longitude, latitude], index=sites_df.columns), ignore_index=True)

		# Explicitly add a row for the MEA site as the column has been removed/is unavailable in the datasets
		name = target_columns[0] # MEA
		value = predicted_value
		longitude = mea_longitude
		latitude = mea_latitude
		sites_df = sites_df.append(pd.Series([name, value, longitude, latitude], index=sites_df.columns), ignore_index=True)
		return sites_df

	def structure_output_as_json(self, kriging_output):
		json_response_obj = {}

		# dict object containing magnetic field variation values of the MEA site
		target_site_dict = {
		r'site': target_columns[0], 
		r'predicted_value': kriging_output['predicted_value'], 
		r'target_value': kriging_output['target_value']
		}

		# dict object containing information about all sites
		sites_data = []
		sites_df = kriging_output['sites_output_df']
		for index, row in sites_df.iterrows():
			site = {}
			site[r'name'] = row['site_name']
			site[r'value'] = row['magnetic_field_variation']
			site[r'lon'] = row['longitude']
			site[r'lat'] = row['latitude']
			sites_data.append(site)
		

		# dict containing information about all coordinates from the grid spanning across Canada
		grid = kriging_output['prediction_grid']
		latitude = southern_most_latitude
		longitude = western_most_longitude
		across_canada_data = []
		for row in grid:
			for value in row:
				location_dict = {}
				location_dict[r'lon'] = longitude
				location_dict[r'lat'] = latitude
				location_dict[r'value'] = round(value, 2)
				across_canada_data.append(location_dict)
				longitude = longitude + 0.5
			longitude = western_most_longitude
			latitude = latitude + 0.5

		# dict containing the dimensions of the sites_output_df.
		# This is used to determine the boundaries of polygons in the heat map.
		grid_dimensions = {'rows': kriging_output['prediction_grid'].shape[0], 'columns': kriging_output['prediction_grid'].shape[1]}
		
		# Generate a dict consisting of the above 3 JSON objects and return it to the browser.
		json_response_obj['current_date'] = kriging_output['current_date']
		json_response_obj[r'target_site'] = target_site_dict
		json_response_obj[r'sites_data'] = sites_data
		json_response_obj[r'across_canada_data'] = across_canada_data
		json_response_obj[r'grid_dimensions'] = grid_dimensions

		# Don't do a json.dumps() here because it leads to escape characters being inserted when the 
		# objects is unpacked as a JSON object in Jinja2 template using the 'tojson' method. Hence,
		# pass it to the browser as a mapping (i.e dict obj) and unpack it as a JSON directly.
		return json_response_obj
