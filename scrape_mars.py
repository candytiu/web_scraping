#import dependencies
import pandas as pd
import requests
from splinter import Browser
import os
from bs4 import BeautifulSoup as bs
import pymongo

def scrape():
    # # NASA Mars News
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(nasa_url)
    soup = bs(response.text, 'lxml')
    result = soup.body.find('div', class_="slide")
    # Assign the text to variables
    news_title = result.find('div',class_='content_title').text
    news_p = result.find('div',class_='rollover_description_inner').text
    
    #--------------------------------------------------------------------------------------------
    # # JPL Mars Space Images - Featured Image
    #setting up 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'lxml')
    
    # Finding the url for image
    jpl_result = jpl_soup.find('div', class_='default floating_text_area ms-layer').find("footer")
    featured_img_url = 'https://www.jpl.nasa.gov' + jpl_result.find('a')['data-fancybox-href']

    #--------------------------------------------------------------------------------------------
    # # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'lxml')

    twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')

    mars_weather = twitter_result.find('p', class_='js-tweet-text').text

    #--------------------------------------------------------------------------------------------
    # # Mars Facts
    fact_url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(fact_url)[0]
    fact_table.columns = ['Description','Value']
    fact_table.set_index('Description', inplace=True)
    
    #convert new pandas df to html, replace "\n" to get html code & Export pandas df to html script
    fact_html = fact_table.to_html()
    fact_html.replace("\n", "")
    fact_table.to_html('mars_fact.html')
    
    #--------------------------------------------------------------------------------------------
    # # Mars Hemispheres
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    usgs_html = browser.html
    usgs_soup = bs(usgs_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    images_list = usgs_soup.find_all('div', class_='item')
    image_urls  = []

    # Loop through each result and add it to the list 
    for image in images_list:
        usgs_dict = {}
        
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html, 'lxml')
        
        title = hemisphere_soup.find('div', class_='content').find('h2', class_='title').text
        usgs_dict['title'] = title
        
        img_url = hemisphere_soup.find('div', class_='downloads').find('a')['href']
        usgs_dict['url_img'] = img_url
        
        image_urls.append(usgs_dict)

    # Create a dictionary to hold all the varibles 
    mars_data = {
     "news_title": news_title,
     "news_p": news_p,
     "featured_image": featured_img_url,
     "mars_weather": mars_weather,
     "image_urls": image_urls
     }

    return mars_data
