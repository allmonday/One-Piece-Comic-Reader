from pyquery import PyQuery as pq
import json
import requests
import os.path


LAST_PAGE = 1000
page_prefix = "index_{}.html"

pages = None

class EndException(Exception):
    pass

def getPageContent(url):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Referer':'http://manhua.fzdm.com/2/'
    }

    r = requests.get(url, headers=headers)
    if r.text == 'Not Found':
        raise EndException('end!')
    else:
        return r.text

def getImageUrl(url):
    print url
    content = getPageContent(url)
    if content:
        d = pq(content)
        img_url = d('#mhpic').attr('src')
        print img_url
        return img_url
    else:
        return None

def addToUrls(collection, url):
    image_url = getImageUrl(url)
    if url:
        collection.append(image_url)

def saveToJson(collection, dest):
    dump_data = json.dumps({"data": collection})
    with open('links/{}'.format(dest), 'w') as f:
        f.write(dump_data)

def checkJsonExisted(dest):
    return os.path.isfile('links/{}'.format(dest))

def main():
    with open('./one-piece.json', 'r') as f:
        pages = json.loads(f.read())
        pages = pages['data']

    for page in pages:
        pid = page['id']
        if checkJsonExisted(pid):
            print '{} is done, pass'.format(pid)
            continue

        image_urls = []
        link = page['link']
        first_page = link 
        addToUrls(image_urls, first_page)

        try:
            for i in range(1, LAST_PAGE):
                others = link + page_prefix.format(i)
                addToUrls(image_urls, others)

        except EndException as e:
            pass

        finally:
            saveToJson(image_urls, pid)

if __name__ == "__main__":
    main()
