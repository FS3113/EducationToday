import pickle
import pathlib
import time

abs_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

f = open(abs_path + 'english_words.txt', 'r')
english_words = f.read().split('\n')

f1 = open(abs_path + 'first_name.pkl', 'rb')
dblp_first_name = pickle.load(f1)

f2 = open(abs_path + 'last_name.pkl', 'rb')
dblp_last_name = pickle.load(f2)

# a = set(dblp_first_name.keys()).union(set(dblp_last_name.keys()))
# b = set(english_words)
# print(len(a), len(b))
# x = a.intersection(b)
# print(len(x))

def check_name(s):
    s = s.lower()
    s = s.replace(',', ' ')
    s = s.split()

    valid_num = 0
    for i in s:
        if (i in dblp_first_name or i in dblp_last_name) and i not in english_words:
            valid_num += 1
    
    if len(s) <= 2:
        return valid_num == len(s)
    if len(s) <= 4:
        return len(s) - valid_num <= 1
    return len(s) - valid_num <= 2
