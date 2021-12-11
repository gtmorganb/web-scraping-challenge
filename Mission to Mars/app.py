from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri = 'mongodb://localhost:27017/mars_data')

@app.route("/")
def index():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scrape():
    mars_info = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_info, upsert = True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)