# Climate Data Analysis and API
This project involves analyzing climate data using Python, SQLAlchemy, Pandas, and Matplotlib, followed by creating a Flask API to serve the data. The dataset used is a SQLite database of climate data from Hawaii.

# Project Structure
# Part 1: Climate Data Analysis
Connected to the SQLite database using SQLAlchemy.
Performed precipitation and station analysis.
Visualized precipitation data over the last 12 months.
Analyzed temperature observations (TOBS) for the most active weather station.
Created histograms for temperature data.
# Part 2: Flask API Design
Created API routes to serve climate data in JSON format.
Routes include:
/: Lists available routes.
/api/v1.0/precipitation: Returns the last 12 months of precipitation data.
/api/v1.0/stations: Returns a list of all weather stations.
/api/v1.0/tobs: Returns temperature observations for the most active station.
/api/v1.0/<start>: Returns min, avg, and max temperatures from a start date.
/api/v1.0/<start>/<end>: Returns min, avg, and max temperatures for a date range.

# I was assisted by open-source AI language models, such as ChatGPT, to complete this challenge.
