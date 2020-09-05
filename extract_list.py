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


def get_raw_html(url):
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
            # driver1.quit()
        except:
            return ""

    return the_page


# given an url, get whole html in a good format (a list)
def get_html(url):
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


def view_html_structure(url):
    html = get_html(url)
    f = open('html_structure.txt', 'w')
    f1 = open('whole_html.txt', 'w')
    f2 = open('raw_html.txt', 'w')
    for i in html:
        f2.write(i + '\n')
    html_structure = []

    body_found = False
    count = 0
    for i in html:
        count += 1
        if not body_found:
            if '<body' in i:
                body_found = True
            else:
                continue
        f1.write(i + '\n')
        if len(i) == 0 or i[0] != '<':
            continue
        if ' ' in i:
            i = i[:i.index(' ')] + '>'
        if '\\n' in i:
            i = i[:i.index('\\n')] + '>'
        if '%' in i:
            i = i[:i.index('%')] + '>'
        f.write(i + str(count - 1) + '\n')
        html_structure.append([i, count - 1])
    f.close()

    root = [0]
    root.extend(html_structure[0])
    html_tree = [[root]]
    level = 0
    for i in html_structure[1: -1]:
        if '<!--' in i[0] or 'br' in i[0] or '\\' in i[0] or '<img' in i[0] or '<input' in i[0] or '<meta' in i[0] or '<hr>' in i[0]:
            continue
        if '/' != i[0][1]:
            level += 1
            if level > len(html_tree) - 1:
                html_tree.append([])
            html_tree[level].append([len(html_tree[level - 1]) - 1, i[0], i[1]])
        else:
            l = level
            try:
                while html_tree[level][-1][1] != '<' + i[0][2:]:
                    level -= 1
                    assert (level >= 0)
            except:
                level = l
                continue
            html_tree[level][-1].append(i[1])
            level -= 1


    for i in html_tree:
        print(i)

    max_children = 0
    max_parent = []
    for i in range(1, len(html_tree)):
        tmp = [0] * len(html_tree[i - 1])
        for j in html_tree[i]:
            tmp[j[0]] += 1
        tmp_max = max(tmp)
        if tmp_max > max_children:
            max_children = tmp_max
            max_parent = [i - 1, tmp.index(tmp_max)]

    print(max_children)
    print(max_parent)
    print(html_tree[max_parent[0]][max_parent[1]])

    result = []
    for i in html_tree[max_parent[0] + 1]:
        if i[0] == max_parent[1]:
            tmp = []
            for j in range(i[2], i[3]):
                line = html[j]
                if line[0] != '<':
                    line = line.replace('\\n', '')
                    line = line.replace('\\t', '')
                    line = line.replace('\\r', '')
                    line = line.replace('\n', '')
                    try:
                        while line[0] == ' ':
                            line = line[1:]
                        while line[-1] == ' ':
                            line = line[: -1]
                    except:
                        continue
                    if line != "":
                        tmp.append(line)
            result.append(tmp)

    return result


a = view_html_structure('https://dblp.uni-trier.de/pers?pos=1')
for i in a:
    print(i)

