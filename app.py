import numpy as np

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
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"You can consult the min, max and average from a start date format yyyy-mm-dd<br/>"
        f"Example:/api/v1.0/2017-08-23<br/>"  
        f"/api/v1.0/<start><br/>" 
        f"You can consult the min, max and average from a start date format yyyy-mm-dd to an end date format yyyy-mm-dd<br/>"
        f"Example:/api/v1.0/2015-05-24/2017-08-23<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prec():
    session = Session(engine)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date <= '2017-08-23').\
                    filter(Measurement.date >= '2016-08-24').all()
    
    session.close()

    precipitation_results = list(np.ravel(precipitation))
    return jsonify(precipitation_results)



@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    
    stations = session.query(Station.station).all()

    session.close()

    stations_results = list(np.ravel(stations))
    return jsonify(stations_results)


@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= '2017-08-23').\
           filter(Measurement.date >= '2016-08-24'). filter(Measurement.station == 'USC00519281').all()

    session.close()

    tobs_results = list(np.ravel(tobs))
    return jsonify(tobs_results)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    start_consult = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    session.close()

    start_list = []

    for min, max, avg in start_consult:
        start_tobs_dict = {}
        start_tobs_dict['min_temp'] = min
        start_tobs_dict['max_temp'] = max
        start_tobs_dict['avg_temp'] = avg
        start_list.append(start_tobs_dict)
    
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    start_end_consult = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    start_end_list = []

    for min, max, avg in start_end_consult:
        start_end_tobs_dict = {}
        start_end_tobs_dict['min_temp'] = min
        start_end_tobs_dict['max_temp'] = max
        start_end_tobs_dict['avg_temp'] = avg
        start_end_list.append(start_end_tobs_dict)
    
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)