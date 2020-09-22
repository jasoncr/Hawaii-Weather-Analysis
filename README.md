# sqlalchemy-challenge

In this challenge, I tested myself with SQLAlchemy and Flask. First, I wanted to use SQLAlchemy to do exploratory analysis on climate measurement stations. To do this, I worked inside a Jupyter Notebook and connected with SQLAlchemy to a sqlite file that held temperature and precipitaion observations from measurement stations around Hawaii. I used Pandas and matplotlib to create visualizations. The first visualization was a bar chart that looked at the last year's worth of observations. Below is that graph. 

<img src = "Images/inches_by_date.png" width=400>

The next question to determine was how many observations per station (which was the most active). Below is a table of the station ID, Name, and then the observation count.

<img src = "Images/station_obs_count.png" width=400>

The most active station, WAIHEE 837.5, HI US and I found that the minimum temperature was: 54.0 degrees, its maximum temperature was: 85.0 degrees, and its average temperature was: 71.7 degrees. For further analysis, I created a temperature vs frequency bar chart of station WAIHEE. Below is that visualization.

<img src = "Images/temp_frequencies.png" width=400>

