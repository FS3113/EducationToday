import json
import urllib.request
from urllib.request import urlopen
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECg
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import pickle
from collections import defaultdict
import string
from find_possible_list_department import find_possible_list
from find_possible_list import handle_extreme_edge_case
import os


f = open('Get_Departments/majors.txt', 'r')
department_dict = set()
for i in f.readlines():
    department_dict.add(i[:-1])
wrong_words = ['school', 'department', 'center', 'major', 'college', 'life', 'education', 'requirement', 'university',
               'curriculum', 'office', 'advising', 'about', 'student', 'program', 'division', 'project', 'learning',
               'academics', 'family']
def check(s):
    s = s.lower()
    for i in wrong_words:
        if i in s:
            return False
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
def get_html(url, scrape_option):
    # flag = False
    the_page = ''
    if scrape_option == 'urllib':
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
            the_page = (str(the_page))
        except:
            return []
    else:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument(' — incognito')
            option.add_argument('--no - sandbox')
            option.add_argument('--window - size = 1420, 1080')
            option.add_argument('--headless')
            option.add_argument('--disable - gpu')
            driver1 = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver', chrome_options=option)
            driver1.get(url)
            the_page = str(driver1.page_source)
            time.sleep(5)
        except:
            return []

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


def view_html_structure(url, scrape_option, known_html=[], wrong_words=[]):
    # print('wrong', wrong_words)
    html = []
    if len(known_html) == 0:
        html = get_html(url, scrape_option)
    else:
        html = known_html
    if not html:
        return {}
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
    # for i in html_tree:
    #     print(len(i), i)

    path_dict = {}
    tmp = []
    for level in range(len(html_tree) - 1, -1, -1):
        update_tmp = []
        for i in range(len(html_tree[level])):
            if html_tree[level][i][0] not in update_tmp:
                update_tmp.append(html_tree[level][i][0])
            if i not in tmp:
                if raw_html[html_tree[level][i][2] + 1][0] == '<' or raw_html[html_tree[level][i][2] + 1] == ' ':
                    continue

                r = ''
                if check(raw_html[html_tree[level][i][2] + 1]):
                    r = 'Department'
                else:
                    r = 'None'
                # print(r, raw_html[html_tree[level][i][2] + 1])
                if r != 'None':
                    p = []
                    t = level
                    n = html_tree[t][i][0]
                    while t >= 1:
                        p.append(n)
                        t -= 1
                        n = html_tree[t][n][0]
                    if r not in path_dict.keys():
                        path_dict[r] = []
                    p = p[::-1]
                    p.append(i)
                    flag = True
                    if len(raw_html[html_tree[level][i][2] + 1]) < 3:
                        flag = False
                    if raw_html[html_tree[level][i][2] + 1].strip() in wrong_words:
                        flag = False
                    if raw_html[html_tree[level][i][2] + 1] in wrong_words:
                        flag = False
                    if flag:
                        path_dict[r].append(list(p).copy())

        tmp = update_tmp.copy()
    # print(path_dict)

    for i in path_dict.keys():
        for j in path_dict[i]:
            t = []
            n = 0
            for k in j:
                t.append(html_tree[n][k][1])
                n += 1

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
        if len(t) > 0 and t[0][1] > 0.2 * candidate_num:
            common_structure.append(t[0][0])
        else:
            break
        a += 1

    final_result = []

    def find_all_target_data(common_structure, correct_subtree_path={}):
        # print(common_structure)
        l = len(common_structure)
        path_dict_2 = {}
        for i in path_dict.keys():
            a = []
            for j in path_dict[i]:
                if j[:l] == common_structure:
                    a.append(j.copy())
            path_dict_2[i] = a.copy()
        # print(path_dict_2)

        dict_for_building_subtree = {}
        each_structure = {}
        for i in path_dict_2.keys():
            d = {}
            dict_for_building_subtree[i] = []
            each_structure[i] = []
            for j in path_dict_2[i]:
                t = ""
                n = 0
                for k in j:
                    t += html_tree[n][k][1]
                    n += 1
                if t not in d.keys():
                    d[t] = 0
                d[t] += 1
                # print(i, j, t, html_tree[n - 1][k], raw_html[html_tree[n - 1][k][2] + 1])
                dict_for_building_subtree[i].append([j.copy(), t])
            a = []
            for j in d.keys():
                a.append([j, d[j]])
            a = sorted(a, key=lambda x: x[1], reverse=True)
            try:
                # print(a[0][0], i)
                each_structure[i] = a[0][0]
            except:
                a31 = 0
                # print('No ' + i)
        # print(common_structure)

        subtree_roots = []
        for i in range(len(html_tree[len(common_structure)])):
            if html_tree[len(common_structure)][i][0] == common_structure[-1]:
                t = html_tree[len(common_structure)][i].copy()
                t.append(i)
                subtree_roots.append(t)
        # print(subtree_roots)

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
        # print(subtree_dict)

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
                    while tag in tag_class_names:
                        tag = tag[:-1] + '@' + '>'
                    tag_class_names.append(tag)

                    node[1] = tag

        translation = {}
        for i in subtree_dict.keys():
            for j in subtree_dict[i]:
                for k in j:
                    translation[k[-1]] = k[1]

        subtree_path = {}
        if len(correct_subtree_path.keys()) > 0:
            subtree_path = correct_subtree_path
        else:
            for i in path_dict_2.keys():
                subtree_path[i] = {}
                for j in path_dict_2[i]:
                    a = ''
                    for k in range(len(common_structure), len(j)):
                        a += str(j[k]) + '-'
                    try:
                        if translation[a] not in subtree_path[i].keys():
                            subtree_path[i][translation[a]] = 0
                        subtree_path[i][translation[a]] += 1
                    except:
                        continue

            # print(subtree_path)

        path_to_result = {}
        for i in subtree_dict.keys():
            path_to_result[i] = {}
            for j in subtree_dict[i]:
                for k in j:
                    path_to_result[i][k[1]] = [k[2], k[3]]

        # print(path_to_result)
        subtree_path['Department'] = max(subtree_path['Department'], key=subtree_path['Department'].get)
        # print(subtree_path)

        if len(correct_subtree_path) == 0:
            for i in subtree_path.keys():
                if subtree_path[i] == 'None' or ' ' in subtree_path[i][subtree_path[i].rfind('<'):]:
                    continue
                case_of_single_child = 0
                for j in path_to_result.keys():
                    if (subtree_path[i][:-1] + '@' + '>') not in path_to_result[j].keys():
                        case_of_single_child += 1
                if case_of_single_child == len(path_to_result):
                    continue
                parent = subtree_path[i][:subtree_path[i].rfind('<')]
                stem = subtree_path[i][len(parent):]
                stem = stem.replace('@', '')
                stem = parent + stem
                stem = stem[:-1]
                anchor_points = {'start': {}, 'end': {}}
                candidates = {}
                for j in path_to_result.keys():
                    for k in path_to_result[j].keys():
                        if len(k) > len(parent) and parent in k and k[len(parent):].rfind('<') == 0:
                            tmp = k[len(parent):]
                            if ' ' in tmp or ('@' not in tmp and k[:-1] + '@>' not in path_to_result[j].keys()):
                                if k not in candidates.keys():
                                    candidates[k] = 0
                                candidates[k] += 1
                for j in candidates.keys():
                    if candidates[j] >= 0.95 * len(path_to_result):
                        anchor_points[j] = {}
                # print(i, anchor_points)
                for j in path_dict_2[i]:
                    path_in_subtree = j[len(common_structure):]
                    subtree_dict_key = path_in_subtree[0]
                    string_path = ''
                    for k in path_in_subtree:
                        string_path += str(k) + '-'
                    parent_string_path = string_path[:string_path[:-1].rfind('-') + 1]
                    parent_name = -1
                    # print(subtree_dict_key)
                    # print(parent_string_path.count('-'))
                    try:
                        for k in subtree_dict[subtree_dict_key][parent_string_path.count('-') - 1]:
                            if k[-1] == parent_string_path:
                                parent_name = k[-2]
                        siblings = []
                        for k in subtree_dict[subtree_dict_key][string_path.count('-') - 1]:
                            if k[0] == parent_name:
                                siblings.append(k.copy())
                        target_index = -1
                    except:
                        continue
                    for k in range(len(siblings)):
                        if siblings[k][-1] == string_path:
                            if siblings[k][1][:len(stem)] != stem:
                                break
                            target_index = k
                    if target_index == -1:
                        continue
                    if target_index not in anchor_points['start'].keys():
                        anchor_points['start'][target_index] = 0
                    anchor_points['start'][target_index] += 1
                    if -1 * (len(siblings) - target_index - 1) not in anchor_points['end'].keys():
                        anchor_points['end'][-1 * (len(siblings) - target_index - 1)] = 0
                    anchor_points['end'][-1 * (len(siblings) - target_index - 1)] += 1
                    for k in anchor_points.keys():
                        if k != 'start' and k != 'end':
                            anchor_index = -1
                            for kk in range(len(siblings)):
                                if siblings[kk][1] == k:
                                    anchor_index = kk
                            if anchor_index == -1:
                                continue
                            anchor_index = target_index - anchor_index
                            if anchor_index not in anchor_points[k].keys():
                                anchor_points[k][anchor_index] = 0
                            anchor_points[k][anchor_index] += 1

                # print(anchor_points)
                best_anchor_point = []
                for j in anchor_points.keys():
                    best_anchor_point.append([j, max(anchor_points[j].values()) / sum(anchor_points[j].values())])
                best_anchor_point = sorted(best_anchor_point, key=lambda x: x[1], reverse=True)
                best_anchor_point = [best_anchor_point[0][0], best_anchor_point[0][1]]
                best_anchor_point[1] = max(anchor_points[best_anchor_point[0]], key=anchor_points[best_anchor_point[0]].get)
                if best_anchor_point[0] == 'start' or best_anchor_point[0] == 'end':
                    best_anchor_point.append(parent)
                # print(best_anchor_point)
                # print()
                subtree_path[i] = best_anchor_point.copy()

        result = []
        total_miss, total_num, total_match = 0, 1, 0
        for i in path_to_result.keys():
            d = {}
            missing = 0
            match = 0
            for j in subtree_path.keys():
                p = subtree_path[j]
                if isinstance(p, str):
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
                                a += raw_html[k] + ' '
                        a = a.replace('\n', ' ')
                        if ' ' in a:
                            a = a[:-1]
                        # print(j + ': ' + a)
                        d[j] = a
                        total_match += 1
                    else:
                        # print(j + ': missing')
                        d[j] = 'Missing'
                        missing += 1
                else:
                    try:
                        parent = ''
                        if p[0] == 'start' or p[0] == 'end':
                            parent = p[-1]
                        else:
                            parent = p[0][:p[0].rfind('<')]
                        siblings = []
                        for kk in subtree_dict[i][parent.count('<')]:
                            if kk[1][:len(parent)] == parent:
                                siblings.append(kk.copy())
                        position = -1
                        if p[0] == 'start':
                            position = p[1]
                        elif p[0] == 'end':
                            position = len(siblings) - 1 + p[1]
                        else:
                            for k in range(len(siblings)):
                                if siblings[k][1] == p[0]:
                                    position = k + p[1]
                        if 0 <= position < len(siblings):
                            a = ''
                            for k in range(siblings[position][2], siblings[position][3]):
                                if raw_html[k][0] != '<':
                                    a += raw_html[k] + ' '
                            a = a.replace('\n', ' ')
                            if ' ' in a:
                                a = a[:-1]
                            # print(j + ': ' + a)
                            d[j] = a
                            total_match += 1
                        else:
                            # print(j + ': missing')
                            d[j] = 'Missing'
                            missing += 1
                    except:
                        # print(j + ': missing')
                        d[j] = 'Missing'
                        missing += 1

            # print()
            if missing < 5:
                result.append(d.copy())
            total_miss += missing
            total_num += 1
        # try:
        #     a_num, a = handle_extreme_edge_case(subtree_dict, subtree_path, raw_html)
        #     print('???')
        #     if a_num > total_match:
        #         print(3113)
        #         for r in a:
        #             if 'Department' in r.keys() and r['Department'] != 'Missing':
        #                 final_result.append(r.copy())
        #         return subtree_path
        # except:
        #     a31 = 0
        #     # print('nothing happens')

        # print(result)
        if total_miss / total_num > 0.66:
            # print('Warning----------Total Miss:', total_miss, '  Num: ', total_num)
            # print()
            return {}

        review_match = 0
        for i in result:
            if i['Department'] and check(i['Department']):
                review_match += 1

        if review_match / (len(result) + 0.0001) < 0.5:
            return {}

        for r in result:
            if 'Department' in r.keys() and r['Department'] != 'Missing':
                final_result.append(r.copy())
        return subtree_path

    common_structures = find_possible_list(path_dict)
    # print(common_structures)
    true_path = {}
    for i in common_structures:
        # print(true_path)
        try:
            r = find_all_target_data(i, true_path)
            # print('r', r)
            if 'Department' in r.keys() and r['Department'] != 'None' and r['Department'] > 10:
                for j in r.keys():
                    true_path[j] = r[j]
        except:
            continue

    noise = []
    for i in ['Department']:
        m = {}
        for j in final_result:
            if i in j.keys() and j[i] != 'Missing':
                if j[i] not in m.keys():
                    m[j[i]] = 0
                m[j[i]] += 1
        if len(m) > 0 and max(m.values()) / (len(final_result)) > 0.93:
            noise.append(max(m, key=m.get))
    # print(wrong_words)
    # print(final_result)
    if len(noise) > 0:

        # avoid infinite loop
        for i in noise:
            if i in wrong_words:
                return final_result
        for i in wrong_words:
            noise.append(i)
        final_result = []
        return view_html_structure(url, scrape_option, html, noise)

    return final_result


