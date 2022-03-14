# import necessary libraries
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars = mongo.db.mars.find_one()
   
    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scrape_mars.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
    app.run()