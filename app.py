import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setting up the database.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

session = Session(bind=engine)
Base = automap_base()
Base.prepare(engine,reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

measurement_dict = []
measurement_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').\
order_by(Measurement.date).all()
for m in measurement_query:
    measurement_dict.append({m[0]:m[1]})

station_list = []
station_query = session.query(Station.station, func.count(Measurement.date)).filter(Station.station == Measurement.station).\
group_by(Station.station).order_by(func.count(Measurement.date).desc()).all()
for s in station_query:
    station_list.append(s[0])

temp_list = []
temp_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').\
filter(Measurement.station.like('USC00519281')).order_by(Measurement.date).all()
for t in temp_query:
    temp_list.append(t[1])

all_measurements_query = session.query(Measurement.date,Measurement.tobs).all()

# all_measurements_query = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
#     group_by(Measurement.date).all()

app = Flask(__name__)

@app.route("/")
def home():
    print("Home page load successful.")
    return (
        f"Welcome to the SQLAlchemy Assignment home page.<br/><br/>"
        f"To see Precipitation data, please click <a href='/api/v1.0/precipitation'>here</a><br/>"
        f"To see Station data, please click <a href='/api/v1.0/stations'>here</a><br/>"
        f"To see Temperature data, please click <a href='/api/v1.0/tobs'>here</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(measurement_dict)

@app.route("/api/v1.0/stations")
def station():
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start_only(start):
    start_date = start.replace("-","")
    start_list = []
    for a in all_measurements_query:
        standardized_date = a[0].replace("-","")
        if start_date <= standardized_date:
            start_list.append(a[1])
    minimum = min(start_list)
    total = sum(start_list)
    length = len(start_list)
    average = total/length
    maximum = max(start_list)
    final_list = [minimum,average,maximum]
    return jsonify(final_list)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start,end):
    start_date = start.replace("-","")
    end_date = end.replace("-","")
    startend_list = []
    for a in all_measurements_query:
        standardized_date = a[0].replace("-","")
        if start_date <= standardized_date:
            if end_date >= standardized_date:
                startend_list.append(a[1])
    minimum = min(startend_list)
    total = sum(startend_list)
    length = len(startend_list)
    average = total/length
    maximum = max(startend_list)
    final_se_list = [minimum,average,maximum]
    return jsonify(final_se_list)

if __name__ == "__main__":
    app.run(debug=True)