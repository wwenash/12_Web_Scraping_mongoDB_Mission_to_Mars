# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------
import numpy as np
import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests as req
import time

# --------------------------------------------------------------------------
# Initialize splinter Browser object (DRY)
# --------------------------------------------------------------------------
def initBrowser():
    """ Function: Creates splinter Browser object
        Parameters: None
        Returns: Browser object instance """
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)
    #return Browser("chrome", headless=False)
    time.sleep(10)

# --------------------------------------------------------------------------
# Close splinter Browser object (DRY)
# --------------------------------------------------------------------------
def closeBrowser(browser):
    """ Function: Closes splinter Browser object
        Parameters: (1) Browser object instance
        Returns: None """
    browser.quit()
    time.sleep(10)

# --------------------------------------------------------------------------
# Convert your Jupyter notebook into a Python script called scrape_mars.py
# with a function called scrape that will execute all of your scraping code
# and return one Python dictionary containing all of the scraped data.
# --------------------------------------------------------------------------
def scrape():
    """ Function: Main scrape functionality
        Calls other functions
        Parameters: None
        Returns: combined mars_data dictionary """

    mars_data = {}

    mars_data["news_data"] = marsNewsData()

    mars_data["featured_image_url"] = marsFeaturedImageURL()

    mars_data["mars_weather"] = marsWeather()

    mars_data["mars_facts"] = marsFacts()

    mars_data["mars_hemispheres"] = marsHemisphereImageURLs()

    # return mars_data dict
    return mars_data

# --------------------------------------------------------------------------
# NASA Mars News - Scrape the NASA Mars News Site and collect the latest
# News Title and Paragragh Text. Assign the text to variables that you can
# reference later.
# --------------------------------------------------------------------------
def marsNewsData():
    """ Function: Mars news data scraping functionality
        Scrapes NASA Mars news site @ nasa_url below
        Returns: news_data dictionary
        Parameters: None """
    news_data = {}
    mars_paragraph_text = [] 

    browser = initBrowser()

    base_url = "https://mars.nasa.gov/" 
    nasa_url = "https://mars.nasa.gov/news/"

    browser.visit(nasa_url)

    mars_html = browser.html
    mars_soup = bs(mars_html, "html.parser")

    time.sleep(2)

    news_title = mars_soup.find('div', class_="bottom_gradient").text
    news_p = mars_soup.find('div', class_="rollover_description_inner").text    

    mars_soup_div = mars_soup.find(class_="content_title")
    mars_soup_p2 = mars_soup_div.find_all('a', href=True)                                   
    mars_soup_p2_url = mars_soup_p2[0]['href']                                               
    mars_paragraph_url = base_url + mars_soup_p2_url 

    response = req.get(mars_paragraph_url)                                          
    mars_para_soup = bs(response.text, "html.parser")                                
    mars_paragraphs = mars_para_soup.find(class_='wysiwyg_content')                     
    All_paragraphs = mars_paragraphs.find_all('p') 

    for paragraph in All_paragraphs:                                                 # iterates through paragraphs
        clean_paragraph = paragraph.get_text().strip()                           # extracts and cleans paragraphs    
        mars_paragraph_text.append(clean_paragraph)

    
    news_data["news_title"] = news_title
    news_data["news_p"] = news_p
    news_data["mars_paragraph_text_1"] = mars_paragraph_text[0]

    closeBrowser(browser)

    return news_data
# --------------------------------------------------------------------------
# JPL Mars Space Images - Visit the url for JPL's Featured Space Image.
# Use splinter to navigate the site and find the image url for the current
# Featured Mars Image and assign the url string to a variable called
# featured_image_url.
# --------------------------------------------------------------------------
def marsFeaturedImageURL():
    """ Function: Mars featured image data scraping functionality
        Scrapes JPL news site @ jpl_url below
        Parameters: None
        Returns: featured_image_url string """

    browser = initBrowser()

    jpl_fullsize_url = 'https://photojournal.jpl.nasa.gov/jpeg/'
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(5)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    time.sleep(5)

    featured_image_list = []

    for image in jpl_soup.find_all('div',class_="img"):
        featured_image_list.append(image.find('img').get('src'))

    feature_image = featured_image_list[0]
    temp_list_1 = feature_image.split('-')
    temp_list_2 = temp_list_1[0].split('/')
    featured_image_url = jpl_fullsize_url + temp_list_2[-1] + '.jpg'

    closeBrowser(browser)

    return featured_image_url

# --------------------------------------------------------------------------
# Mars Weather - Visit the Mars Weather twitter account and scrape the
# latest Mars weather tweet from the page. Save the tweet text for the
# weather report as a variable called mars_weather
# --------------------------------------------------------------------------
def marsWeather():
    """ Function: Mars twitter weather data scraping functionality
        Scrapes Twitter for weather news @ tweet_url below
        Parameters: None
        Returns: mars_weather string """

    browser = initBrowser()

    tweeter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweeter_url)
    time.sleep(5)

    tweeter_html = browser.html
    tweeter_soup = bs(tweeter_html, 'html.parser')
    time.sleep(5)

    weather_info_list = []

    for weather_info in tweeter_soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_info_list.append(weather_info.text.strip())

    for value in reversed(weather_info_list):
        if value[:3]=='Sol':
            mars_weather = value

    closeBrowser(browser)

    return mars_weather

# --------------------------------------------------------------------------
# Mars Facts - Visit the Mars Facts webpage here and use Pandas to scrape
# the table containing facts about the planet including Diameter, Mass, etc.
# --------------------------------------------------------------------------
def marsFacts():
    """ Function: Mars facts data scraping functionality
        Scrapes Space-Facts site @ facts_url below
        Parameters: None
        Returns facts_table string (HTML) """

    facts_url = 'https://space-facts.com/mars/'
    fact_list = pd.read_html(facts_url)
    time.sleep(5)
    facts_df = fact_list[0]
    facts_table = facts_df.to_html(header=False, index=False)

    return facts_table

# --------------------------------------------------------------------------
# Mars Hemisperes - Visit the USGS Astrogeology site to obtain
# high resolution images for each of Mars' hemispheres.
# --------------------------------------------------------------------------
def marsHemisphereImageURLs():
    """ Function: Mars hemispheres image data scraping functionality
        Scrapes USGS site @ usgs_url below
        Parameters: None
        Returns: hemisphere_image_urls list """

    browser = initBrowser()

    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    time.sleep(5)

    usgs_html = browser.html
    usgs_soup = bs(usgs_html, 'html.parser')
    time.sleep(5)

    hemisphere_image_urls = []

    products = usgs_soup.find('div', class_='result-list')
    time.sleep(5)
    hemispheres = products.find_all('div', class_='item')
    time.sleep(5)

    for hemisphere in hemispheres:
        title = hemisphere.find('div', class_='description')

        title_text = title.a.text
        title_text = title_text.replace(' Enhanced', '')
        browser.click_link_by_partial_text(title_text)

        usgs_html = browser.html
        usgs_soup = bs(usgs_html, 'html.parser')

        image = usgs_soup.find('div', class_='downloads').find('ul').find('li')
        img_url = image.a['href']

        hemisphere_image_urls.append({'title': title_text, 'img_url': img_url})

        browser.click_link_by_partial_text('Back')

    closeBrowser(browser)

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape())