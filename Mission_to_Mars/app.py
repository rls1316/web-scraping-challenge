from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from scrape_mars import scrape_info

# Create instane of Flask
app = Flask(__name__)

# Use Pymongo to establish Mongo connection
mongo = PyMongo(app, uri = 'mongodb://localhost:27017/mars.app')

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run scrape function and save results to a variable
    Mars_Data = mongo.db.Mars_Data
    Mars_Data_Scrape = scrape_info()

    # Update the Mongo db using update upsert = True
    Mars_Data.update({}, Mars_Data_Scrape, upsert = True)

    # Redirect back to index/ Home Page
    return redirect("/")

# Route to render index.html template using data from Mongo
@app.route("/")
def index(): 

    # Find one record of data from mongo db
    Mars_Data = mongo.db.Mars_Data.find_one()
    return render_template("index.html", Mars_Data = Mars_Data)

if __name__ == "__main__":
    app.run(debug = True)