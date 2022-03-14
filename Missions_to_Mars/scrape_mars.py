#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import pymongo
import pandas as pd
import requests


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # Step 1 - Scraping
# 
# * Initial scraping using Jupyter Notebook. Link provided in instructions for "https://redplanetscience.com/" did not appear to have the correct background links to search. Found "https://mars.nasa.gov/news/" to have the same information but the right components in the html code to scrape.

# In[3]:


url = ('https://mars.nasa.gov/news/')

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# In[4]:


#print(soup.prettify())


# In[5]:


# pull titles from website
news_title = soup.find_all('div', class_="content_title")
#print(news_title)


# In[6]:


# pull body from website
news_p = soup.find_all('div', class_="rollover_description_inner")
#print(news_p)


# In[7]:


#combine both title and their bodies
results = soup.find_all('div', class_="slide")
for result in results:
    titles = result.find('div', class_="content_title")
    title = titles.find('a').text
    bodies = result.find('div', class_="rollover_description")
    body = bodies.find('div', class_="rollover_description_inner").text
    print('----------------')
    print(title)
    print(body)


# # JPL Mars Space Image
# * Visit the url for the Featured Space Image page here.
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# 
# * Make sure to find the image url to the full size .jpg image.
# 
# * Make sure to save a complete url string for this image.

# In[8]:


url = ('https://www.jpl.nasa.gov/images?query=&page=1&topics=Mars')

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# In[9]:


print(soup.prettify())


# In[10]:


images = soup.find_all('img', class_="BaseImage object-contain")
print(images)


# In[11]:


# pull image link
pic_src = []
for image in images:
    pic = image['data-src']

featured_image_url = pic
featured_image_url


# # Mars Facts
# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# 
# * Use Pandas to convert the data to a HTML table string.

# In[12]:


url = ('https://galaxyfacts-mars.com/')

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# In[13]:


print(soup.prettify())


# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.head()


# In[15]:


df.columns=['Description', 'Mars', 'Earth']
#drop earth column (not relevant)
df.drop('Earth', inplace=True, axis=1)
#drop first row (not relevant)
df.drop(index=df.index[0], axis=0, inplace=True)
#reset the index
df.set_index('Description', inplace=True)


# In[16]:


df.head()


# In[17]:


df.to_html()


# # Mars Hemisphere
# * Visit the Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[18]:


url = 'https://marshemispheres.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# In[19]:


print(soup.prettify())


# In[ ]:


browser.visit(url)


# In[ ]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):
    #create empty dictionary
    hemispheres = {}
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.links.find_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# In[ ]:


hemisphere_image_urls


# In[ ]:


browser.quit()


# In[24]:




