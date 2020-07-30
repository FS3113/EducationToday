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


# given an url, get whole html in a good format (a list)
def get_html(url):
    flag = False
    faculty_image = []
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        the_page = (str(the_page))
    except:
        print("cannot crawl")
        flag = True

    flag = True
    if flag:
        try:
            chrome_option = Options()
            driver1 = webdriver.Chrome(executable_path='/Users/juefei/Desktop/Research/chromedriver',
                                       chrome_options=chrome_option)
            driver1.get(url)
            the_page = str(driver1.page_source)
            # images = driver1.find_elements_by_tag_name('img')
            # for image in images:
            #     faculty_image.append(image.get_attribute('src'))
            time.sleep(5)
        except:
            return ""

    # urllib.request.urlretrieve('https://gps.ucsd.edu/_images/people/faculty/faculty_feinberg.jpg', "filename.png")
    # for i in range(len(faculty_image)):
    #     print(faculty_image[i])
    #     urllib.request.urlretrieve(faculty_image[i], 'Faculty_Image/' + str(i) + '.png')

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
    return result, faculty_image


def view_html_structure(url, wrong_common_sturcutre = []):
    html, faculty_images = get_html(url)
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
        if i != ' ' and i[0] != '<' and 0 < j < len(html) - 1 and (html[j + 1][:2] != '</' or html[j - 1][:2] == '</' or html[j - 1][:3] == '<br'):
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
    for i in raw_html:
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
        if '<!--' in i[0] or 'br' in i[0] or '\\' in i[0] or '<img' in i[0] or '<input' in i[0] or '<meta' in i [0] or '<hr>' in i[0]:
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
                    flag = True
                    for j in wrong_common_sturcutre:
                        if list(p)[:len(j)] == j:
                            flag = False
                            break
                    if r == 'Name' or r == 'Position' or r == 'Research Interest':
                        for j in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Email', 'Phone', 'Homepage', '@']:
                            if j in raw_html[html_tree[level][i][2] + 1]:
                                flag = False
                                break
                    if len(raw_html[html_tree[level][i][2] + 1]) < 3:
                        flag = False
                    if flag:
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
            print(i, j, raw_html[html_tree[n - 1][k][2] + 1], t, html_tree[n - 1][k])
            # print(i, raw_html[html_tree[n - 1][k][2] + 1])

    candidate_num = sum([len(path_dict[i]) for i in path_dict.keys()])
    common_structure = []
    a = 0
    while True:
        count = {}
        for i in path_dict.keys():
            for j in path_dict[i]:
                if a >= len(j) or j[: len(common_structure)] != common_structure:
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
        try:
            print(a[0][0], i)
            each_structure[i] = a[0][0]
        except:
            print('No ' + i)
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
            try:
                if i[4] == n:
                    root = i.copy()
            except:
                return []
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


    subtree_dict = {}
    for i in subtree_roots:
        if get_subtree(i[-1]) != []:
            subtree_dict[i[-1]] = get_subtree(i[-1]).copy()
    print(subtree_dict)

    for i in subtree_dict.keys():
        subtree_dict[i][0].append(str(subtree_dict[i][0][-1]) + '-')
        subtree_dict[i][0] = [subtree_dict[i][0].copy()]
        for j in range(1, len(subtree_dict[i])):
            tag_class_names = []
            for node in subtree_dict[i][j]:
                tag = node[1]
                for k in subtree_dict[i][j - 1]:
                    if k[-2] == node[0]:
                        tag = k[1] + tag
                        node.append(k[-1] + str(node[-1]) + '-')
                a = raw_html[node[2]]
                if 'class=' in a:
                    a = a[a.index('class=') + 6:]
                    if ' id' in a:
                        a = a[: a.index(' id')]
                    if ' href' in a:
                        a = a[: a.index(' href')]
                    if ' about' in a:
                        a = a[: a.index(' about')]
                    if ' typeof' in a:
                        a = a[: a.index(' typeof')]
                    else:
                        a = a[: -2]
                    tag = tag[: -1] + ' ' + a + '>'
                while tag in tag_class_names:
                    tag = tag[:-1] + '@' + '>'
                tag_class_names.append(tag)

                node[1] = tag

    # print(subtree_dict)
    
    translation = {}
    for i in subtree_dict.keys():
        for j in subtree_dict[i]:
            for k in j:
                translation[k[-1]] = k[1]
                
    subtree_path = {}
    for i in path_dict.keys():
        subtree_path[i] = {}
        for j in path_dict[i]:
            a = ''
            for k in range(len(common_structure), len(j)):
                a += str(j[k]) + '-'
            try:
                if translation[a] not in subtree_path[i].keys():
                    subtree_path[i][translation[a]] = 0
                subtree_path[i][translation[a]] += 1
            except:
                continue

    print(subtree_path)

    # for i in subtree_path.keys():
    #     for j in wrong_path[i]:
    #         if j in subtree_path[i].keys():
    #             subtree_path[i][j] = 0

    for x in range(3):
        for i in subtree_path.keys():
            for j in subtree_path.keys():
                if i != j:
                    try:
                        a, b = max(subtree_path[i], key=subtree_path[i].get), max(subtree_path[j], key=subtree_path[j].get)
                    except:
                        continue
                    if a == b:
                        # a1 = subtree_path[i][a] / (sum(subtree_path[i].values()) + 1)
                        # b1 = subtree_path[j][b] / (sum(subtree_path[j].values()) + 1)
                        a1 = subtree_path[i][a]
                        b1 = subtree_path[j][b]
                        if a1 > b1:
                            subtree_path[j][a] = 0
                        else:
                            subtree_path[i][a] = 0
    print(subtree_path)

    for i in subtree_path.keys():
        if len(subtree_path[i].keys()) == 0 or subtree_path[i][max(subtree_path[i], key=subtree_path[i].get)] == 0:
            subtree_path[i] = 'None'
        else:
            subtree_path[i] = max(subtree_path[i], key=subtree_path[i].get)


    print(subtree_path)

    path_to_result = {}
    for i in subtree_dict.keys():
        path_to_result[i] = {}
        for j in subtree_dict[i]:
            for k in j:
                path_to_result[i][k[1]] = [k[2], k[3]]

    result = []
    total_miss, total_num = 0, 0
    for i in path_to_result.keys():
        d = {}
        missing = 0
        for j in subtree_path.keys():
            p = subtree_path[j]
            if p not in path_to_result[i].keys():
                p = p[:p.rfind('<')]
                if p in path_to_result[i].keys() and path_to_result[i][p][1] - path_to_result[i][p][0] > 2:
                    p = subtree_path[j]
            if p not in path_to_result[i].keys():
                p = p[:p.rfind('<')]
                if p in path_to_result[i].keys() and path_to_result[i][p][1] - path_to_result[i][p][0] > 2:
                    p = subtree_path[j]
            if p in path_to_result[i].keys():
                a = ''
                for k in range(path_to_result[i][p][0], path_to_result[i][p][1]):
                    if raw_html[k][0] != '<':
                        a += raw_html[k] + '  '
                print(j + ': ' + a)
                d[j] = a
            else:
                print(j + ': missing')
                d[j] = 'Missing'
                missing += 1
        print()
        # root_tag = subtree_path['Name'][: subtree_path['Name'].find('>') + 1]
        # l = path_to_result[i][root_tag].copy()

        # image_src = '?'
        # for j in range(l[0], l[1] + 1):
        #     if raw_html[j][:5] == '<img ':
        #         img = raw_html[j]
        #         a = img[img.find('src=\"') + 5:]
        #         a = a[:a.find('\"')]
        #         # print(a)
        #         if a[:2] == '..':
        #             a = a[2:]
        #         for k in range(len(faculty_images)):
        #             if a in faculty_images[k]:
        #                 image_src = str(k)
        #                 break
        # print(image_src)
        # print(faculty_images)
        # image_src += '.png'
        # d['Image'] = image_src
        if missing < 3:
            result.append(d.copy())
        total_miss += missing
        total_num += 3
    print(subtree_path)
    wrong = wrong_common_sturcutre.copy()
    wrong.append(common_structure.copy())
    if total_miss / total_num > 0.55:
        print('Total Miss:', total_miss, '  Num: ', total_num)
        return view_html_structure(url, wrong)

    return result, subtree_path


