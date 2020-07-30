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
import pickle
from random_forest import vectorize
import string

random_forest_model = pickle.load(open('random_forest_model.sav', 'rb'))


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
    raw_html = []
    for j in range(len(html)):
        i = html[j]
        i = i.replace('\\n', '')
        i = i.replace('\\t', '')
        i = i.replace('\\r', '')
        i = i.replace('&nbsp;', '')
        while '  ' in i:
            i = i.replace('  ', ' ')
        if len(i) == 0 or i == ';':
            i = ' '
        if i != ' ' and i[0] != '<' and 0 < j < len(html) - 1 and (
                html[j + 1][:2] != '</' or html[j - 1][:2] == '</' or html[j - 1][:3] == '<br'):
            a = i.strip()
            if a in string.punctuation:
                continue
            raw_html.append('<no_tag>')
            raw_html.append(i)
            raw_html.append('</no_tag>')
            f2.write('<no_tag>\n')
            f2.write(i + '\n')
            f2.write('</no_tag>\n')
        else:
            raw_html.append(i)
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
        if '<!--' in i[0] or 'br' in i[0] or '\\' in i[0] or '<img' in i[0] or '<input' in i[0] or '<meta' in i[0]:
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
                    # print(html_tree[level][-1])
                    # print(i)
            except:
                level = l
                continue
            html_tree[level][-1].append(i[1])
            level -= 1
    for i in html_tree:
        print(len(i), i)

    path_dict = {}
    tmp = []
    for level in range(len(html_tree) - 1, -1, -1):
        update_tmp = []
        for i in range(len(html_tree[level])):
            if html_tree[level][i][0] not in update_tmp:
                update_tmp.append(html_tree[level][i][0])
            if i not in tmp:
                # print(raw_html[html_tree[level][i][2] + 1])
                if raw_html[html_tree[level][i][2] + 1][0] == '<' or raw_html[html_tree[level][i][2] + 1] == ' ':
                    continue
                r = random_forest_model.predict([vectorize(raw_html[html_tree[level][i][2] + 1])])[0]
                if r != 'None':
                    # print(raw_html[html_tree[level][i][2] + 1], r)
                    p = []
                    t = level
                    n = html_tree[t][i][0]
                    while t >= 1:
                        # print(p, t, n, len(html_tree[t - 1]))
                        p.append(n)
                        t -= 1
                        n = html_tree[t][n][0]
                    # p.append(n)
                    if r not in path_dict.keys():
                        path_dict[r] = []
                    p = p[::-1]
                    p.append(i)
                    path_dict[r].append(list(p).copy())

        tmp = update_tmp.copy()
    print(path_dict)

    for i in path_dict.keys():
        for j in path_dict[i]:
            t = []
            n = 0
            for k in j:
                t.append(html_tree[n][k][1])
                n += 1
            print(i, j, t, html_tree[n - 1][k], raw_html[html_tree[n - 1][k][2] + 1])

    candidate_num = sum([len(path_dict[i]) for i in path_dict.keys()])
    common_structure = []
    a = 0
    while True:
        count = {}
        for i in path_dict.keys():
            for j in path_dict[i]:
                if a >= len(j):
                    continue
                if j[a] not in count.keys():
                    count[j[a]] = 0
                count[j[a]] += 1
        t = []
        for i in count.keys():
            t.append([i, count[i]])
        t = sorted(t, key=lambda x: x[1], reverse=True)
        if t[0][1] > 0.2 * candidate_num:
            common_structure.append(t[0][0])
        else:
            break
        a += 1
    print(common_structure)

    l = len(common_structure)
    for i in path_dict.keys():
        a = []
        for j in path_dict[i]:
            if j[:l] == common_structure:
                a.append(j.copy())
        path_dict[i] = a.copy()
    print(path_dict)

    dict_for_building_subtree = {}
    each_structure = {}
    for i in path_dict.keys():
        d = {}
        dict_for_building_subtree[i] = []
        each_structure[i] = []
        for j in path_dict[i]:
            t = ""
            n = 0
            for k in j:
                t += html_tree[n][k][1]
                n += 1
            if t not in d.keys():
                d[t] = 0
            d[t] += 1
            print(i, j, t, html_tree[n - 1][k], raw_html[html_tree[n - 1][k][2] + 1])
            dict_for_building_subtree[i].append([j.copy(), t])
        a = []
        for j in d.keys():
            a.append([j, d[j]])
        a = sorted(a, key=lambda x: x[1], reverse=True)
        print(a[0][0], i)
        each_structure[i] = a[0][0]
    print(common_structure)

    subtree_roots = []
    for i in range(len(html_tree[len(common_structure)])):
        if html_tree[len(common_structure)][i][0] == common_structure[-1]:
            t = html_tree[len(common_structure)][i].copy()
            t.append(i)
            subtree_roots.append(t)
    print(subtree_roots)

    def get_subtree(n):
        root = []
        for i in subtree_roots:
            if i[4] == n:
                root = i.copy()
        if len(root) == 0:
            return []
        result = [root.copy()]
        level = len(common_structure) + 1
        pre = [root.copy()]
        while True:
            t = []
            for i in pre:
                if level > len(html_tree) - 1:
                    continue
                for j in range(len(html_tree[level])):
                    # print(j, i)
                    if len(i) != 5:
                        continue
                    if html_tree[level][j][0] == i[4]:
                        a = html_tree[level][j].copy()
                        a.append(j)
                        t.append(a.copy())
            if len(t) == 0:
                break
            pre = t.copy()
            level += 1
            result.append(t.copy())
        return result

    print(get_subtree(24))

    subtree_dict = {}
    for i in subtree_roots:
        subtree_dict[i[-1]] = get_subtree(i[-1]).copy()
    print(subtree_dict)
    
    subtree_path = {}
    for i in each_structure.keys():
        subtree_path[i] = []
        d = {}
        for j in dict_for_building_subtree[i]:
            if j[1] != each_structure[i]:
                continue
            a = j[0][-1]
            subtree = subtree_dict[j[0][len(common_structure)]]
            level = len(subtree) - 1
            path = ''
            while level > 0:
                x1, x2 = -1, -1
                for k in range(len(subtree[level])):
                    if subtree[level][k][-1] == a:
                        x2 = k
                        b = subtree[level][k][0]
                        # print(a, b)
                        a = b
                        for l in range(len(subtree[level])):
                            if subtree[level][l][0] == b:
                                x1 = l
                                break
                if x1 != -1:
                    # print(x1, x2)
                    path += str(x2 - x1) + ' '
                level -= 1
            # print(subtree)
            # print(path, j, i)
            # print()
            if path not in d.keys():
                d[path] = 0
            d[path] += 1
        # l = []
        # for j in d.keys():
        #     l.append([j, d[j]])
        # l = sorted(l, key=lambda x: x[1], reverse=True)
        # r = l[0][0].split()
        subtree_path[i] = d.copy()
    print(subtree_path)

    for i in subtree_path.keys():
        d = {}
        print(i)
        for j in subtree_path[i].keys():
            a = j[j.index(' ') + 1:]
            print(a)
            if a not in d.keys():
                d[a] = 0
            d[a] += 1
        print(d)
        print()
        if ' ' not in max(d, key=d.get)[:-1]:
            continue
        if max(d.values()) > 0.7 * sum(d.values()) and len(subtree_path[i].keys()) > 3:
            new_d = {}
            m = max(d, key=d.get)
            for j in subtree_path[i].keys():
                t = m if m in j else j
                if t not in new_d.keys():
                    new_d[t] = 0
                new_d[t] += subtree_path[i][j]
            subtree_path[i] = new_d.copy()
    print(subtree_path)

    # for i in subtree_path.keys():
    #     for j in subtree_path.keys():
    #         if i != j:
    #             a, b = max(subtree_path[i], key=subtree_path[i].get), max(subtree_path[j], key=subtree_path[j].get)
    #             if a == b:
    #                 a1 = subtree_path[i][a] / sum(subtree_path[i].values())
    #                 b1 = subtree_path[j][b] / sum(subtree_path[j].values())
    #                 if a1 > b1:
    #                     subtree_path[j][a] = 0
    #                 else:
    #                     subtree_path[i][a] = 0
    # print(subtree_path)
    for i in subtree_path.keys():
        a = max(subtree_path[i], key=subtree_path[i].get)
        a = a.split()
        subtree_path[i] = a[::-1].copy()
    print(subtree_path)

    for i in subtree_dict.values():
        # print(i)
        for j in subtree_path.keys():
            try:
                a = i[0][-1]
                r = []
                for k in range(len(subtree_path[j])):
                    kk = int(subtree_path[j][k])
                    xx = 0
                    for x in range(len(i[k + 1])):
                        if i[k + 1][x][0] == a:
                            a = i[k + 1][x + kk][-1]
                            xx = x + kk
                    if k == len(subtree_path[j]) - 1:
                        r = [i[k + 1][xx][2], i[k + 1][xx][3]]
                f = ""
                for k in range(r[0], r[1]):
                    if raw_html[k][0] != '<':
                        f += raw_html[k] + ' '
                print(j + ':', f)
            except:
                print(j + ': missing')
        print()


# view_html_structure('https://gps.ucsd.edu/faculty-research/faculty.html')
# view_html_structure('https://engineering.dartmouth.edu/people/faculty/core/')
# view_html_structure('https://sils.unc.edu/directory/faculty')
# view_html_structure('https://www.cs.cornell.edu/people/faculty')

# positions are misclassified as research interests:
# view_html_structure('http://www.bbe.caltech.edu/people?cat_one=Faculty&cat_two=all')

# research interests for each faculty are separated under different tags
# view_html_structure('http://cce.caltech.edu/people?cat_one=faculty&cat_two=all')

# variation in structures (to do)
# view_html_structure('http://www.hss.caltech.edu/people?cat_one=Professorial%20Faculty&cat_two=all')
# view_html_structure('http://pma.divisions.caltech.edu/people?cat_one=Professorial%20Faculty&cat_two=all'https://chemistry.mit.edu/faculty/)

view_html_structure('https://chemistry.mit.edu/faculty/')

