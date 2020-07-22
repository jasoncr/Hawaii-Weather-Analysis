###################
# Dependencies
##################
import sqlalchemy
import numpy as np 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd

##################
# Database Setup
##################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect = True)

#Save the reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

##################
# Flask Setup
##################
app = Flask(__name__)

##################
# Flask Routes
##################

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
def precipitation(): #Displays dictionary of all dates and prcps
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


@app.route("/api/v1.0/stations")
def stations(): #Lists the stations in the dataset
    #Create session link
    session = Session(engine)

    #Return a JSON list of stations from the dataset.
    results = session.query(Station.station, Station.name).all()

    session.close()

    all_stations = []
    for station in results:
        all_stations.append(station)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs(): #Displays the dates and temp. observations of the most active station for the last year of data.
    # Create a session link
    session = Session(engine)

    # query to find the last date of the data
    last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    #save the last date in a date variable (query_date)
    last_date = last_date.date
    yr = int(last_date[0:4])
    mo = int(last_date[5:7])
    day = int(last_date[8:10])
    query_date = dt.date(yr, mo, day)

    #find the station with the most observations in the last year of data
    data = session.query(Measurement.tobs, Measurement.station).\
        filter(Measurement.date > query_date - dt.timedelta(days = 365)).\
            order_by(Measurement.date).all()
    data_df = pd.DataFrame(data)
    grouped = data_df.groupby('station').count().sort_values('tobs', ascending = False)
    most_active = grouped.index[0]

    #query the data to find the most active station's observations in the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > query_date - dt.timedelta(days = 365)).\
        filter(Measurement.station == most_active).all()

    session.close()

    all_observations = []
    for date, tobs in results:
        observations_dict = {}
        observations_dict['date'] = date
        observations_dict['tobs'] = tobs
        all_observations.append(observations_dict)

    return jsonify(all_observations)

@app.route("/api/v1.0/<start>")
def temp_breakdown(start): #Returns a list of the minimum temp, the average temp, and the max temp for given start date.
    #Create session link
    session = Session(engine)

    #query all the data from the start date on
    data = session.query(Measurement.tobs).\
        filter(Measurement.date >= start).all()
    
    session.close()

    #Converts to df and uses describe() to find the max, min, and mean
    data_df = pd.DataFrame(data)
    described = data_df.describe()

    return(
        f'Starting Date: {start}<br/>'
        f'minimum temp: {described.iloc[3,0]}<br/>'
        f'maximum temp: {described.iloc[7,0]}<br/>'
        f'average temp: {round(described.iloc[1,0], 1)}'
    )


@app.route("/api/v1.0/<start>/<end>")
def start_end_breakdown(start, end):
    #Create session link
    session = Session(engine)

    #query all the data from the start date on
    data = session.query(Measurement.tobs).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

    #Converts to df and uses describe() to find the max, min, and mean
    data_df = pd.DataFrame(data)
    described = data_df.describe()

    return(
        f'Starting Date: {start}<br/>'
        f'Ending Date: {end}<br/>'
        f'<br/>'
        f'minimum temp: {described.iloc[3,0]}<br/>'
        f'maximum temp: {described.iloc[7,0]}<br/>'
        f'average temp: {round(described.iloc[1,0], 1)}'
    )

if __name__ == '__main__':
    app.run(debug = True)