# view_html_structure('https://www.cc.gatech.edu/people/faculty')
# view_html_structure('https://engineering.dartmouth.edu/people/faculty/core/')
# view_html_structure('https://sils.unc.edu/directory/faculty')
# view_html_structure('https://www.cs.cornell.edu/people/faculty')

# positions are misclassified as research interests:
# view_html_structure('http://www.bbe.caltech.edu/people?cat_one=Faculty&cat_two=all')

# research interests for each faculty are separated under different tags
# view_html_structure('http://cce.caltech.edu/people?cat_one=faculty&cat_two=all')

# variation in structures (to do)
# view_html_structure('http://www.hss.caltech.edu/people?cat_one=Professorial%20Faculty&cat_two=all')
# view_html_structure('http://www.hss.caltech.edu/people?cat_one=Professorial%20Faculty&cat_two=all')

# view_html_structure('https://architecture.mit.edu/people')
# print(random_forest_model.predict([vectorize(('Balibanu, Ana'))]))
# print(random_forest_model.predict([vectorize(('SC 532g'))]))
# print(random_forest_model.predict([vectorize(('Computer Science'))]))

def collect_data(url, name='1', wrong_path={'Name': [], 'Position': [], 'Research Interest': []}):
    result, path = view_html_structure(url, wrong_path)
    print(wrong_path)
    user_input = input('Input (Name: 1, Position: 2, Research Interest: 3): ')
    if user_input == 'p':
        f = open('Faculty/MIT/' + name + '.txt', 'w')
        for i in result:
            if i['Name'] == 'Missing':
                continue
            for j in i.keys():
                f.write(j + ': ' + i[j] + '\n')
            f.write('\n')
        return
    user_input = user_input.split(' ')
    d = {'1': 'Name', '2': 'Position', '3': 'Research Interest'}
    if len(user_input) >= 2:
        wrong_path[d[user_input[1]]].append(path[d[user_input[1]]])
    if len(user_input) == 3:
        f1 = open('negative.txt', 'a')
        for i in result:
            print(i[d[user_input[1]]])
            f1.write(i[d[user_input[1]]] + '\n')
    collect_data(url, name, wrong_path.copy())

# collect_data('https://chemistry.mit.edu/faculty/', 'Chemistry')

# Brain and Cognitive Sciences
# Chemistry

# driver = webdriver.Chrome(executable_path='/Users/juefei/Desktop/Research/chromedriver',
#                                        chrome_options=Options())
# driver.get('https://gps.ucsd.edu/faculty-research/faculty.html')
# images = driver.find_elements_by_tag_name('img')
# for image in images:
#     print(image.get_attribute('src'))
#
# driver.close()
# urllib.request.urlretrieve('https://gps.ucsd.edu/_images/people/faculty/faculty_feinberg.jpg', "filename.png")
# print(images)

view_html_structure('https://math.yale.edu/people/all-faculty')