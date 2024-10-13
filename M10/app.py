# Import dependencies
import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Set up the database engine for SQLite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session (link) from Python to the DB
session = Session(engine)

# Set up Flask
app = Flask(__name__)

# Define the home route
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months"""
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
    # Create a dictionary with the date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all weather stations"""
    # Query all stations
    stations_data = session.query(Station.station).all()
    
    # Unravel results into a list
    stations_list = list(np.ravel(stations_data))
    
    return jsonify(stations_list)
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station for the last year"""
    # Find the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    # Calculate the date 1 year ago from the last data point
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query the temperature observations for the most active station for the last year
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Return the temperature observations as a JSON list
    tobs_list = list(np.ravel(tobs_data))
    
    return jsonify(tobs_list)
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return TMIN, TAVG, and TMAX for a specified start or start-end range."""
    # Query for minimum, average, and maximum temperatures based on the start date
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        # Calculate TMIN, TAVG, TMAX for all dates >= start date
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        # Calculate TMIN, TAVG, TMAX for dates between start and end (inclusive)
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Unravel results into a list and return JSON
    temp_list = list(np.ravel(results))
    
    return jsonify(temp_list)


# Check if the app is run directly
if __name__ == '__main__':
    app.run(debug=True)
