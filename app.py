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

measurement_df = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').\
order_by(Measurement.date).all()


app = Flask(__name__)

@app.route("/")
def home():
    print("Home page load successful.")
    return (
        f"Welcome to the home page.<br/><br/>"
        f"To see Precipitation data, please click <a href='/api/v1.0/precipitation'>here</a><br/>"
        f"To see Station data, please click <a href='/api/v1.0/stations'>here</a><br/>"
        f"To see Temperature data, please click <a href='/api/v1.0/tobs'>here</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(measurement_df)

@app.route("/api/v1.0/stations")
def station():
    return "Welcome to the Station landing page."

@app.route("/api/v1.0/tobs")
def tobs():
    return "Welcome to the Temperature landing page."


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
