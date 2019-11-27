import sklearn
import numpy as np
import pandas as pd
import pickle
from xgboost import XGBRegressor
from .filepaths import trained_model_filepath
from .dataset_meta_data import columns_used_for_model_training

class Model():
	def __init__(self):
		self.model = self.load_model_from_file()
		self.predictions = {}
		print(f"Loaded the trained model...", flush=True)

	def load_model_from_file(self):
		model = pickle.load(open(trained_model_filepath, 'rb'))
		return model

	def make_predictions(self, data, year, week):

		self.predictions['year'] = year
		self.predictions['week'] = week
		self.predictions['result'] = []
		for polygon in data.polygon_grid.polygons:
			#print(f"Serving polygon {polygon['polygon_id']}", flush=True)
			result = {}
			result['lat1'] = float(polygon['bottom_edge'])
			result['lon1'] = float(polygon['left_edge'])
			
			result['lat2'] = float(polygon['bottom_edge'])
			result['lon2'] = float(polygon['right_edge'])
			
			result['lat3'] = float(polygon['top_edge'])
			result['lon3'] = float(polygon['right_edge'])

			result['lat4'] = float(polygon['top_edge'])
			result['lon4'] = float(polygon['left_edge'])

			if(polygon['polygon_id'] in data.unvisited_polygons):
				result['predicted_value'] = 0
			else:
				entire_row = data.X_test[data.X_test['polygon_id'] == polygon['polygon_id']]
				query = entire_row[columns_used_for_model_training]

				# Make prediction
				prediction = int(round(self.model.predict(query)[0]))
				if (prediction < 0):
					prediction *= -1
				result['predicted_value'] = prediction

			self.predictions['result'].append(result)

		return self.predictions