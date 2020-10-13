from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import numpy as np
import string
import pickle
from sklearn.ensemble import RandomForestClassifier
# import enchant
import nltk
nltk.download('words')
from nltk.corpus import words

warnings.filterwarnings(action='ignore')
# english_dictionary = enchant.Dict("en_US")
ed = set(words.words())


# check if a string is an English word
def check_english(aa):
    a = aa.lower()
    if a in ed or a[0].upper() + a[1:] in ed:
        return True
    if a[-1] == 's' and a[:-1] in ed:
        return True
    return False


# read training data
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

    f = open('phone_numbers.txt', 'r')
    for i in f.readlines():
        result.append(i)
        data.append(i)
        label.append('Phone number')

    f = open('email.txt', 'r')
    for i in f.readlines():
        result.append(i)
        data.append(i)
        label.append('Email')

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
        if j[1] not in string.punctuation and check_english(j[1]):
            a += 1
            keyword_list.append(j[1])
        if a == 20:
            break
# print(keyword_list)

entries = list(keywords_dict.keys())
def vectorize(d):
    # split by space and punctuation
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

    # feature: number of English works, number of numerical numbers, number of punctuations,
    # number of strings that is a combination of numerical number and characters
    english, number, punctuation, number_words = 0, 0, 0, 0

    # scores of words appear in each field
    keywords = [0] * len(keywords_dict.keys())

    # not used in this version
    keywords_match = [0] * len(entries)

    # total score of words appear in the negative examples
    negative = 0
    for j in data:
        if j.isnumeric():
            number += 1
        elif j in string.punctuation:
            punctuation += 1
        elif check_english(j):
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
    v.extend(keywords)
    # for i in keyword_list:
    #     if i in data:
    #         v.append(1)
    #     else:
    #         v.append(0)
    return v


for i in range(len(data)):
    data[i] = vectorize(data[i])

model = RandomForestClassifier(n_estimators=10, max_depth=10)
model.fit(data, label)
pickle.dump(model, open('random_forest_model.sav', 'wb'))

# a = "Associate Professor"
# v = vectorize(a)
# r = model.predict([v])
# print(r)
