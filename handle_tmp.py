import random
import string


# def randomString(stringLength):
#     """Generate a random string of fixed length """
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(stringLength))
#
# for i in range(100):
#     print(randomString(6) + '.' + randomString(6) + '@' + randomString(6) + '.edu')



# f = open('tmp.txt', 'r')
# f1 = open('faculty_list.txt', 'a')
# for i in f.readlines():
#     f1.write(i)



def f(n):
    r = ''
    for i in range(n):
        r += str(random.randint(0, 9))
    return r
for i in range(100):
    print('| (' + f(3) + ') ' + f(3) + '-' + f(4))