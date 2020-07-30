from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import gensim
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.ensemble import RandomForestClassifier
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import enchant
import numpy as np
import string
import pickle
import nltk

warnings.filterwarnings(action='ignore')
english_dictionary = enchant.Dict("en_US")


def handle_input():
    result = []
    data = []
    label = []
    f = open('faculty_list.txt', 'r')
    for i in f.readlines():
        if len(i) > 1:
            a = i.replace('\n', '')
            a = a.replace(i[: i.index(':') + 2], '')
            result.append(a)
            data.append(a)
            label.append(i[: i.index(':')])
    f = open('negative.txt', 'r')
    negative_dict = {}
    for i in f.readlines():
        if len(i) > 1:
            a = i.replace('\n', '')
            result.append(a)
            data.append(a)
            label.append('None')
            a = a.split()
            for j in a:
                if j not in negative_dict:
                    negative_dict[j] = 0
                negative_dict[j] += 1
    return result, data, label, negative_dict.copy()


texts, data, label, negative_dict = handle_input()

splited_data = []
for i in range(len(data)):
    tmp = data[i]
    j = 0
    while j < len(tmp):
        if tmp[j] in string.punctuation:
            tmp = tmp[:j] + ' ' + tmp[j] + ' ' + tmp[j + 1:]
            j += 2
        j += 1
    splited_data.append(tmp.split())

# n
keywords_dict = {}
for i in range(len(splited_data)):
    if label[i] not in keywords_dict.keys():
        keywords_dict[label[i]] = {}
    for j in range(len(splited_data[i])):
        if splited_data[i][j] not in keywords_dict[label[i]]:
            keywords_dict[label[i]][splited_data[i][j]] = 0
        keywords_dict[label[i]][splited_data[i][j]] += 1

words_dict = {}
for i in keywords_dict.keys():
    l = [[keywords_dict[i][j], j] for j in keywords_dict[i].keys()]
    l = sorted(l, key=lambda x: x[0], reverse=True)
    words_dict[i] = l.copy()
keyword_list = []
for i in words_dict.keys():
    a = 0
    for j in words_dict[i]:
        if j[1] not in string.punctuation and english_dictionary.check(j[1]) and len(j[1]) > 1:
            a += 1
            keyword_list.append(j[1])
        if a == 20:
            break
print(keywords_dict)

check_keywords = []
for i in keywords_dict.keys():
    d = keywords_dict[i]
    l = []
    for j in d.keys():
        a = nltk.pos_tag([j])
        if len(j) > 1 and ('JJ' in a[0][1] or 'VB' in a[0][1] or 'NN' in a[0][1] or 'RB' in a[0][1]):
            l.append([j, d[j]])
    l = sorted(l, key=lambda x: x[1], reverse=True)
    for j in range(40):
        check_keywords.append(l[j][0])
        print(j, l[j][0])

entries = list(keywords_dict.keys())
def vectorize(d):
    space = 0
    tmp = d
    pos_tags = nltk.pos_tag(d.split())
    # print(pos_tags)

    # jj, vb, nn, rb, in
    pos_vector = [0, 0, 0, 0, 0]
    for i in pos_tags:
        if english_dictionary.check(i[0]) and len(i[0]) > 1:
            if 'JJ' in i[1]:
                pos_vector[0] += 1
            elif 'VB' in i[1]:
                pos_vector[1] += 1
            elif 'NN' in i[1]:
                pos_vector[2] += 1
            elif 'RB' in i[1]:
                pos_vector[3] += 1
            elif 'IN' in i[1]:
                pos_vector[4] += 1

    while '  ' in tmp:
        tmp = tmp.replace('  ', ' ')
    for i in tmp:
        if i == ' ':
            space += 1
    j = 0
    while j < len(tmp):
        if tmp[j] in string.punctuation:
            tmp = tmp[:j] + ' ' + tmp[j] + ' ' + tmp[j + 1:]
            j += 2
        j += 1
    data = tmp.split()
    english, number, punctuation, number_words = 0, 0, 0, 0
    negative = 0
    for j in data:
        if j.isnumeric():
            number += 1
        elif j in string.punctuation:
            punctuation += 1
        elif english_dictionary.check(j) and len(j) > 1:
            english += 1
        flag_n, flag_w = False, False
        for k in j:
            if k.isnumeric():
                flag_n = True
            if k in string.ascii_lowercase or k in string.ascii_uppercase:
                flag_w = True
        if flag_n and flag_w:
            number_words += 1

        if j in negative_dict.keys() and j not in string.punctuation:
            negative += negative_dict[j]
    v = [len(data), english, number, punctuation, space, number_words, negative]
    # v.extend(pos_vector)
    for i in check_keywords:
        if i in d:
            v.append(1)
        else:
            v.append(0)
    return v


for i in range(len(data)):
    data[i] = vectorize(data[i])


model = RandomForestClassifier(n_estimators=10, max_depth=10)
model.fit(data, label)
pickle.dump(model, open('random_forest_model.sav', 'wb'))

print(model.predict([vectorize('A')]))
print(vectorize('B'))
print(model.predict([vectorize('B')]))
print(english_dictionary.check('B'))
print(model.predict([vectorize('computer science')]))
print(nltk.pos_tag(['test']))
print(vectorize('9'))

print(nltk.pos_tag(['juefei', 'chen']))
print(english_dictionary.check('Felix'))
