from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import pandas as pd

class Rappler:
    driver = webdriver.Chrome('chromedriver.exe')
    url = 'https://www.rappler.com/topic/2022-philippine-elections/'

    driver.get(url)
    driver.maximize_window()

    #loading all website content
    i = 0;
    element = driver.find_element(By.XPATH, '//button[contains(text(), "Load More")]')
    time.sleep(3)
    alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "ALLOW")]'))).click()
    while 1:
    #for i in range(5):
        try:
            i += 1;
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(2)
            alert = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Load More")]'))).click()
            print(f'Iteration: {i}')
        except:
            break

    time.sleep(5)

    #getting news title and upload date
    news = driver.find_elements_by_tag_name('h3')
    dates = driver.find_elements_by_tag_name('time')
    title = []
    time = []
    for new, date in zip(news, dates):
        title.append(new.text)
        time.append(date.text)

    #getting link/href for each news
    anchors = driver.find_elements_by_tag_name('a')
    links = []
    i = 0
    for anchor in anchors:
        try:
            if anchor.text == title[i]:
                links.append(anchor.get_attribute('href'))
                i += 1
        except:
            break

    #getting author
    authors = []
    for link in links:
        html_text = requests.get(link).text
        auth = BeautifulSoup(html_text, 'lxml')
        # authors.append(driver.find('a', class_='A-sc-120nwt8-1 ListAuthor__ListAuthors-sc-15js12l-1 jZXTrG')).text

        try:
            try:
                author = auth.find('a', class_='A-sc-120nwt8-1 ListAuthor__ListAuthors-sc-15js12l-1 bTrYxg').text
            except:
                author = auth.find('a', class_='A-sc-120nwt8-1 ListAuthor__ListAuthors-sc-15js12l-1 jZXTrG').text
        except:
            author = 'Not Available'
        authors.append(author)

    #dataframe to csv file
    rappler = pd.DataFrame(zip(title, time, authors, links), columns=["Title", "Date", "Publisher", "Website"])
    rappler.to_csv("rappler.csv")
    print(rappler)
