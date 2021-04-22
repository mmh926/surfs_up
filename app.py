
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)
@app.route("/")

#if __name__ == "__main__":
#    app.run()
def welcome():
    return(
    '''
    Welcome to the Hawaii Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")

# add the line of code that calculates the date one year ago from the most 
# recent date in the database. 
# Next, write a query to get the date and precipitation for the previous year.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# Now run "flask run" via terminal then copy/paste http://127.0.0.1:5000/api/v1.0/precipitation.

# Now create route # 3, Stations Route. We'll run a list of all stations.
# Begin by defining the route and route name. NOTE: THERE ARE NO INDENTATIONS.
@app.route("/api/v1.0/stations")
#With our route defined, we'll create a new function called stations().
#def stations():
#    return
# Now create a query that will get all of the stations in our database.
#def stations():
#    results = session.query(Station.station).all()
#    return
# Next, convert our unraveled results into a one dimensional list. 
# To convert the results to a list, use the list function, which is list(), 
# then convert that array into a list. Then we'll jsonify the list and return 
# it as JSON. 
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Next, define the temperature observations for the previous year. Define the route:
@app.route("/api/v1.0/tobs")
# Next, create a function called temp_monthly():
#def temp_monthly():
#    return
# Now, calculate the date one year ago from the last date in the database. 
# (This is the same date as the one we calculated previously.) 
#def temp_monthly():
#    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
#    return
# Next, query the primary station for all the temp obs from the prev year.
#def temp_monthly():
    # prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # results = session.query(Measurement.tobs).\
    #     filter(Measurement.station == 'USC00519281').\
    #     filter(Measurement.date >= prev_year).all()
    # return
# Finally, unravel the results into one-dimensional array and convert array into a list.
# Then Jsonify the list and return the results.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Our last route will be to report on the minimum, average, and maximum temperatures 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Next, create a function called stats()
# add parameters to our stats()function: a start parameter and an end parameter.
    # def stats(start=None, end=None):
    #     return
# With the function declared, we can now create a query to select the minimum, 
# average, and maximum temperatures from our SQLite database. Then add an "if-not" statement.
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)








# Now that everything has been declared, run/launch the application...
#if __name__ == ‘__main__‘:
#    app.run()