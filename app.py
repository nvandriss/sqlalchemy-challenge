#dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app=Flask(__name__)

# home route
@app.route("/")
def home():
 return """<html>
<h1>Available Routes:</h1>
<p>Precipitation:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station List:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2016-08-23</a></li>
</ul>
<p>Start & End Day:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2016-08-23/2017-08-23</a></li>
</ul>
</html>
"""

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>=year_ago).\
        all()

    precip_data_list = dict(precip_data)
    return jsonify(precip_data_list)

# station route
@app.route("/api/v1.0/stations")
def stations():
        all_stations = session.query(Station.station, Station.name).all()
        station_list = list(all_stations)
        return jsonify(station_list)

# TOBs route
@app.route("/api/v1.0/tobs")
def tobs():
        year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= year_ago).\
                order_by(Measurement.date).all()
        tobs_list = list(tobs_data)
        return jsonify(tobs_list)

# start day route
@app.route("/api/v1.0/<start>")
def Start_Date(start_date):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).\
                  all()

      
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        min = start_date_tobs_dict["min_temp"]
        avg = start_date_tobs_dict["avg_temp"]
        max = start_date_tobs_dict["max_temp"]
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

#start-end date
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start_date, end_date):
    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
  
    start_end = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end.append(start_end_dict) 
    

    return jsonify(start_end)

if __name__ == '__main__':
    app.run()

