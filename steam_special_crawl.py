# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 21:20:15 2024

@author: ASUS
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException
chrome_options=Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver=webdriver.Chrome(options=chrome_options)
driver.get('https://store.steampowered.com/specials#tab=TopSellers')
time.sleep(5)
#set up the loading bar 
pbar = tqdm(range(500), desc="Processing", dynamic_ncols=True,bar_format="{l_bar}{bar}| {percentage:3.0f}%")
#try to scroll down to botton and click "see more" button 500 times， if the button is no longer availiable then exit the loop
for i in pbar:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    try:
        locater=(By.CLASS_NAME,'_2tkiJ4VfEdI9kq1agjZyNz.Focusable')
        WebDriverWait(driver,20).until(EC.presence_of_element_located(locater))
    except TimeoutException:
        pbar.n = pbar.total  
        pbar.last_print_n = pbar.total  
        pbar.refresh()
        break
    btn=driver.find_element(By.CLASS_NAME,'_2tkiJ4VfEdI9kq1agjZyNz.Focusable')
    btn.click()
    time.sleep(1)
#get the page source
r=driver.page_source
driver.quit()
soup=bs(r,'html.parser')
titles=soup.select('._18byEIHFiivSklOwKqIx2b ._3rrH9dPdtHVRMzAEw82AId')
prices=soup.select('._18byEIHFiivSklOwKqIx2b ._3j4dI1yA7cRfCvK8h406OB')
discounts=soup.select('._18byEIHFiivSklOwKqIx2b .cnkoFkzVCby40gJ0jGGS4')
reviews=soup.select('._18byEIHFiivSklOwKqIx2b ._2nuoOi5kC2aUI12z85PneA')

n=1 #initialise place of best seller
titles_list=[] #initialise game title list
discounts_list=[] #initialise discount list
prices_list=[] #initialise discounted priced list
place_list=[] #initialise place of best seller list
reviews_list=[] #initialise reviews list
for title,price,discount,review in zip(titles,prices,discounts,reviews):
    print(f'特價銷售第{n}:',title.text,discount.text,price.text,review.text)
    titles_list.append(title.text)
    prices_list.append(price.text)
    discounts_list.append(discount.text)
    place_list.append(n)    
    reviews_list.append(review.text)
    n+=1
#save into DataFrame
data=pd.DataFrame({'title':titles_list,'price':prices_list,'discount':discounts_list,'review':reviews_list,'place':place_list})
