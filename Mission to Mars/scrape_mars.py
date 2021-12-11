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
    facts_df_table = facts_df.to_html(classes="table table-striped")
    
    #Mars Hempispheres 

    the_url = 'https://marshemispheres.com/'
    browser.visit(the_url)
    time.sleep(4)
    the_url_html = browser.html
    soup3 = BeautifulSoup(the_url_html, 'html.parser')

    hem_urls = []

    links = soup3.find_all('div', class_= 'item')
    for link in links: 
        hem_urls.append(f"{the_url}{link.find('a', class_ = 'itemLink product-item')['href']}")

    #using links above, iterate through list and pull info from each page
    #put title and img src into dictionary
    hem_img_urls = []

    for url in hem_urls: 
        browser.visit(url)
    
        time.sleep(4)
    
        hem_html = browser.html
        soup = BeautifulSoup(hem_html, 'html.parser')
    
        article_name = soup.find('h2', class_ = 'title').text
        hem_img_url = soup.find('img', class_ = 'wide-image')['src']
    
        hem_img_urls.append({"title":article_name,"img_url":f"https://marshemispheres.com/{hem_img_url}"})
    
    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_img": featured_image_url,
        "mars_facts": facts_df_table,
        "mars_hemisphere": hem_img_urls
    }
    browser.quit()

    return mars_info