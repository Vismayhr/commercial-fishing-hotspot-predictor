import numpy as np
from .canadas_coordinates import *

class PolygonGrid():
	def __init__(self):
		self.polygons = self.create_polygon_grid()

	def create_polygon_grid(self):
		## West coast grid box: polygons on to bin the coordinates on the west coast of Canada
		west_lat_grid = np.linspace(west_coast_grid_southern_latitude, west_coast_grid_northern_latitude, ((west_coast_grid_northern_latitude-west_coast_grid_southern_latitude)*2), endpoint=False)

		west_lon_grid = np.linspace(west_coast_grid_western_longitude, west_coast_grid_eastern_longitude, ((abs(west_coast_grid_western_longitude)-abs(west_coast_grid_eastern_longitude))*2), endpoint=False)
		p_id = 0
		west_polygon_list = []
		for lat in west_lat_grid:
		    for lon in west_lon_grid:
		        polygon = {}
		        b = lat
		        t = lat+0.5
		        l = lon
		        r = lon+0.5
		        polygon['polygon_id'] = p_id
		        polygon['bottom_edge'] = b
		        polygon['top_edge'] = t
		        polygon['left_edge'] = l
		        polygon['right_edge'] = r
		        west_polygon_list.append(polygon)
		        p_id += 1
		print(f"West polygon[-1]: {west_polygon_list[-1]}")
				
		## East coast grid box: polygons on to bin the coordinates on the east coast of Canada
		east_lat_grid = np.linspace(east_coast_grid_southern_latitude, east_coast_grid_northern_latitude, ((east_coast_grid_northern_latitude-east_coast_grid_southern_latitude)*2), endpoint=False)
		east_lon_grid = np.linspace(east_coast_grid_western_longitude, east_coast_grid_eastern_longitude, ((abs(east_coast_grid_western_longitude)-abs(east_coast_grid_eastern_longitude))*2), endpoint=False)

		east_polygon_list = []
		for lat in east_lat_grid:
		    for lon in east_lon_grid:
		        polygon = {}
		        b = lat
		        t = lat+0.5
		        l = lon
		        r = lon+0.5
		        polygon['polygon_id'] = p_id
		        polygon['bottom_edge'] = b
		        polygon['top_edge'] = t
		        polygon['left_edge'] = l
		        polygon['right_edge'] = r
		        east_polygon_list.append(polygon)
		        p_id += 1
		print(f"East polygon[-1]: {east_polygon_list[-1]}")

		# Join the two lists and return them
		return(west_polygon_list + east_polygon_list)