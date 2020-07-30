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
import pandas as pd
import nltk

warnings.filterwarnings(action='ignore')
english_dictionary = enchant.Dict("en_US")


def handle_input():
    result = []
    data = []
    label = []

    f = pd.read_csv('Courses/combined_data_cleaned_duplicates.csv')
    for i in f.iloc[:, 2].values:
        result.append(i[:-1])
        data.append(i[:-1])
        label.append('Course')

    f = pd.read_csv('Courses/combined_data_cleaned_duplicates.csv')
    for i in f.iloc[:, -1].values:
        result.append(i[:-1])
        data.append(i[:-1])
        label.append('Description')

    f = open('negative_courses.txt', 'r')
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

    # f = pd.read_csv('Courses/data_harvard_negative.csv')
    # # negative_dict = {}
    # for i in f.iloc[:, 1].values:
    #     if len(i) > 1:
    #         a = i.replace('\n', '')
    #         result.append(a)
    #         data.append(a)
    #         label.append('None')
    #         a = a.split()
    #         for j in a:
    #             if j not in negative_dict.keys():
    #                 negative_dict[j] = 0
    #             negative_dict[j] += 1
    #
    # f = pd.read_csv('Courses/data_berkeley_negative.csv')
    # for i in f.iloc[:, 1].values:
    #     if len(i) > 1:
    #         a = i.replace('\n', '')
    #         result.append(a)
    #         data.append(a)
    #         label.append('None')
    #         a = a.split()
    #         for j in a:
    #             if j not in negative_dict.keys():
    #                 negative_dict[j] = 0
    #             negative_dict[j] += 1
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
        if j[1] not in string.punctuation and english_dictionary.check(j[1]):
            a += 1
            keyword_list.append(j[1])
        if a == 20:
            break
print(keywords_dict)


entries = list(keywords_dict.keys())
def vectorize(d):
    space = 0
    tmp = d
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
    keywords = [0] * len(keywords_dict.keys())
    keywords_match = [0] * len(entries)
    negative = 0
    for j in data:
        if j.isnumeric():
            number += 1
        elif j in string.punctuation:
            punctuation += 1
        elif english_dictionary.check(j):
            english += 1
        flag_n, flag_w = False, False
        for k in j:
            if k.isnumeric():
                flag_n = True
            if k in string.ascii_lowercase or k in string.ascii_uppercase:
                flag_w = True
        if flag_n and flag_w:
            number_words += 1

        for k in range(len(entries)):
            if j in keywords_dict[entries[k]].keys() and j not in string.punctuation:
                keywords_match[k] += keywords_dict[entries[k]][j]

        a = 0
        for k in keywords_dict.keys():
            if j in keywords_dict[k].keys():
                keywords[a] += keywords_dict[k][j]
            a += 1

        if j in negative_dict.keys() and j not in string.punctuation:
            negative += negative_dict[j]
    v = [len(data), english, number, punctuation, space, number_words, negative]
    # v.extend(keywords_match)
    # v.extend(keywords)
    # for i in keyword_list:
    #     if i in data:
    #         v.append(1)
    #     else:
    #         v.append(0)
    # print(d, v)
    return v


for i in range(len(data)):
    data[i] = vectorize(data[i])


model = RandomForestClassifier(n_estimators=10, max_depth=10)
model.fit(data, label)
pickle.dump(model, open('random_forest_model_course.sav', 'wb'))

# f = pd.read_csv('Courses/combined_data_cleaned_duplicates.csv')
# for i in f.iloc[:, 2].values:
#     # print(i, vectorize(i), model.predict([vectorize(i)]))
#     print(i, nltk.pos_tag(i.split()), model.predict([vectorize(i)]))
# print()
# print()
#
# f = open('raw_html.txt', 'r')
# for i in f.readlines():
#     i = i.replace('\n', '')
#     if len(i) <= 1 or i[0] == '<':
#         continue
#     # print(i, vectorize(i), model.predict([vectorize(i)]))
#     print(i, nltk.pos_tag(i.split()), model.predict([vectorize(i)]))
#
# print(nltk.pos_tag('Jeremiah Sullivan'.split()))
# print(nltk.pos_tag('Computer Science'.split()))