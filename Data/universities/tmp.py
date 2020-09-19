f = open('US_Universities.txt', 'a')

f1 = open('tmp.txt', 'r')
l = []
for i in f1.readlines():
    l.append(i[:-1])

key = 'Regional Colleges West'
for i in range(len(l)):
    if len(l[i]) >= len(key) and l[i][:len(key)] == key and l[i - 1] == 'in':
        f.write(l[i - 5] + '\n')