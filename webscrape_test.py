from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

url = 'https://www.owgr.com/current-world-ranking'
driver = webdriver.Firefox()
driver.get(url)
golfers = []
wait = WebDriverWait(driver,5)

wait.until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(), 'Accept All Cookies')]")))
cookies = driver.find_element(By.XPATH,"//button[contains(text(), 'Accept All Cookies')]")
cookies.click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME,"table__link-column")))
soup = BeautifulSoup(driver.page_source, 'html.parser')
divs = soup.find_all('div', class_ = 'table__link-column')

for i in range(0,100):
    print(divs[i].text)
    golfers.append(divs[i].text)


for i in range(1,5):
    # click "next page" button
    xpath = "//a[@aria-label='Page {npage_no}']".format(npage_no = i+1)
    next_page = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
    driver.execute_script("arguments[0].click();", next_page)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table__link-column")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div', class_ = 'table__link-column')

    for i in range(0,100):
        # repeat above code to add next 100 golfers
        print(divs[i].text)
        golfers.append(divs[i].text)