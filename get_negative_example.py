import json
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import numpy as np


def get_negative(url):
    f = open('faculty_list.txt', 'r')
    correct = ''
    for i in f.readlines():
        if len(i) > 3:
            correct += i
    flag = False
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        the_page = (str(the_page))
    except:
        print("cannot crawl")
        flag = True

    if flag:
        try:
            chrome_option = Options()
            driver1 = webdriver.Chrome(executable_path='/Users/juefei/Desktop/Research/chromedriver',
                                       chrome_options=chrome_option)
            driver1.get(url)
            the_page = str(driver1.page_source)
            time.sleep(5)
        except:
            return ""

    result = []
    line = ""
    flag = True
    for i in the_page:
        if i == '<':
            while len(line) > 1 and line[0] == '\\' and line[1] == 'n':
                line = line[2:]
            line = ' '.join(line.split())
            while len(line) > 1 and line[0] == '\\' and line[1] == 'n':
                line = line[2:]
            if len(line) != 0 and line[0] != '<' and line != '\\n':
                line.replace(',', '')
                result.append(line)
            line = ''
            flag = False
        elif i == '>':
            flag = True
        elif flag:
            line += i
    line.replace(',', '')
    result.append(line)

    f = open('negative.txt', 'a')
    for i in result:
        i = i.replace('\\n', '')
        i = i.replace('\\t', '')
        print(i)
        if len(i) > 0 and i not in correct:
            f.write(i + '\n')

    return result


get_negative('https://www.purdue.edu/')
