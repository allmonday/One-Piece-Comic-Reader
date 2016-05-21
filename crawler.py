from pyquery import PyQuery as pq
import json

d = pq(url='http://manhua.fzdm.com/2/')
links = d('.pure-u-1-2 a')
formatted = []
prefix = 'http://manhua.fzdm.com/2/'

links.reverse()

for idx, li in enumerate(links):
    dl = pq(li)
    formatted.append({"name": dl.text(), "link": prefix + dl.attr('href'), "id": idx})

dumps = json.dumps({"data": formatted})

with open('one-piece.json', 'w') as f:
    f.write(dumps) 

print 'updated'
