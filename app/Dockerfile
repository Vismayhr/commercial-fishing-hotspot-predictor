# Install a base Ubuntu image
FROM ubuntu:18.04

# Update Ubuntu dependencies and install python3 and flask
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install flask flask-cors uwsgi

# Install python packages required to build the model (numpy, pykrige, etc)
RUN pip3 install numpy scipy matplotlib pandas sklearn xgboost

# Copy the files of the application into the work space of the container
COPY ./ ./app
WORKDIR ./app

# Install the python dependencies listed in requirements.txt
#RUN pip3 install -r requirements.txt

# Expose Docker's port
EXPOSE 8001:80

# Run the flask app
CMD ["python3", "./mainapp/app.py"]