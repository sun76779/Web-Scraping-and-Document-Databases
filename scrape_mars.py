from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import pymongo
import requests


from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time


def scrape_mars():

    # ## NASA Mars News

    # In[34]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html,"html.parser")

    # print(soup.prettify())

    # Scrapping the news title and first paragraph
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="rollover_description_inner").text

    print(f"Title: {news_title}")
    print(f"Paragraph: {news_paragraph}")


    # ## JPL Mars Space Images - Featured Image

    # In[38]:


    # URL of page to be scraped JPL Featured Space Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')


    # In[45]:


    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    img_path = jpl_soup.find('img', class_='thumb')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{img_path}'
    print(featured_image_url)


    # ## Mars Weather

    # In[47]:


    # URL of page to be scraped Mars Weather Twitter Page
    wea_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(wea_url)


    # In[55]:


    wea_html = browser.html
    wea_soup = BeautifulSoup(wea_html, 'html.parser')

    # Scraping the lastest tweet
    mars_weather = wea_soup.find('p', class_="tweet-text").text

    print(f"Last Weather Tweet: {mars_weather}")


    # ## Mars Facts

    # In[56]:


    url = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    ### BEGIN SOLUTION
    tables = pd.read_html(url)
    tables
    ### END SOLUTION                              


    # In[59]:


    df = tables[0]
    df.columns = ['Facts', 'Value']
    df.head()


    # In[64]:


    # Convert DataFrame to HTML and save the file
    html_table = df.to_html('table.html')


    # ## Mars Hemispheres

    # In[111]:


    # URL of page to be scraped Mars' hemispheres 
    hms_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    

    for i in range(1,9,2):
        hms_dicts = {}
        hms_dict = {}
        
        browser.visit(hms_url)

        hms_html = browser.html
        hms_soup = BeautifulSoup(hms_html, 'html.parser')
        hms_title = hms_soup.find_all('a', class_='product-item')
        hms_name = hms_title[i].text.strip('Enhanced')
        
        links = browser.find_by_css('a.product-item')
        links[i].click()
        

        browser.find_link_by_text('Sample').first.click()
        
    
        browser.windows.current = browser.windows[-1]
        hms_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        img_soup = BeautifulSoup(hms_img_html, 'html.parser')
        img_path = img_soup.find('img')['src']

        print(hms_name)
        hms_dict['title'] = hms_name.strip()
        
        print(img_path)
        hms_dict['img_url'] = img_path

        #hms_dicts.append(hms_dict)


    mars_scrape = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "html_table": html_table,
            #"hms_dicts": hms_dicts
            }
    
    #print(mars_scrape)
    return mars_scrape
