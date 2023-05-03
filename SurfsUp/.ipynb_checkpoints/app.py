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
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save reference to the table
station = base.classes.station
measurement = base.classes.measurement
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"<strong/>Available Routes:</strong> <br/>"
        f"<br/><strong/>Precipitation during the last year of available data (2016-08-24 to 2017-08-23):</strong> /api/v1.0/precipitation<br/>"
        f"<br/><strong/>List of stations:</strong>  /api/v1.0/stations<br/>"
        f"<br/><strong/>Dates and temperature observations during the last year of available data (2016-08-24 to 2017-08-23):</strong>  /api/v1.0/tobs<br/>"
        f"<br/><strong/>List of minimum temperature, average temperature, and max temperature for a given start date (use YYYY-MM-DD):</strong>  /api/v1.0/<start><br/>"
        f"<br><strong/>List of minimum temperature, average temperature, and max temperature for a given start and end (use YYYY-MM-DD):</strong>  /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    # Query precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-24").\
        filter(Measurement.date <= "2017-08-23").all()

    session.close()

    return jsonify({k:v for k,v in results})
    
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station = list(np.ravel(results))
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Query tobs
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date >="2016-08-24", Measurement.date <="2017-08-23").all()
    
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<date>")
def start(date):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    # Query date
    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs) ).\
    group_by(Measurement.date).filter(Measurement.date >= date).group_by(Measurement.date).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None,end=None):
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    # Query start and end
    results = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs) ).\
    filter(Measurement.date >= start).filter(Measurement.date <=end ).group_by(Measurement.date).all()

    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
