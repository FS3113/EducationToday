from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
from sklearn.ensemble import RandomForestClassifier
import pickle

im = Image.open('Faculty_Image/4.png')
pix = im.load()
print(im.size)
print(pix[0, 0])
a = 0
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if pix[i, j][0] >= 240 and pix[i, j][1] >= 240 and pix[i, j][1] >= 240:
            a += 1
print(a / (im.size[0] * im.size[1]))



def vectorize_image(path):
    im = Image.open(path)
    pix = im.load()
    a, a1, a2, a3 = 0, [], [], []
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pix[i, j][0] >= 240 and pix[i, j][1] >= 240 and pix[i, j][1] >= 240:
                a += 1
            a1.append(pix[i, j][0])
            a2.append(pix[i, j][1])
            a3.append(pix[i, j][2])
    a /= (im.size[0] * im.size[1])
    a1 = np.array(a1)
    a2 = np.array(a2)
    a3 = np.array(a3)
    v = [im.size[0], im.size[1], a, np.mean(a1), np.std(a1), np.mean(a2), np.std(a2), np.mean(a3), np.std(a3)]
    return v


onlyfiles = [f for f in listdir('Training_Images/Positive') if isfile(join('Training_Images/Positive', f))]
data, label = [], []
for i in onlyfiles:
    if i[-4:] == '.png':
        data.append(vectorize_image('Training_Images/Positive/' + i).copy())
        label.append(1)

onlyfiles = [f for f in listdir('Training_Images/Negative') if isfile(join('Training_Images/Negative', f))]
for i in onlyfiles:
    if i[-4:] == '.png':
        data.append(vectorize_image('Training_Images/Negative/' + i).copy())
        label.append(0)
print(data)

model = RandomForestClassifier(n_estimators=5, max_depth=5)
model.fit(data, label)
pickle.dump(model, open('image_random_forest_model.sav', 'wb'))
print('finish training')

for i in [f for f in listdir('Training_Images/Positive') if isfile(join('Training_Images/Positive', f))]:
    if i[-4:] == '.png':
        v = vectorize_image('Training_Images/Positive/' + i)
        a = model.predict([v])
        print(v, a)
print()
for i in [f for f in listdir('Training_Images/Negative') if isfile(join('Training_Images/Negative', f))]:
    if i[-4:] == '.png':
        v = vectorize_image('Training_Images/Negative/' + i)
        a = model.predict([v])
        print(v, a)
