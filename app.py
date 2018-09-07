import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcom to my Homepage Mike!<br><br>"
        f"Available APIs are the following:<br><br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br>"
        f"/api/v1.0/2016-08-22<br>"
        f"/api/v1.0/2016-08-22/2016-10-01/<br>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.tobs, Measurement.date)\
                            .filter(Measurement.date>"2016-08-22").all()
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict[measurement.date] = measurement.tobs
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    
    results = session.query(Measurement.tobs)\
                            .filter(Measurement.date>"2016-08-22").all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/")
def startt(start):
    
    results = session.query(func.max(Measurement.tobs),
                            func.min(Measurement.tobs),
                            func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()

    summary=[]
    for result in results:
        max_dict={}
        max_dict['Max Temp']=result[0]
        min_dict={}
        min_dict['Min Temp']=result[1]
        avg_dict={}
        avg_dict['Avg Temp']=result[2]
        summary.append(max_dict)
        summary.append(min_dict)
        summary.append(avg_dict)

    return jsonify(summary)

@app.route("/api/v1.0/<start>/<end>/")
def between(start,end):
    
    results = session.query(func.max(Measurement.tobs),
                            func.min(Measurement.tobs),
                            func.avg(Measurement.tobs)).filter(Measurement.date>=start, Measurement.date<=end).all()

    summary=[]
    for result in results:
        max_dict={}
        max_dict['Max Temp']=result[0]
        min_dict={}
        min_dict['Min Temp']=result[1]
        avg_dict={}
        avg_dict['Avg Temp']=result[2]
        summary.append(max_dict)
        summary.append(min_dict)
        summary.append(avg_dict)

    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)