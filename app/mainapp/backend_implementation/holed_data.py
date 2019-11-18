import pandas as pd
import numpy as np
import logging
from .data import Data
from .filepaths import holed_dataset_filepath
from .canadas_coordinates import *
from .dataset_columns import holed_dataset_site_names

class HoledData(Data):
	def __init__(self):
		Data.__init__(self)

		# Load the holed_dataset csv file into a DataFrame and retain data only from the relevant columns
		self.dataset_df = pd.read_csv(holed_dataset_filepath)
		self.sites = holed_dataset_site_names
		
		# Retain data from the required columns only
		self.df = self.dataset_df[holed_dataset_site_names]
		#self.holed_data_target = self.holed_data[target_columns]
		self.longitudes = []
		self.latitudes = []
		for site in holed_dataset_site_names:
			self.longitudes.append(self.dataset_df[site + '_lon'][0])
			self.latitudes.append(self.dataset_df[site + '_lat'][0])

	def get_index_of_timestamp(self, timestamp):
		try:
			index = self.dataset_df.index[self.dataset_df['DD-HH'] == timestamp].to_list()[0]
		except:
			print(f"The timestamp {timestamp} is not present in the holed dataset. Instead, fetching the index for the timestamp 01-01")
			index = self.dataset_df.index[self.dataset_df['DD-HH'] == "01-01"].to_list()[0]
		print(f"holed data index is: {index}", flush=True)
		return index	