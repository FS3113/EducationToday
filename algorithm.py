import time
from selenium import webdriver
import json
import urllib.request
from urllib.request import urlopen
from get_data_from_multiple_lists import view_html_structure
from datetime import datetime
import sys
import re
import urllib.parse
import pickle

forbidden = ['google', 'wiki', 'news', 'instagram', 'twitter', 'linkedin', 'criminal', 'course', 'facebook']


def find(university, department):
    possibleURLs = []
    query = university + ' ' + department
    url = 'https://www.google.com/search?q=' + query.replace(' ', '+').replace('/', "%2F").replace('–', '') + '+faculty'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'})
    with urllib.request.urlopen(req) as response:
        r = response.read()
    plaintext = r.decode('utf8')
    links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
    for i in links:
        k = '/url?q=http'
        flag = True
        for j in forbidden:
            if j in i:
                flag = False
        if len(i) > len(k) and i[:len(k)] == k and flag:
            link = i[7:].split('&amp')[0]
            link = urllib.parse.unquote(link)
            possibleURLs.append(link)

    # for i in possibleURLs:
    #     print(i)

    res_data = {}
    res_url = ''
    res_num = 0

    for url in possibleURLs:
        for option in ['urllib', 'urllibs']:
            # print(option, url)
            try:
                r = view_html_structure(url, option)
            except:
                continue

            if len(r) > 1:
                return r, url

            # if len(r) < 6:
            #     continue
            # valid_data = 0
            # for i in r:
            #     for j in i.values():
            #         if j != 'Missing':
            #             valid_data += 1
            # if len(r) >= 7 and valid_data / (5 * len(r)) > 0.56:
            #     return r, url
            # if len(r) > 20 and valid_data / (5 * len(r)) > 0.36 and r[0]['Name'] != 'Missing':
            #     return r, url
            # if valid_data > res_num:
            #     res_url = url
            #     res_data = r.copy()
            #     res_num = valid_data
    return res_data, res_url

university = 'UIUC'
department = 'Computer Science'
data, url = find(university, department)
print(data, url)


# r = view_html_structure('https://www.ashland.edu/cas/faculty-staff', 'urllib')
# for i in r:
#     print(i['Name'])

# if __name__ == "__main__":
#     # args: university name + worker ID
#     start = datetime.now()

#     name = " ".join(sys.argv[1: -1])
#     tmp = name.split('_')
#     university = tmp[0]
#     department = tmp[1]
#     r, url = find(university, department)

#     end = datetime.now()
#     t = end - start

#     res = {}
#     res['task'] = 'faculty'
#     res['university'] = university
#     res['department'] = department
#     res['id'] = '_' + end.strftime("%d/%m/%Y-%H:%M:%S")
#     res['time_stamp'] = end.strftime("%d/%m/%Y-%H:%M:%S")
#     res['execution_time'] = str(t.seconds)
#     res['url'] = url
#     res['algo_version'] = 1
#     res['status'] = 'Success' if r else 'Fail'
#     res['data'] = r

#     name = name.replace('/', '-slash-')
#     f = open('output/' + sys.argv[-1] + '/' + name + '.json', 'w')
#     json.dump(res, f, indent=4)
#     for i in r:
#         print(i)
