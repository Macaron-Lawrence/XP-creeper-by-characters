import math
import time
def render(obj:dict,title:str,subtitle:str,type:str,mode:str):
    _i = {
        '%inall':[2,'占该角色所有色图的百分比'],
        '%inalltags':[3,'占该角色所有标签百分比'],
        'count':[1,'总计']
    }
    _mode = 2
    if mode:
        _mode = _i[mode][0]
    html = ''
    temp = {}
    temp['text'] = '"'+title+'"'
    temp['subtext'] = '"'+subtitle+'"'
    temp['name'] = '"' + _i[mode][1] +'"'
    arr = obj[list(obj.keys())[0]]
    arr.sort(key=lambda k:k[_mode])
    if type == 'pie':
        (temp,html) = pie(arr,temp,_mode)
    if type == 'bar':
        (temp,html) = bar(arr,temp,_mode)
    for i in temp.keys():
        html = html.replace('{%=' + i + '%}',temp[i])
    with open('./html/'+ title +'_' + subtitle +'_' + mode + '_'+ str(math.floor(time.time()))+ '.html','w',encoding='utf-8') as F:
        F.write(html)

def pie(arr,temp,_mode):
    temp['data'] = ''
    for i in arr:
        temp['data'] +='{value: '+ str(i[_mode]) +', name: "'+ i[0] +'"},'
    temp['data'] = temp['data'][:-1]
    with open('./templates/pie.xml', 'r', encoding='utf-8') as f:
        html = f.read()

    return temp,html


def bar(arr,temp,_mode):
    temp['data'] = ''
    temp['yaxis'] = ''
    for i in arr:
        temp['data'] +=str(i[_mode]) +','
        temp['yaxis'] +='"'+i[0] +'",'
    temp['data'] = temp['data'][:-1]
    temp['yaxis'] = temp['yaxis'][:-1]
    with open('./templates/bar.xml', 'r', encoding='utf-8') as f:
        html = f.read()

    return temp,html