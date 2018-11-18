from flask import Flask, render_template, redirect
import scrape_mars
import pymongo

#################################################
# Database Setup
#################################################
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    try:
        mars_data = db.mars_data.find()
        return render_template('index.html', mars_data = mars_data)
    except:
        return redirect("http://localhost:5000/scrape", code=302)

@app.route("/scrape")
def scraped():
    mars = scrape_mars.scrape()
    collection = db.mars_data 

    collection.update(
        {},
        mars,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)