universities = []
f = open('Data/universities/US_Universities.txt', 'r')
for i in f.readlines():
    universities.append(i[:-1])


def find(keywords):
    url = 'https://www.google.com/'
    option = webdriver.ChromeOptions()
    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver', chrome_options=option)
    driver.get(url)
    input_tab = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    time.sleep(1)
    input_tab.send_keys(keywords, Keys.ENTER)
    elems = driver.find_elements_by_xpath("//a[@href]")
    possibleURLs = []
    words = ['google', 'wiki', 'news', 'instagram', 'twitter', 'linkedin', 'criminal', 'student', 'course', 'facebook', 'usnews']
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
    return possibleURLs


# a = view_html_structure('https://oru.edu/academics/explore-programs.php', 'urllib')
# print(len(a))
# for i in a:
#     print(i)


def get_departments_of_university(university):
    urls = find(university + ' majors')
    for url in urls:
        print(url)
        try:
            r = view_html_structure(url, 'urllib')
        except:
            continue
        res = []
        count = 0
        for j in r:
            if 'Department' in j.keys():
                if check(j['Department']):
                    count += 1
                res.append(j['Department'])
        if count / (len(res) + 0.0001) > 0.6 and len(res) > 10:
            # for j in res:
            #     print(j)
            return res


# for i in range(61, 100):
#     print(i, universities[i])
#     try:
#         r = get_departments_of_university(universities[i])
#     except:
#         continue
#     print(r)
#     if r:
#         f = open(os.getcwd() + '/Data/departments/' + universities[i] + '.txt', 'w')
#         for j in r:
#             f.write(j + '\n')
#     f.close()

r = get_departments_of_university('Carroll College')
print(r)