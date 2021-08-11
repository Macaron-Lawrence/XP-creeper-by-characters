# from modules.getLinks import getlinks
# from modules.getLinks import getlinks
import requests
from lxml import html
import math

links = [
    'https://gelbooru.com/index.php?page=post&s=view&id=6349265&tags=arknights+rating%3Aexplicit',
    'https://gelbooru.com/index.php?page=post&s=view&id=6349239&tags=arknights+rating%3Aexplicit'
]  # getlinks()


heads = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'PHPSESSID': 'rmhsof5bmdujqv6qhodr7ccbt2; comment_threshold=0; post_threshold=0; fringeBenefits=yup'
}


def print33(indexnow, indextotal, title):  # 进度条
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10
    print('>> 正在抓取 |' + A + B + '| ' + str(C) + '% | ' + title, flush=True)


def ifempty(arr):
    if arr[0:1]:
        return arr
    else:
        return ['']


def getnotexist(lstnew, lstold):
    lst = []
    for i in lstnew:
        if i not in lstold:
            lst.append(i)
    return lst


def gettagsbycharacter(links):
    tags = {}
    _counter = 0
    last = {
        'tags': [],
        'source': '',
        'size': '',
        'uploader': ''
    }

    for link in links:
        print33(_counter, len(links), link)
        _counter += 1
        request = requests.get(link, headers=heads, timeout=(5, 20))
        content = html.fromstring(request.content)
        copyright = content.xpath(
            '//*[@id="tag-list"]/li[@class="tag-type-copyright"]/a/text()')
        _source = ifempty(content.xpath(
            '//*[@id="tag-list"]/li[text()="Source: "]/a/@href'))[0]
        _size = ifempty(content.xpath(
            '//*[@id="tag-list"]/li[contains(text(),"Size: ")]/text()'))[0]
        _uploader = ifempty(content.xpath(
            '//*[@id="tag-list"]/li[contains(text(),"Posted: ")]/a/text()'))[0]
        _tags = content.xpath(
            '//*[@id="tag-list"]/li[@class="tag-type-general"]/a/text()')
        if (_source, _size, _uploader) == (last['source'], last['size'], last['uploader']):
            _tags = getnotexist(_tags, last['tags'])

        if not(copyright[0:1]):
            if 'nocopyright' not in tags:
                tags['nocopyright'] = {}
                tags['nocopyright']['tags'] = []
            tags['nocopyright']['tags'].extend(_tags)

        elif copyright[0] != 'original':
            chars = content.xpath(
                '//*[@id="tag-list"]/li[@class="tag-type-character"]/a/text()')
            for i in chars:
                if i not in tags:
                    tags[i] = {}
                    tags[i]['tags'] = []
                tags[i]['tags'].extend(_tags)

        else:
            if 'original' not in tags:
                tags['original'] = {}
                tags['original']['tags'] = []
            tags['original']['tags'].extend(_tags)

        (last['source'], last['size'], last['uploader'],
         last['tags']) = (_source, _size, _uploader, _tags)
    return tags


# gettagsbycharacter(links)
