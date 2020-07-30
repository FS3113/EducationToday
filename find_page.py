from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup


def judge(urls):
    input_list = []
    f = open('input_list.txt', 'r')
    for i in f:
        if '\n' in i:
            i = i[:-1]
        input_list.append(i)

    print(input_list)

    for url in urls:
        print(url)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read()
        html = (str(html))

        keyword_found = 0
        for i in input_list:
            if i in html:
                print(i)
                keyword_found += 1
        print(keyword_found)
        if keyword_found == len(input_list):
            return url

    return '?'


def find_page_on_google(keyword):
    url = 'https://www.google.com/'
    chrome_option = Options()
    driver = webdriver.Chrome(executable_path='/Users/juefei/Desktop/Research/chromedriver', chrome_options=chrome_option)
    driver.get(url)
    input_tab = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    time.sleep(1)
    input_tab.send_keys(keyword, Keys.ENTER)
    elems = driver.find_elements_by_xpath("//a[@href]")
    possibleURLs = []
    for elem in elems:
        url = elem.get_attribute("href")
        if "google" not in url:
            possibleURLs.append(url)
    time.sleep(3)
    driver.quit()

    return judge(possibleURLs)


# print(find_page_on_google("uiuc faculty"))