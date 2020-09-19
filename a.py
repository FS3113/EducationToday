import os
import re

d = {}
s = set()
ss = set()

universities = []
f = open('Data/universities/US_Universities.txt', 'r')
for i in f.readlines():
    universities.append(i[:-1])

for filename in os.listdir(os.getcwd() + '/departmentData'):
    if not filename[:-4] in universities[:20]:
        continue
    f = open(os.getcwd() + '/departmentData/' + filename, 'r')
    if filename == '.DS_Store':
        continue
    for i in f.readlines():
        i = i.replace('\\n', '').replace('\\t', '').replace('&amp;', '&').replace('&nbsp;', ' ')
        if '(' in i and ')' in i:
            i = i[:i.index('(')] + i[i.index(')') + 1:]
        if '(' in i:
            ss.add(filename)
        a = re.split('\W+', i)
        for j in a:
            j = j.replace(',', '')
            j = j.lower()
            s.add(j)
            if j not in d.keys():
                d[j] = []
            d[j].append(filename)

f = open('Get_Departments/majors.txt', 'w')
for i in s:
    f.write(i + '\n')

for i in d:
    print(i, len(d[i]), d[i])