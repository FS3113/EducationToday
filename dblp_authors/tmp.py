import time
import pickle

start = time.perf_counter()
f = open('dblp_authors.txt', 'r')
first = {}
last = {}
for i in f.readlines():
    if ',' not in i:
        continue
    idx = i.index(',')

    t = i[:idx].lower()
    if t not in first.keys():
        first[t] = 0
    first[t] += 1

    a = i[idx + 1:]
    a = a.replace('\n', '')
    a = a.replace(',', '')
    a = a.split()
    for j in a:
        t = j.lower()
        if t not in last.keys():
            last[t] = 0
        last[t] += 1
print(len(first), len(last))

f = open('first_name.pkl', 'wb')
f1 = open('last_name.pkl', 'wb')
pickle.dump(first, f)
pickle.dump(last, f1)

end = time.perf_counter()
print(end - start)

# a = time.perf_counter()
# f = open('last_name.pkl', 'rb')
# s = pickle.load(f)
# print(len(s))
# print(s['youtube'])
# # for i in s:
# #     print(i)
# print(time.perf_counter() - a)
