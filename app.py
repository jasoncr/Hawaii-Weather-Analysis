# Dependencies

import sqlalchemy
import numpy as np 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

##
# Database Setup
##
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect = True)

#Save the reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

##
# Flask Setup
##
app = Flask(__name__)

##
# Flask Routes
##

@app.route("/")
def welcome():
    #List all available routes
    return(
        f'Available Routes <br/>'
        f'/api/v1.0/precipitation <br/>'
        f'/api/v1.0/stations <br/>'
        f'/api/v1.0/tobs <br/>'
        f'/api/v1.0/start <br/>'
        f'/api/v1.0/start/end'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session link
    session = Session(engine)

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


#@app.route("/api/v1.0/stations")



#@app.route("/api/v1.0/tobs")


#@app.route("/api/v1.0/start")


#@app.route("/api/v1.0/start/end")


if __name__ == '__main__':
    app.run(debug = True)