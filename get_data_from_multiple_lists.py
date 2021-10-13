import time
import json
import urllib.request
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECg
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pickle
from collections import defaultdict
from random_forest import vectorize
import string
from find_possible_list import find_possible_list
from find_possible_list import find_info_in_grandchildren
import os
import pathlib


abs_path = str(pathlib.Path(__file__).parent.absolute()) + '/'
random_forest_model = pickle.load(open(abs_path + 'random_forest_model.sav', 'rb'))

f1 = open(abs_path + 'dblp_authors/first_name.pkl', 'rb')
dblp_first_name = pickle.load(f1)
f2 = open(abs_path + 'dblp_authors/last_name.pkl', 'rb')
dblp_last_name = pickle.load(f2)
invalid_dblp_names = {'only', 'every', 'faculty', 'research', 'international', 'study', 'group', 'department', 'policy', 'internet'
                      'the', 'of', 'people', 'peoples', 'found', 'lab', 'team', 'offer', 'doctor', 'task', 'school', 'new', 'old'
                      'single', 'add', 'to', 'event', 'all', 'day', 'university', 'data', 'learn', 'internet', 'architecture'
                      , 'urban', 'court', 'train', 'manage', 'child', 'family', 'this', 'site', 'search', 'main', 'close',
                      'at', 'are', 'you', 'here', 'skip', 'content', 'english', 'and', 'latin', 'world', 'fellows', 'summer',
                      'haven', 'about', 'jobs', 'meet', 'us', 'or', 'call', 'start', 'dates', 'from', 'crowd', 'state',
                      'university', 'general', 'finance', 'as', 'few', 'far', 'supply', 'chain', 'planner', 'buyer',
                      'market', 'works', 'major', 'minor', 'minors', 'plus', 'max', 'by', 'in', 'we', 'have', 'name', 'personal',
                      'link', 'for', 'general', 'information', 'room', 'street', 'wall', 'reading', 'list', 'with',
                      'divine', 'comedy', 'times', 'more', 'please', 'visit', 'south', 'north', 'west', 'east',
                      'africa', 'machine', 'learning', 'part', 'states', 'united', 'year', 'back', '3rd', 'durability',
                      'life', 'students', 'must', 'student', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                      'saturday', 'sunday', 'seminar', 'what', 'is', 'are', 'an', 'be', 'honors', 'gold', 'real',
                      'analysis', 'algebra', 'software', 'design', 'designer', 'studio', 'media', 'scales', 'about',
                      'college', 'column', 'footer', 'first', 'second', 'third', 'fourth', 'on', 'market', 'contact',
                      'home', 'colleges', 'schools', 'database', 'center', 'server', 'alumni', 'awards', 'interests',
                      'q:','requirements', 'hall', 'master', 'plan', 'knowledge', 'base', 'live', 'work', 'bridge', 'vote', 'how',
                      'to', 'form', 'self', 'report', 'reporting', 'health', 'community', 'international', 'leadership', 'fees',
                      'bookstore', 'board', 'core', 'values', 'policies', 'policy', 'experience', 'title', 'model', 'unitied',
                      'club', 'music', 'camera', 'change', 'overview', 'mission', 'vision', 'why', 'glance', 'brave', 'start', 
                      'grant', 'admission', 'about', 'faqs', 'building', 'summer', 'home', 'academics', 'position', 'news', 'events', 
                      'advising', 'undergraduate', 'catalog', 'map', 'campus', 'support', 'ask', 'question', 'give', 'apply', 'visit',
                      'small', 'farm', 'venture', 'area', 'about', 'my', 'bs', 'ba', 'ma', 'staff', 'stay', 'centre', 'message',
                      'dean', 'messager', 'food', 'dinning', 'tools', 'apps', 'awards', 'more', 'find', 'out', 'majors'}
max_name_length = 0



