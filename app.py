# import flask
from flask import Flask, jsonify
#dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app=Flask(__name__)

# home route
@app.route("/")
def home():
    print("List all available api routes. ")
    return(
    f"Welcome!<br/>"
    f"Available Routes:<br/>"
    f"<br/>"
    f"Precipitation:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"<br/>"
    f"Station List:<br/>"
    f"//api/v1.0/stations<br/>"
    f"<br/>"
    f"Temperature for a year:<br/>"
    f"/api/v1.0/tobs<br/>"
    f"<br/>"
    f"Min, Max, and Avg. temps for given start date:<br/>"
    f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
    f"Min, Max, and Avg. temps for given start and end date:<br/>"
    f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"

    
)
# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>=year_ago).\
        order_by(Measurement.date).all()
    precip_data_list = dict(precip_data)
    return jsonify(precip_data_list)

# station route
@app.route("/api/v1.0/stations")
def stations():
        stations = session.query(Station.station, Station.name).all()
        station_list = list(stations)
        return jsonify(station_list)

# TOBs route
@app.route("/api/v1.0/tobs")
def tobs():
        year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= year_ago).\
                order_by(Measurement.date).all()
        tobs_data_list = list(tobs_data)
        return jsonify(tobs_data_list)

# start-end day route
@app.route("/api/v1.0/<start>")
def Start_date(start_date):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()
      
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        min = start_date_tobs_dict["min_temp"]
        avg = start_date_tobs_dict["avg_temp"]
        max = start_date_tobs_dict["max_temp"]
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

#Start-End Date
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start_date, end_date):
    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run()

