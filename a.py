from random import randint

f = open('tmp.txt', 'r')
r = 0
for i in f.readlines():
    if int(i) < 0:
        r += 1
print(r)