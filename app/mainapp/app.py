from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='')
CORS(app)

# Load the datasets before the very first user request and have it available during the entire lifespan of the application.
# Hence, time taken for file I/O is reduced as the csv files (i.e datasets) are only read once and not for every user request.
@app.before_first_request
def load_datasets():
	pass


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
	return render_template('index.html')

@app.route('/av', methods=['POST', 'GET'])
def home(day='01', hour='01', dataset='full'): 
	pass

@app.route('/handle_input', methods=['POST'])
def handle_input():
	pass

# Set host to 0.0.0.0 so that it is accessible from 'outside the container'
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8001)))