# given an url, get whole html in a good format (a list)
def get_html(url, scrape_option):
    # flag = False
    faculty_image = []
    the_page = ''
    if scrape_option == 'urllib':
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
            the_page = (str(the_page))
        except:
            # print("cannot crawl")
            # flag = True
            return []
    else:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument(' — incognito')
            option.add_argument('--no - sandbox')
            option.add_argument('--window - size = 1420, 1080')
            option.add_argument('--headless')
            option.add_argument('--disable - gpu')
            driver1 = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver',
                                       chrome_options=option)
            driver1.get(url)
            time.sleep(1)
            the_page = str(driver1.page_source)
            # print(the_page)
            time.sleep(2)
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
    global max_name_length
    html = []
    if len(known_html) == 0:
        html = get_html(url, scrape_option)
    else:
        html = known_html
    if not html:
        return {}
    f = open(abs_path + 'html_structure.txt', 'w')
    f1 = open(abs_path + 'whole_html.txt', 'w')
    f2 = open(abs_path + 'raw_html.txt', 'w')
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

    # path_dict: keys are fields we are looking for such as names and positions, values are lists of correspond tag path
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

                check_name = raw_html[html_tree[level][i][2] + 1]
                check_name = check_name.replace(',', ' ')
                check_name = check_name.split()
                name_type = False
                if 1 < len(check_name) < 6:
                    name_c = 0
                    for k in check_name:
                        k = k.lower()
                        if (k in dblp_first_name.keys() or k in dblp_last_name.keys()) and k not in invalid_dblp_names:
                            name_c += 1
                    if len(check_name) <= 2:
                        if name_c == len(check_name):
                            name_type = True
                    elif 2 < len(check_name) <= 4:
                        if len(check_name) - name_c <= 1:
                            name_type = True
                    elif len(check_name) > 4:
                        if len(check_name) - name_c <= 2:
                            name_type = True
                r = ''
                if name_type:
                    max_name_length = max(max_name_length, len(check_name))
                    r = 'Name'
                elif raw_html[html_tree[level][i][2] + 1] in wrong_words:
                    r = 'None'
                else:
                    r = random_forest_model.predict([vectorize(raw_html[html_tree[level][i][2] + 1])])[0]
                    if r == 'Name':
                        r = 'None'
                # if r != 'None':
                #     print(r, '---', raw_html[html_tree[level][i][2] + 1])
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
                    # if r != 'Name':
                    #     flag = False
                    if r == 'Research Interest':
                        if 'Research' in raw_html[html_tree[level][i][2] + 1]:
                            aa = raw_html[html_tree[level][i][2] + 1].split(' ')
                            if len(aa) <= 3:
                                flag = False
                    invalid_names = ['admission', 'about', 'faqs', 'building', 'summer', 'home', 'academics', 'position', 'news', 'events', 'advising', 
                                    'undergraduate', 'catalog', 'map', 'campus', 'support', 'ask', 'question', 'give', 'apply', 'visit']
                    if r == 'Name':
                        for j in invalid_names:
                            if j in raw_html[html_tree[level][i][2] + 1].lower():
                                flag = False
                                break
                    if r == 'Name' or r == 'Position' or r == 'Research Interest':
                        for j in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Email', 'Phone', 'Homepage', '@', 'E-mail', 'Full Profile', '.edu']:
                            if j in raw_html[html_tree[level][i][2] + 1]:
                                flag = False
                                break
                    if len(raw_html[html_tree[level][i][2] + 1]) < 3:
                        flag = False
                    if raw_html[html_tree[level][i][2] + 1].strip() in wrong_words:
                        flag = False
                    if raw_html[html_tree[level][i][2] + 1] in wrong_words:
                        flag = False
                    if flag:
                        path_dict[r].append(list(p).copy())

        tmp = update_tmp.copy()
    # for i in path_dict:
    #     print(i)
    #     for j in path_dict[i]:
    #         print(j)
    #     print()

    # for i in path_dict.keys():
    #     for j in path_dict[i]:
    #         t = []
    #         n = 0
    #         for k in j:
    #             t.append(html_tree[n][k][1])
    #             n += 1
            # print(i, j, raw_html[html_tree[n - 1][k][2] + 1], t, html_tree[n - 1][k])
            # print(i, raw_html[html_tree[n - 1][k][2] + 1])

    # find the cluster in HTML that is most likely to contain a list faculty info
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
        # print(t)
        t = sorted(t, key=lambda x: x[1], reverse=True)
        if t and t[0][1] > 0.2 * candidate_num:
            common_structure.append(t[0][0])
        else:
            break
        a += 1
    # print(common_structure)

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

        # each subtree is expected to contain information of a faculty member
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
                continue
                # print('No ' + i)
        # print(common_structure)

        subtree_roots = []
        for i in range(len(html_tree[len(common_structure)])):
            if html_tree[len(common_structure)][i][0] == common_structure[-1]:
                t = html_tree[len(common_structure)][i].copy()
                t.append(i)
                subtree_roots.append(t)
        # print(subtree_roots)

        # return list of subtrees of a root node
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
                    if 'class="' in a:
                        a = a[a.index('class="') + 7:]
                        a = a[:a.index('"')]
                        if ' ' in a and any(char.isdigit() for char in a[a.index(' '):]):
                            a = a[:a.index(' ')]
                        p = 0
                        while p < len(a):
                            if a[p] in "1234567890":
                                a = a[:p] + a[p + 1:]
                            else:
                                p += 1
                        # tag = tag[: -1] + ' ' + a + '>'
                        tag = tag[:-1] + ' ' + a[:a.find(' ')] + '>'
                    while tag in tag_class_names:
                        tag = tag[:-1] + '@' + '>'
                    tag_class_names.append(tag)

                    node[1] = tag

        translation = {}
        for i in subtree_dict.keys():
            for j in subtree_dict[i]:
                for k in j:
                    translation[k[-1]] = k[1]

        # find tag path leading to each field of interest
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

            for x in range(3):
                for i in subtree_path.keys():
                    for j in subtree_path.keys():
                        if i != j:
                            try:
                                a, b = max(subtree_path[i], key=subtree_path[i].get), max(subtree_path[j],
                                                                                          key=subtree_path[j].get)
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
            # print(subtree_path)

            subtree_path1 = {}
            for i in subtree_path.keys():
                if len(subtree_path[i].keys()) == 0 or subtree_path[i][max(subtree_path[i], key=subtree_path[i].get)] == 0:
                    subtree_path1[i] = 'None'
                else:
                    subtree_path1[i] = max(subtree_path[i], key=subtree_path[i].get)

            subtree_path2 = {}
            for i in subtree_path.keys():
                if subtree_path1[i] == 'None':
                    subtree_path2[i] = 'None'
                else:
                    # print(i)
                    t1 = defaultdict(int)
                    for j in subtree_path[i].keys():
                        t1[j[:j.rfind('<')]] += subtree_path[i][j]
                    a1 = max(t1, key=t1.get)
                    flag1 = True
                    s = set([])
                    for j in subtree_path1.keys():
                        if j != i:
                            s.add(subtree_path1[j])
                    t_max = 0
                    t_sum = 0
                    for j in subtree_path[i].keys():
                        if j[:j.rfind('<')] == a1:
                            if j in s:
                                flag1 = False
                            else:
                                t_max = max(t_max, subtree_path[i][j])
                                t_sum += subtree_path[i][j]
                    if flag1 and t_sum / t_max > 1.85:
                        subtree_path2[i] = a1
                    else:
                        subtree_path2[i] = subtree_path1[i]

            for i in subtree_path.keys():
                subtree_path[i] = subtree_path2[i]

        path_to_result = {}
        for i in subtree_dict.keys():
            path_to_result[i] = {}
            for j in subtree_dict[i]:
                for k in j:
                    path_to_result[i][k[1]] = [k[2], k[3]]

        # apply "anchor point" technique
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

        # print(subtree_path)

        # analyzing result
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
            if missing < 4:
                result.append(d.copy())
            total_miss += missing
            total_num += 5
        # print(subtree_path)
        # print('--------------------------------------------------------------------')

        try:
            # handle the case when each cell of faculty info is not the direct decendent of the root
            a_num, a = find_info_in_grandchildren(subtree_dict, subtree_path, raw_html)
            # print(a_num, a, total_match)
            if a_num > total_match:
                for r in a:
                    if 'Name' in r.keys() and r['Name'] != 'Missing':
                        tmp_name = r['Name']
                        tmp_name = tmp_name.replace(',', ' ')
                        tmp_name = tmp_name.split()
                        if len(tmp_name) <= max_name_length:
                            final_result.append(r.copy())
                return subtree_path
        except:
            a31 = 0
        if total_miss / total_num > 0.8:
            # print('Warning----------Total Miss:', total_miss, '  Num: ', total_num)
            # print()
            return {}

        for r in result:
            if 'Name' in r.keys() and r['Name'] != 'Missing':
                tmp_name = r['Name']
                tmp_name = tmp_name.replace(',', ' ')
                tmp_name = tmp_name.split()
                if len(tmp_name) <= max_name_length:
                    final_result.append(r.copy())
        return subtree_path

    common_structures = find_possible_list(path_dict)
    true_path = {}
    for i in common_structures:
        # print(true_path)
        try:
            r = find_all_target_data(i, true_path)
            # print('r', r)
            if 'Name' in r.keys() and r['Name'] != 'None':
                for j in r.keys():
                    true_path[j] = r[j]
        except:
            continue

    noise = []
    for i in ['Name', 'Position', 'Research Interest', 'Email', 'Phone number']:
        m = {}
        t = 0.01
        for j in final_result:
            if i in j.keys() and j[i] != 'Missing':
                if j[i] not in m.keys():
                    m[j[i]] = 0
                m[j[i]] += 1
                t += 1
        if len(m) > 0 and max(m.values()) / t > 0.93:
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


