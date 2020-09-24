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
# from google import google


f = open('Get_Departments/majors.txt', 'r')
department_dict = set()
for i in f.readlines():
    department_dict.add(i[:-1])
def check(s):
    a = s.replace('\\n', '').replace('\\t', '').replace('&amp;', '&').replace('&nbsp;', ' ')
    if '(' in a and ')' in a:
        a = a[:a.index('(')] + a[a.index(')') + 1:]
    a = re.split('\W+', a)
    while len(a) > 0 and a[-1] == '':
        del a[-1]
    match = 0
    for i in a:
        if i.lower() in department_dict:
            match += 1
    if len(a) == 0:
        return False
    if len(a) < 3:
        return match == len(a)
    if 3 <= len(a) < 6:
        return match >= len(a) - 1
    return match >= len(a) - 2


# given an url, get whole html in a good format (a list)
def getHTML(url):
    flag = False
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
           the_page = response.read()
        the_page = (str(the_page))
    except:
        # print("cannot crawl")
        flag = True

    # if flag:
    #     try:
    #         chrome_option = Options()
    #         driver1 = webdriver.Chrome(executable_path='/Users/juefei/Desktop/EducationToday/chromedriver',
    #                                    chrome_options=chrome_option)
    #         driver1.get(url)
    #         the_page = str(driver1.page_source)
    #         print(the_page)
    #         time.sleep(5)
    #         # driver1.quit()
    #     except:
    #         return ""

    result = []

    line = ""
    for i in the_page:
        if i == '<':
            if len(line) != 0:
                result.append(line)
            line = "<"
        elif i == '>':
            line += '>'
            result.append(line)
            line = ""
        else:
            line += i
    result.append(line)
    return result


# help creating the structure containing department names
def addHTML(html):
    if html[0] != '<':
        return ""
    if "http" in html:
        return html.split("http")[0]
    if "=" in html:
        return html.split("=")[0]
    return html


def deleteIrreleventInfo(info, check):
    i = 0
    start, end = [], []
    while i < len(info):
        if i >= len(info) - 7:
            break
        if ord(info[i + 1][0]) - ord(info[i][0]) <= 3 and ord(info[i + 2][0]) - ord(info[i + 1][0]) <= 3 \
            and ord(info[i + 3][0]) - ord(info[i + 2][0]) <= 3 and ord(info[i + 4][0]) - ord(info[i + 3][0]) <= 3\
            and ord(info[i + 5][0]) - ord(info[i + 4][0]) <= 3 and ord(info[i + 6][0]) - ord(info[i + 5][0]) <= 3:

            start.append(i)
            i += 1
            while i < len(info) and ord(info[i][0]) >= ord(info[i - 1][0]):
                i += 1
            end.append(i)
            i -= 1
        i += 1

    i = 1
    while i < len(start):
        if start[i] - end[i - 1] == 0 and ord(info[end[i - 1]][0]) >= ord(info[end[i - 1] - 2][0]):
            start.remove(start[i])
            end.remove(end[i - 1])
        else:
            i += 1

    for i in range(len(start)):
        flag1 = True
        for j in check:
            flag = False
            for k in info[start[i]: end[i]]:
                if j in k:
                    flag = True
                    break
            if flag == False:
                flag1 = False
                break
        if flag1:
            return info[start[i]: end[i]], True
    return info, False


def getDepartments(url):
    whole_html = getHTML(url)

    # print whole html to Output.txt
    s = ""
    for i in whole_html:
        s += i + '\n'
    with open("Output.txt", "w") as text_file:
        text_file.write(s)

    checkList = ["Mathematics", "Physics", "English", "Biology", "Media", "Computer",
                 "MATHEMATICS", "PHYSICS", "ENGLISH", "BIOLOGY", "MEDIA", "COMPUTER"]

    # store possible structures of html containing department name in a map
    possible_structure = {}
    for i in checkList:
        possible_structure[i] = []
    for i in range(len(whole_html)):
        for j in checkList:
            if j in whole_html[i] and possible_structure[j] == [] and len(whole_html[i]) < 170:
                # print(i, ": ", j)
                l = []
                l.extend([addHTML(whole_html[k]) for k in range(i - 3, i)])
                l.extend([addHTML(whole_html[k]) for k in range(i + 1, i + 4)])
                possible_structure[j] = l

    # checkItem: strcture of html containing department name (three lines of html above the department name, and
    # three lines of html below the department name)
    checkItem = []
    for i in range(len(checkList)):
        for j in range(i + 1, len(checkList)):
            # print(possible_structure[checkList[i]], possible_structure[checkList[j]])
            if possible_structure[checkList[i]] == possible_structure[checkList[j]] and possible_structure[checkList[i]] != []:
                checkItem = possible_structure[checkList[i]]
                break

    # print(possible_structure)

    if checkItem == []:
        return []

    allDepartments = []

    for i in range(len(whole_html) - len(checkItem)):
        same = 0
        if whole_html[i][:len(checkItem[0])] == checkItem[0]:
            same += 1
        if whole_html[i + 1][:len(checkItem[1])] == checkItem[1]:
            same += 1
        if whole_html[i + 2][:len(checkItem[2])] == checkItem[2]:
            same += 1
        if whole_html[i + 4][:len(checkItem[3])] == checkItem[3]:
            same += 1
        if whole_html[i + 5][:len(checkItem[4])] == checkItem[4]:
            same += 1
        if whole_html[i + 6][:len(checkItem[5])] == checkItem[5]:
            same += 1
        if same > 5:
            found  = whole_html[i + 3]
            while found[0] == " ":
                found = found[1:]
            if found[0] != '<' and len(found.split(" ")) < 8 and "Professor" not in found:
                allDepartments.append(found)

    # for i in allDepartments:
    #     print(i)

    check = []
    for i in possible_structure.keys():
        if possible_structure[i] == checkItem:
            check.append(i)
    allDepartments, use = deleteIrreleventInfo(allDepartments, check)

    # for i in allDepartments:
    #     print(i)

    # print(use)

    return allDepartments


def find(keywords):
    url = 'https://www.google.com/'
    chrome_option = Options()
    driver = webdriver.Chrome(executable_path='/Users/juefei/Desktop/EducationToday/chromedriver',
                              chrome_options=chrome_option)
    driver.get(url)
    input_tab = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    time.sleep(1)
    input_tab.send_keys(keywords, Keys.ENTER)
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

    # search_results = google.search(keywords, 1)
    # possibleURLs = []
    # for i in search_results:
    #     possibleURLs.append(i.link)
    return possibleURLs


def get_department_by_university_name(university):
    urls = find(university + ' majors')
    for url in urls:
        try:
            r = getDepartments(url)
        except:
            continue
        res = []
        count = 0
        for j in r:
            if check(j):
                count += 1
            res.append(j)
        if count / (len(res) + 0.0001) > 0.7:
            return res
    return []


r = get_department_by_university_name('mit')
for i in r:
    print(i)
