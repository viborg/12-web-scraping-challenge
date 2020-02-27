# scrape_mars_py
# a helper function for the web-scraping-challenge

# a test function
def hello():
    return "hello from scrape_mars.py"

def scrape_mars_data():
    from splinter import Browser
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import time
    import pymongo
 
    nasa_mars_news_url = 'https://mars.nasa.gov/news'
    jpl_mars_site_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    twitter_mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    mars_facts_site_url = 'https://space-facts.com/mars/'
    usgs_astrogeology_site_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # scrape dictionary
    scrape_data = {}

    # initiate splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    #-----------------------------------------------------------------
    # NASA Mars News
    print("\nNASA Mars News")
    print("--------------")
    #-----------------------------------------------------------------
    # render the web page content as a BeautifulSoup object and archive as a txt file, which 
    # can then be inspected with an editor to verify correctness (i.e. matches the content shown
    # in the browser inspector)
    browser.visit(nasa_mars_news_url)
    nasa_mars_news_soup = BeautifulSoup(browser.html, 'html.parser')
    with open("html_txt/nasa_mars_news.txt", "w") as file:
        file.write(nasa_mars_news_soup.prettify())

    # it seems to need a repeat to insure the entire web page is loaded
    time.sleep(2)
    browser.visit(nasa_mars_news_url)
    nasa_mars_news_soup = BeautifulSoup(browser.html, 'html.parser')
    with open("html_txt/nasa_mars_news.txt", "w") as file:
        file.write(nasa_mars_news_soup.prettify())

    # parse the soup object for the first slide class content and further examine
    nasa_mars_news_element = nasa_mars_news_soup.find('li', class_='slide')
    print(nasa_mars_news_element.prettify())

    # add to the scrape dictionary
    scrape_data["nasa_mars_news_title"] = nasa_mars_news_element.find('h3').text
    scrape_data["nasa_mars_news_p"] = nasa_mars_news_element.find(class_="article_teaser_body").text

    #-----------------------------------------------------------------
    # JPL Mars Space Images
    print("\nJPL Mars Space Images")
    print("---------------------")
    #-----------------------------------------------------------------
    # render the web page content as a BeautifulSoup object and archive as a txt file, which 
    browser.visit(jpl_mars_site_url)
    jpl_mars_site_soup = BeautifulSoup(browser.html, 'html.parser')
    with open("html_txt/jpl_mars_site.txt", "w") as file:
        file.write(jpl_mars_site_soup.prettify())

    # parse the soup object for the carousel_container class content and further examine
    jpl_mars_site_element = jpl_mars_site_soup.find(class_='carousel_container')
    print(jpl_mars_site_element.prettify())
    
    # extract the local URL link 
    jpl_mars_site_local_link = jpl_mars_site_element.find("a")['data-fancybox-href']

    # append the host URL link
    jpl_mars_site_link = 'https://www.jpl.nasa.gov' + jpl_mars_site_local_link
    print(jpl_mars_site_link)
    
    # add to the scrape dictionary
    scrape_data["jpl_mars_site_link"] = jpl_mars_site_link

    #-----------------------------------------------------------------
    # Mars Weather
    print("\nMars Weather")
    print("------------")
    #-----------------------------------------------------------------
    # Use Requests, instead of Splinter, because the latter does not
    # properly work for this web page
    twitter_mars_weather_response = requests.get(twitter_mars_weather_url)
#     time.sleep(2)

    # render the web page content as a BeautifulSoup object and archive as a txt file, which 
    # can then be inspected with an editor to verify correctness (i.e. matches the content shown
    # in the browser inspector)
    twitter_mars_weather_soup = BeautifulSoup(twitter_mars_weather_response.text, 'html.parser')
    with open("html_txt/twitter_mars_weather_site.txt", "w") as file:
        file.write(twitter_mars_weather_soup.prettify())

    # parse the soup object for the <p> content and further examine
    twitter_mars_weather_element = twitter_mars_weather_soup.find('p', class_="TweetTextSize")
    print(twitter_mars_weather_element.prettify())
    
    # extract the weather text
    twitter_mars_weather = twitter_mars_weather_element.text

    # add to the scrape dictionary
    scrape_data["twitter_mars_weather"] = twitter_mars_weather

    #-----------------------------------------------------------------
    # Mars Facts
    print("\nMars Facts")
    print("----------")
    #-----------------------------------------------------------------
    # render the web page content as a BeautifulSoup object and archive as a txt file
    browser.visit(mars_facts_site_url)
    mars_facts_site_soup = BeautifulSoup(browser.html, 'html.parser')
    with open("html_txt/mars_facts_site.txt", "w") as file:
        file.write(mars_facts_site_soup.prettify())

    mars_facts_site_tables = pd.read_html(mars_facts_site_url)
    print(mars_facts_site_tables)
    
    # extract the single table from the list of tables and name the columns
    mars_facts_site_table_df = mars_facts_site_tables[0]
    mars_facts_site_table_df.columns = ['Item', 'Value']

    # convert the data frame to an html string
    mars_facts_site_html_table = mars_facts_site_table_df.to_html()
    print(mars_facts_site_html_table)
    
    # add to the scrape dictionary
    scrape_data["mars_facts_html"] = mars_facts_site_html_table

    #-----------------------------------------------------------------
    # Mars Hemispheres
    print("\nMars Hemispheres")
    print("----------------")
    #-----------------------------------------------------------------
    # render the web page content as a BeautifulSoup object and archive as a txt file
    browser.visit(usgs_astrogeology_site_url)
    usgs_astrogeology_site_soup = BeautifulSoup(browser.html, 'html.parser')
    with open("html_txt/usgs_astrogeology_site.txt", "w") as file:
        file.write(usgs_astrogeology_site_soup.prettify())

    # build list of products
    # the webpage identifies each link as part of a "product" 
    astrogeology_products_list = []
    astrogeology_products = usgs_astrogeology_site_soup.find_all('h3')
    for product in astrogeology_products:
        title = product.text
        astrogeology_products_list.append(title)

    # extract the images from the child sites
    hemisphere_image_urls = []

    # click the link of each product (on the parent page) and get its image
    for image_idx in range(len(astrogeology_products_list)):
        # revisit the parent page (return from the image page) and build a list of buttons to be clicked
        # the button list is rebuilt
        # the term "button" refers to the element that contains the link to the page with the high
        # resolution image 
        browser.visit(usgs_astrogeology_site_url)
        usgs_astrogeology_site_soup = BeautifulSoup(browser.html, 'html.parser')
        buttons = browser.find_by_css('.thumb')
            
        # click the applicable button, per the loop count, which is image_idx
        print(f"Button #{image_idx} = {buttons[image_idx]}")
        buttons[image_idx].click()
            
        # obtain linked webpage content and save to a text file
        soup = BeautifulSoup(browser.html, 'html.parser')
        title = astrogeology_products_list[image_idx]
        with open("html_txt/" + title + ".txt", "w") as file:
            file.write(soup.prettify())
            
        # obtain the image of the product's corresponding webpage, which in the article having text = 'Original'
        articles = soup.find_all('a')
        for article in articles:
            if article.text == 'Sample':
                img_url = article['href']

        # append the title and image url as a dictionary to the image list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

        # end of for loop

    # add to the scrape dictionary
    scrape_data["hemisphere_image_urls"] = hemisphere_image_urls

    # send scrap_data to mongoDB
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars_data_db
    collection = db.items

    # insert the Mars data into MongoDB
    collection.insert_one(scrape_data)

    return