from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import pandas as pd
import pickle
from backend_implementation.filepaths import full_dataset_filepath, trained_model_filepath
from backend_implementation.data import Data
from backend_implementation.user_input import UserInput


# Create global variables used throughout the life of the application
data = None
trained_model = None

app = Flask(__name__, static_url_path='')
CORS(app)

# Load the datasets before the very first user request and have it available during the entire lifespan of the application.
# Hence, time taken for file I/O is reduced as the csv files (i.e datasets) are only read once and not for every user request.
@app.before_first_request
def setup():
	print(f"Setting up the server....")
	print(f"Loading the dataset from: {full_dataset_filepath}", flush=True)
	global data
	data = Data()
	print(f"Shape of the dataset is: {data.dataset.shape}", flush=True)
	
	print(f"Loading the trained model from: {trained_model_filepath}", flush=True)
	global trained_model
	trained_model = pickle.load(open(trained_model_filepath, 'rb'))
	print("Server setup complete. Server can handle user requests now...", flush=True)


@app.route('/init', methods=['GET'])
def init():
    return "Init method called"


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.route('/')
def go_home():
	return redirect(url_for('home'))

@app.route('/fishing-vessel-presence', methods=['POST', 'GET'])
def home(year='2015', week='1'): 
	if request.method == 'POST':
		form_values = request.form.to_dict()
		year = form_values['year']
		week = form_values['week']
		print(f"POST request received. year: {year} and week: {week}", flush=True)
	else:
		print(f"GET request received. Using default values: {year} {week}", flush=True)

	# Store the user input
	user_input = UserInput(year, week)

	# Update the df with the year and week input by the user
	data.update_df_with_user_input(user_input)

	print(f"The updated df:\n{data.X_test.head()}", flush=True)

	data.perform_feature_encoding()

	print(f"The df after feature encoding:\n{data.X_test.head()}", flush=True)	


	return render_template('index.html')

@app.route('/handle_input', methods=['POST'])
def handle_input():
	pass

# Set host to 0.0.0.0 so that it is accessible from 'outside the container'
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8001)))