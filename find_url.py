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
from get_data_from_multiple_lists import view_html_structure


def find(university, department):
    url = 'https://www.google.com/'
    option = webdriver.ChromeOptions()
    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')
    driver = webdriver.Chrome(executable_path='/Users/juefei/Desktop/EducationToday/chromedriver',
                              chrome_options=option)
    driver.get(url)
    input_tab = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    time.sleep(1)
    input_tab.send_keys(university + ' ' + department + ' faculty', Keys.ENTER)
    elems = driver.find_elements_by_xpath("//a[@href]")
    possibleURLs = []
    words = ['google', 'wiki', 'news', 'instagram', 'twitter', 'linkedin', 'criminal', 'student', 'course', 'facebook']
    n = 0
    for elem in elems:
        t = elem.get_attribute("href")
        flag = True
        for i in words:
            if i in t:
                flag = False
                break
        if flag:
            possibleURLs.append(t)
            n += 1
        if n == 10:
            break
    time.sleep(2)
    driver.quit()
    print(possibleURLs)

    res_data = {}
    res_url = ''
    res_num = 0
    for option in ['urllib', 'urllibs']:
        for url in possibleURLs:
            # print(option, url)
            try:
                r = view_html_structure(url, option)
            except:
                continue

            if len(r) < 8:
                continue
            valid_data = 0
            for i in r:
                for j in i.values():
                    if j != 'Missing':
                        valid_data += 1
            if len(r) >= 10 and valid_data / (5 * len(r)) > 0.56:
                return url, r
            if len(r) > 20 and valid_data / (5 * len(r)) > 0.36 and r[0]['Name'] != 'Missing':
                return url, r
            # print(valid_data)
            # print(len(r), r)
            if valid_data > res_num:
                res_url = url
                res_data = r.copy()
                res_num = valid_data
    return res_url, res_data


u = 'emory universiy'
a = 'computer science'
r1, r2 = find(u, a)
for i in r2:
    print(i)
print(r1)

# with open('Data/faculty_data/' + u + '/' + a + '.json', 'w') as f1:
#     json.dump(r2, f1, indent=4)

