from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

url = 'https://www.owgr.com/current-world-ranking'
driver = webdriver.Firefox()
driver.get(url)

wait = WebDriverWait(driver,10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table__link-column")))

soup = BeautifulSoup(driver.page_source, 'html.parser')
divs = soup.find_all('div', class_ = 'table__link-column')

golfers = []

for i in range(0,500):
    print(divs[i].text)
    golfers.append(divs[i].text)