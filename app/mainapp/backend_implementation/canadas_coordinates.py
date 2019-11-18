'''
This file contains the values of coordinates that are used by the application to estimate and also
plot the magnetic field reading across Canada. It also contains the coordinates of the site named MEA 
which is the site with missing values in the holed dataset (i.e its values have to be predicted).

Source of extreme coordinates: https://en.wikipedia.org/wiki/List_of_extreme_points_of_Canada#All_Canada

Map for reference: http://legallandconverter.com/images/canada_grid.jpg
'''

# The Western-most longitude passing through Canada
western_most_longitude = -142.0

# The Eastern-most longitude passing through Canada
eastern_most_longitude = -51.0

# The Southern-most latitude passing through Canada
southern_most_latitude = 41.0

# The Northern-most latitude passing through Canada
northern_most_latitude = 84.0

# The longitude at the magnetometer site MEA (rounded off to the nearest 0.5 degrees longitude)
mea_longitude = -113.50 

# The lattitude at the magnetometer site MEA (rounded off to the nearest 0.5 degrees lattitude)
mea_latitude = 54.5
