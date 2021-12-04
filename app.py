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
    """List all available api routes."""
    return (
f"Available Routes:<br/>"
f"Precipitation:<br/>"
f"/api/v1.0/precipitation<br/>"
f"Station List:<br/>"
f"/api/v1.0/stations<br/>"
f"Temperature:<br/>"
f"/api/v1.0/tobs<br/>"
f"Start Day:<br/>"
f"/api/v1.0/2017-03-14<br/>"
f"Start & End Day:<br/>"
f"/api/v1.0/2017-03-14/2017-03-28<br/>"
    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return precipitation data"""
    year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>=year_ago).\
        all()
    session.close()
    precip_data_list = dict(precip_data)
    return jsonify(precip_data_list)

# station route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return all of the station in the database"""
    all_stations = session.query(Station.station, Station.name).all()
    session.close()
    station_list = list(all_stations)
    return jsonify(station_list)

# TOBs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return most active station for the last year"""
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
          filter(Measurement.date >= year_ago).\
          order_by(Measurement.date).all()
    session.close()
    tobs_list = list(tobs_data)
    return jsonify(tobs_list)

# start day route
@app.route("/api/v1.0/<start>")
def Start_Date(start_date):
    session = Session(engine)
    """TMIN, TMAX, TAVG for Start Date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).\
                  all()
    session.close()
      
    temps = []
    for result in results:
        row = {}
        row["TMIN"] = result[0]
        row["TMAX"] = result[1]
        row["TAVG"] = result[2]

        temps.append(row)

    return jsonify(temps)

#start-end date
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start_date, end_date):
    session = Session(engine)
    """TMIN, TMAX, TAVG for Start Date to End Date"""


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    start_end = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict["TMIN"] = min
        start_end_dict["TMAX"] = max
        start_end_dict["TAVG"] = avg
        start_end.append(start_end_dict)

    return jsonify(start_end)

if __name__ == '__main__':
    app.run()

