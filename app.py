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
    amq_list = []
    for a in all_measurements_query:
        standardized_date = a[0].replace("-","")
        if start_date <= standardized_date:
            amq_list.append(a[1])
    minimum = min(amq_list)
    total = sum(amq_list)
    length = len(amq_list)
    average = total/length
    maximum = max(amq_list)
    final_list = [minimum,average,maximum]
    return jsonify(final_list)

# @app.route("/api/v1.0/<start>")
# def start_only(start):
#     standardized_date = start.replace("-","")
#     all_measurements_query = session.query(Measurement.date,Measurement.tobs).\
#         filter(Measurement.date >= start).all()
#     for a in all_measurements_query:
#         search_term = a[0].replace("-","")
#         if standardized_date == search_term:
#             date_temp_list = []
#             date_temp_list.append(a[1])
#             date_temp_list.append(a[2])
#             date_temp_list.append(a[3])
#             return(
#                 jsonify(date_temp_list)
#                 # f"Starting from {start}, the minimum temp was {min_temp},<br/>"
#                 # f"the average temp was {avg_temp}, and the max temp was {max_temp}."
#             )
#     return "Nope, didn't work..."

if __name__ == "__main__":
    app.run(debug=True)

# PRACTICE CODE
# hello_dict = [{"Hello":"World"},{"Hello":"Portland"}]

# justice_league_members = [
#     {"superhero": "Aquaman", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

# @app.route("/")
# def home():
#     print("Operation: Successful")
#     return (
#         "You made it home!<br/>"
#         "Here are links to all pages.<br/>"
#         f"<a href='/about'>About</a><br/>"
#         f"<a href='/contact'>Contact</a><br/>"
#         f"<a href='/jsonified'>Jsonified</a><br/>"
#         f"<a href='/api/v1.0/justice-league'>Justice League</a><br/>"
#         f"Welcome to the Justice League API!<br/>"
#         f"Available Routes:<br/>"
#         f"<a href='/api/v1.0/justice-league'>All Heros</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Arthur%20Curry'>Arthur Curry</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Bruce%20Wayne'>Bruce Wayne</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Victor%20Stone'>Victor Stone</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Barry%20Allen'>Barry Allen</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Hal%20Jordan'>Hal Jordan</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Clark%20Kent'>Clark Kent</a><br/>"
#         f"<a href='/api/v1.0/justice-league/real_name/Princess%20Diana'>Princess Diana</a>"
#     )
# @app.route("/about")
# def about():
#     print("Operation: Successful 'About' page location")

#     name = "Brock"
#     location = "Portland, OR"

#     return (
#         f"My name is {name} and I am located in {location}.<br/>"
#         "Click below to return to home page.<br/>"
#         f"<a href='/'>Home</a>"
#     )

# @app.route("/contact")
# def contact():
#     email = "brock.vriesman@gmail.com"

#     return (
#         f"If you want to get a hold of me, email me at {email}."
#         "Click below to return to home page.<br/>"
#         f"<a href='/'>Home</a>"
#     )

# @app.route("/jsonified")
# def jsonified():
#     return jsonify(hello_dict)

# @app.route("/api/v1.0/justice-league")
# def justice_league():
#     return jsonify(justice_league_members)

# @app.route("/api/v1.0/justice-league/real_name/<real_name>")
# def justice_league_real_name(real_name):
#     standardized = real_name.replace(" ","").lower()
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ","").lower()
#         if search_term == standardized:
#             return jsonify(character)
#     return jsonify({"error":f"Character with real_name {real_name} not found."}),404

# @app.route("/api/v1.0/justice-league/superhero/<superhero>")
# def justice_league_superhero(superhero):
#     standardized = superhero.replace(" ","").lower()
#     for character in justice_league_members:
#         search_term = character["superhero"].replace(" ","").lower()
#         if search_term == standardized:
#             return jsonify(character)
#     return jsonify({"error":f"The superhero {superhero} was not found"}),404

# if __name__ == "__main__":
#     app.run(debug=True)
