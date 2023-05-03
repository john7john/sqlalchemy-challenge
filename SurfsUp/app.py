import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis Homepage. Here are the Available Routes:<br/>"
        f"<br/>"
        f"Precipitation Data for One Year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of Active Weather Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations of the Most-Active Station for One Year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The Average, Maximum, and Minimum Temperature for a specified Start Date(Format:yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"The Average, Maximum, and Minimum Temperatures for a specified Start and End Date(Format:yyyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    
    session = Session(engine)
    
    #year ago date
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    # Precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago_date).all()
                                                       
    session.close()
    
    # Create a dictionary to append list prcp_data
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)
        
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    # Retrieve data for all stations
    stations = session.query(Station.name, Station.station, Station.elevation, Station.latitude, Station.longitude).all()
                                                        
    session.close()
    
    
    station_data = []
    for name, station, elevation, latitude, longitude in stations:
        station_dict = {}
        station_dict["Name"] = name
        station_dict["Station ID"] = station
        station_dict["Elevation"] = elevation
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_data.append(station_dict)
        
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    
    
    session = Session(engine)
    
  