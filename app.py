# import necessary libraries
from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

collection = db.mars_collection

@app.route("/test")
def test():
    return (
        f"Hello Shang"
    )


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_scrape = db.collection.find_one()
    # return template and data
    return render_template("index.html", mars_scrape=mars_scrape)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    db.collection.remove({})

    mars_data = scrape_mars.scrape_mars()
    db.collection.insert_one(mars_data)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
