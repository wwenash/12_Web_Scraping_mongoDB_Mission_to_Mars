# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------
from flask import Flask, jsonify, redirect, render_template
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# --------------------------------------------------------------------------
# Initializes connection to MongoDb; default port 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
# Remember to start MongoDb server daemon prior to execution
# --------------------------------------------------------------------------
client = pymongo.MongoClient('mongodb://localhost:27017')

# --------------------------------------------------------------------------
# Initializes initialize flask
# --------------------------------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------------------------------
# Nominates MongoDb database and collection
# --------------------------------------------------------------------------
db = client.mars_data_DB

# Drops collection if available to remove duplicates
db.mars_collection.drop()

mars_collection = db.mars_collection

# --------------------------------------------------------------------------
# Initializes default route
# --------------------------------------------------------------------------
@app.route("/")
def render_index():
    # Error handler for missing collection
    try:
        mars_find =  mars_collection.find_one()

        # Distributes data from collection
        news_title = mars_find['news_data']['news_title']
        paragraph_text = mars_find['news_data']['news_p']
        paragraph_text_2 = mars_find['news_data']['mars_paragraph_text_1']
        featured_image_url = mars_find['featured_image_url']
        mars_weather_tweet = mars_find['mars_weather']
        mars_facts_table = mars_find['mars_facts']
        hemisphere_title_1 = mars_find['mars_hemispheres'][0]['title']
        hemisphere_img_1 = mars_find['mars_hemispheres'][0]['img_url']
        hemisphere_title_2 = mars_find['mars_hemispheres'][1]['title']
        hemisphere_img_2 = mars_find['mars_hemispheres'][1]['img_url']
        hemisphere_title_3 = mars_find['mars_hemispheres'][2]['title']
        hemisphere_img_3 = mars_find['mars_hemispheres'][2]['img_url']
        hemisphere_title_4 = mars_find['mars_hemispheres'][3]['title']
        hemisphere_img_4 = mars_find['mars_hemispheres'][3]['img_url']
    except (IndexError, TypeError) as error_handler:

        # Missing collection; clears fields
        news_title = ""
        paragraph_text =""
        paragraph_text_2 = ""
        featured_image_url = ""
        mars_weather_tweet = ""
        mars_facts_table = ""
        hemisphere_title_1 = ""
        hemisphere_img_1 = ""
        hemisphere_title_2 = ""
        hemisphere_img_2 = ""
        hemisphere_title_3 = ""
        hemisphere_img_3 = ""
        hemisphere_title_4 = ""
        hemisphere_img_4 = ""

    # ------------------------------------------------------------------------
    # Renders template to index.html
    # ------------------------------------------------------------------------
    return render_template("index.html", news_title=news_title,\
                                         paragraph_text=paragraph_text,\
                                         paragraph_text_2=paragraph_text_2,\
                                         featured_image_url=featured_image_url,\
                                         mars_weather_tweet=mars_weather_tweet,\
                                         mars_facts_table=mars_facts_table,\
                                         hemisphere_title_1=hemisphere_title_1,\
                                         hemisphere_img_1=hemisphere_img_1,\
                                         hemisphere_title_2=hemisphere_title_2,\
                                         hemisphere_img_2=hemisphere_img_2,\
                                         hemisphere_title_3=hemisphere_title_3,\
                                         hemisphere_img_3=hemisphere_img_3,\
                                         hemisphere_title_4=hemisphere_title_4,\
                                         hemisphere_img_4=hemisphere_img_4)

# --------------------------------------------------------------------------
# Initializes scrape route; inserts results into  mars_data_db in MongoDB
# --------------------------------------------------------------------------
@app.route('/scrape')
def scrape_mars_data():
    scrape_results = scrape_mars.scrape()
    mars_collection.replace_one({}, scrape_results, upsert=True)
    #mars_collection.update_many({}, scrape_results, upsert=True)
    return redirect('http://localhost:5000/', code=302)

if __name__ == '__main__':
    app.run(debug=True)