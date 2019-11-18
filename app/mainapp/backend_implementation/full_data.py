import pandas as pd
import numpy as np
import logging
from .data import Data
from .filepaths import full_dataset_filepath
from .canadas_coordinates import *
from .dataset_columns import full_dataset_site_names, target_columns

class FullData(Data):
	def __init__(self):
		Data.__init__(self)

		# Load the full_dataset csv file into a DataFrame and retain only the relevant columns
		self.dataset_df = pd.read_csv(full_dataset_filepath)
		self.sites = full_dataset_site_names
		self.df = self.dataset_df[full_dataset_site_names]
		self.target = self.dataset_df[target_columns]
		self.longitudes = []
		self.latitudes = []
		for site in full_dataset_site_names:
			self.longitudes.append(self.dataset_df[site + '_lon'][0])
			self.latitudes.append(self.dataset_df[site + '_lat'][0])

	def get_index_of_timestamp(self, timestamp):
		try:
			index = self.dataset_df.index[self.dataset_df['DD-HH'] == timestamp].to_list()[0]
		except:
			print(f"The timestamp {timestamp} is not present in the full dataset. Instead, fetching the index for the timestamp 01-01")
			index = self.dataset_df.index[self.dataset_df['DD-HH'] == "01-01"].to_list()[0]
		print(f"full data index is: {index}", flush=True)
		return index