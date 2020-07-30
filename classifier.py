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
import enchant
import numpy as np


english_dictionary = enchant.Dict("en_US")


def get_string_in_html(url):
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

    f = open('html_string.txt', 'w')
    for i in result:
        f.write(i + '\n')

    return result


def build_dict():
    f = open('faculty_list.txt', 'r')
    info_dict = {'Name': {'english': [], 'number': [], 'length': [], 'match': {}},
                 'Position': {'english': [], 'number': [], 'length': [], 'match': {}},
                 'Research Interest': {'english': [], 'number': [], 'length': [], 'match': {}}}
    for i in f.readlines():
        if ': ' not in i:
            continue
        c = i[:i.index(': ')]
        strings = i[i.index(': ') + 2:].split()
        info_dict[c]['length'].append(len(strings))
        english, number = 0, 0
        # s = re.sub(r'[,.?:;!\']', '', s)
        for j in strings:
            if j in info_dict[c]['match'].keys():
                info_dict[c]['match'][j] += 1
            else:
                info_dict[c]['match'][j] = 1
            if j.isnumeric():
                number += 1
            elif english_dictionary.check(j):
                english += 1
        info_dict[c]['english'].append(english)
        info_dict[c]['number'].append(number)

    return info_dict


def build_statistical_dict(dict):
    stat_dict = {}
    for i in dict.keys():
        tmp_dict = {'english': 0, 'number': 0, 'length': 0}
        for j in ['english', 'number', 'length']:
            tmp_dict[j] = [np.mean(np.array(dict[i][j])), np.std(np.array(dict[i][j]))]
            if tmp_dict[j][1] == 0:
                tmp_dict[j][1] = 0.01
        stat_dict[i] = tmp_dict.copy()
    return stat_dict


info_dict = build_dict()
stat_dict = build_statistical_dict(info_dict)
f = open('faculty_list.txt', 'r')
comparing_dict = {'Name': [], 'Position': [], 'Research Interest': []}
for i in f.readlines():
    if ': ' not in i:
        continue
    c = i[:i.index(': ')]
    strings = i[i.index(': ') + 2:].split()
    count_s = {'english': 0, 'number': 0, 'length': len(strings)}
    for j in strings:
        if j.isnumeric():
            count_s['number'] += 1
        elif english_dictionary.check(j):
            count_s['english'] += 1
    value = 1
    for j in strings:
        if j in info_dict[c]['match'].keys():
            value += info_dict[c]['match'][j]
    value /= sum(info_dict[c]['match'].values())
    tmp = 0
    for j in stat_dict[c].keys():
        tmp += (abs((count_s[j] - stat_dict[c][j][0])))
    value /= tmp
    comparing_dict[c].append(value)
common_words = {'Name': [], 'Position': [], 'Research Interest': []}
for i in info_dict.keys():
    s = sum(info_dict[i]['match'].values())
    for j in info_dict[i]['match'].keys():
        if info_dict[i]['match'][j] / s > 0.18:
            common_words[i].append(j)
print(common_words)

stat_comparing_dict = {'Name': [0, 0], 'Position': [0, 0], 'Research Interest': [0, 0]}
for i in comparing_dict.keys():
    stat_comparing_dict[i][0] = np.mean(np.array(comparing_dict[i]))
    stat_comparing_dict[i][1] = np.std(np.array(comparing_dict[i]))

print(info_dict)
print(stat_dict)
def classify(s):
    a = s.split(' ')
    # for i in a:
    #     flag = True
    #     for j in info_dict.keys():
    #         if i not in info_dict[j]['match'].keys():
    #             flag = False
    #     if flag:
    #         return j
    count = {'english': 0, 'number': 0, 'length': len(a)}
    for i in a:
        try:
            if i.isnumeric():
                count['number'] += 1
            elif english_dictionary.check(i):
                count['english'] += 1
        except:
            x = 1

    result = []
    for i in stat_dict.keys():
        value = 1

        for j in a:
            if j in info_dict[i]['match'].keys():
                value += info_dict[i]['match'][j]
        value /= sum(info_dict[i]['match'].values())

        tmp = 0
        for j in stat_dict[i].keys():
            tmp += (abs((count[j] - stat_dict[i][j][0])))
        value /= tmp
        # print(value)
        result.append([i, value])

    result = sorted(result, key=lambda x: x[1], reverse=True)
    value, tag = result[0][1], result[0][0]
    # print(stat_comparing_dict)
    lower = stat_comparing_dict[tag][0] - 0.66 * stat_comparing_dict[tag][1]
    lower = lower if lower > 0 else stat_comparing_dict[tag][0] / 4
    if lower < value < stat_comparing_dict[tag][0] + 0.8 * stat_comparing_dict[tag][1]:
        return tag
    return 'None'


# [english, number, length, match]

# get_string_in_html('https://be.mit.edu/directory')
# print(english_dictionary.check('felix'))
# a = build_dict()
# b = build_statistical_dict(a)
# print(b)
r = classify("Dean and Qualcomm Endowed Chair in Communications and Technology Policy")
print(r)
print('Assistant' in info_dict['Research Interest']['match'].keys())

input = get_string_in_html('https://directory.illinois.edu/facultyListing')
for i in input:
    s = i.split()
    c = classify(i)
    if c == 'None':
        continue
    flag = True
    for j in common_words[c]:
        if j not in i:
            flag = False
            break
    for j in common_words.keys():
        if j != c:
            for k in common_words[j]:
                if k in i:
                    flag = False
    if flag:
        print(classify(i) + ':', i)

print(classify('computer science'))
