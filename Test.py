# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 16:23:56 2021

@author: Karshil Sheth
"""

#### This program scrapes naukri.com's page and gives our result as a
#### list of all the job_profiles which are currently present there.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import csv
import os
import sys

#url of the page we want to scrape
url = "https://itdashboard.gov/"

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('K:/chromedriver')
driver.get(url)

# this is just to ensure that the page is loaded
time.sleep(5)

python_button = driver.find_element_by_link_text('DIVE IN')
python_button.click()
html = driver.page_source

# this renders the JS code and stores all of the information in static HTML code.

# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "html.parser")

list_header=[]
data = []
with open('output.csv', 'w', encoding='utf-8', newline='') as csvfile:
      fieldnames = ["Agency Name", "Agency Expense", "Agency Link"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      try:
        for div in soup.find_all(id='agency-tiles-container'):
            spans = div.find_all('span', {'class' : 'w900'})
            lines = [span.get_text() for span in spans]
            for line in lines:
                fund=line
                print(line)
            for img in div.find_all('img', alt=True):
                title=img['alt']
                print(img['alt'])
            for a in div.find_all('a', href=True):
                link=url+a['href']
                print (url+a['href'])          
                
            Table_dict={ 'Agency Name': title,'Agency Expense': lines, 'Agency Link' : link}
            data.append(Table_dict)
            writer.writerows(data)
            """ Table_dict={ 'Method': line,'Description':img['alt']}
            templist.append(Table_dict)
            df=pd.DataFrame(templist)
        df.to_csv('table_csv') """
      except NoSuchElementException:
      		print("Error Caught")

driver.close() # closing the webdriver
