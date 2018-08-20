# import necessary libraries
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_scrape = mongo.db.mars_scrape.find_one()
    # return template and data
    return render_template("index.html", mars_scrape=mars_scrape)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    mars_scrape = mongo.db.mars_scrape
    mars_data = scrape_mars.scrape_mars()
    mars_scrape.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
