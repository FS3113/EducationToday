# import base64
# from PIL import Image
# import io
# import numpy as np
# import matplotlib.pyplot as plt
#
# # with open("Training_Images/Positive/0.png", "rb") as image:
# #     b64string = base64.b64encode(image.read())
# # print(b64string)
# #
# # f = io.BytesIO(base64.b64decode(b64string))
# # pilimage = Image.open(f)
# # Image._show(pilimage)
#
# def render(image_name):
#     with open(image_name, "rb") as image:
#         b64string = base64.b64encode(image.read())
#     print('@user_image@' + str(b64string))
#
# contents = ["“THAT SHIT WAS GAAAAAASSS” -jesus, circa year 4","Intellectually stimulated, brown melinated, free in spirit ✨I was born to see out my artistic visions 💕 #UIUC 💙 I’m just here to paint the bigger picture 🎨","Jermiah 29:11 // ♑️","Founder DGPW. 14 yr cancer survivor (I've got too much havoc yet to wreak). Love all my boys. Love my Vespa. 5 continents down, 2 to go! RIP Archie🐕 7/25/17🌈","Bejucos 🇲🇽🤪","Bejucos 🇲🇽🤪","just smack your face against my hand I'm too lazy to slap you","","I tweet about work but also not about work. Researcher at @RiceKinderInst. Opinions are mine, not theirs.","I tweet about work but also not about work. Researcher at @RiceKinderInst. Opinions are mine, not theirs.","","Mediocre Muay Thai Fighter. Poor BJJ Fighter. Opinionated but I love a good debate. Co-host of The Split Decision Podcast (@split_podcast) 🎙","UW-Madison's official Forest and Wildlife Ecology page\n\n#UWMadison\n#Conservation","viol(in/a???), crosswords, and BB-8 | punk ass book jockey | UIUC classics/library science | she/her","grown || uiuc || educator || she/her || BLM || 🇵🇸"]
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# print(3113)
# x1 = np.linspace(0.0, 5.0)
# x2 = np.linspace(0.0, 2.0)
#
# y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
# y2 = np.cos(2 * np.pi * x2)
#
# fig, (ax1, ax2) = plt.subplots(2, 1)
# fig.suptitle('A tale of 2 subplots')
#
# ax1.plot(x1, y1, 'o-')
# ax1.set_ylabel('Damped oscillation')
#
# ax2.plot(x2, y2, '.-')
# ax2.set_xlabel('time (s)')
# ax2.set_ylabel('Undamped')
#
# plt.savefig('a.png')
#
# render('a.png')

i = 3
s = set()
while True:
    a = (i ** 2 + i - 1) % 64
    b = (i ** 4 + i - 2) % 64
    c = (i ** 6 + i - 3) % 64
    if a in s and b in s and c in s:
        print(i)
        break
    s.add(a)
    s.add(b)
    s.add(c)
    i += 3


class valuable:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight


class box:
    def __init__(self):
        self.contents = {}
        self.weights = [[0, 0]]

    def add(self, a, t):
        self.contents[a.id] = a
        self.weights.append([self.weights[-1][0] + a.weight, t])

    def remove(self, a, t):
        if a in self.contents.keys():
            self.weights.append([self.weights[-1][0] - self.contents[a].weight, t])
            del self.contents[a]


b = box()
v1 = valuable(1, 10)
v2 = valuable(2, 20)
b.add(v1, 60)
b.add(v2, 70)
b.remove(2, 80)
print(b.weights)
