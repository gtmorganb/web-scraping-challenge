from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


def scrape(): 
    #Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(4)
    #making html object
    mars_news = browser.html
    #using beautiful soup to parse object 
    soup1 = BeautifulSoup(mars_news, 'html.parser')
    #getting first title
    news_title = soup1.find('div', class_='content_title').text
    #getting first paragraph text 
    news_p = soup1.find('div', class_ = 'article_teaser_body').text
    
    #Mars Image
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    time.sleep(4)
    mars_img = browser.html
    soup2 = BeautifulSoup(mars_img, 'html.parser')
    img_src = soup2.find('img', class_='headerimage fade-in')['src']
    img_url = img_src.replace("background-image: url('","").replace("');","")
    featured_image_url = f"https://spaceimages-mars.com/{img_url}"

    #Mars Facts
    #url and opening table in html using pandas 
    facts_url = 'https://galaxyfacts-mars.com/'
    facts_table = pd.read_html(facts_url)
    
    #create table from html
    type(facts_table)
    facts_df = facts_table[0]
    #label columns 
    facts_df.columns = ["Mars-Earth Comparison", "Mars", "Earth"]
    facts_df = facts_df.set_index("Mars-Earth Comparison")
    
    """
    Mars_data
    """
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    # Collect the tables from the page 
    tables = pd.read_html(requests.get('https://space-facts.com/mars/').text)
    #tables = pd.read_html(facts_url)

    # Retrieve the table containing facts about the planet 
    df = tables[2]
    df.columns = ["Description","Value"]
    idx_df = df.set_index("Description")
    # Export to a HTML file
    mars_df = idx_df.to_html(border="1",justify="left")
   

    """
    Mars Hemispheres
    """
    # Navigate to the page
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(4)
    # Assign the HTML content of the page to a variable
    hemisphere_html = browser.html
    # Parse HTML with Beautifulsoup
    soup = BeautifulSoup(hemisphere_html,'html.parser')

    # Collect the urls for the hemisphere images
    items = soup.find_all("div", class_="item")

    main_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls=[]
    for item in items:
        hemisphere_url = f"{main_url}{item.find('a', class_='itemLink')['href']}"
        
        # Navigate to the page
        browser.visit(hemisphere_url)
        time.sleep(4)
        # Assign the HTML content of the page to a variable
        hemisphere_html = browser.html
        # Parse HTML with Beautifulsoup
        soup = BeautifulSoup(hemisphere_html,'html.parser')
        
        img_url = soup.find('img', class_="wide-image")['src']
        title = soup.find('h2', class_="title").text
        
        hemisphere_image_urls.append({"title":title,"img_url":f"{main_url}{img_url}"})
    
    
    mars_info = {
        "mars_news": {
            "news_title": news_title,
            "news_p": news_p,
            },
        "mars_img": featured_image_url,
        "mars_weather": mars_weather,
        "mars_fact": mars_df,
        "mars_hemisphere": hemisphere_image_urls
    }
    browser.quit()

    return mars_info