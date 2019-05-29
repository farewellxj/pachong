# -*- coding: utf-8 -*-
"""
Created on Wed May 29 22:35:00 2019
@author: farewell
"""
import re
from urllib import request
from bs4 import BeautifulSoup as bs

def get_html(urls):
    resp_ = request.urlopen(urls)
    html_info = resp_.read().decode('utf-8')
    return html_info

def get_content(htmls_info,part='div',id_='ozoom'):
    soup = bs(htmls_info, "lxml")    
    content = soup.find_all(part,id = id_ )
    return content

def text_htmls(contents):
    texts_ = str(contents)
    texts_tmp = texts_.replace(u'\u3000',u'')
    contents_ = re.findall('<p>(.{0,})</p>',texts_tmp)
    return contents_

def replace_p(text_):
    text_ = str(text_)
    text_ = text_.replace('<p>',"")
    text_ = text_.replace('</p>',"")
    text_  = text_.replace('\\xa0',u"")
    return text_

def creat_url(dates):
    fine_url = None
    if isinstance(dates,int) != True:
        print('Date type error,should like yyyymmdd')
    else:
        dates = str(dates)
        yyyy = dates[:4]
        mm = dates[4:6]
        dd = dates[6:8]
        fine_url = 'http://paper.people.com.cn/rmrb/html/'+yyyy+'-'+mm+'/'+dd+'/'+'nw.D110000renmrb_'+str(dates)
    return fine_url

print(creat_url(20191224))

today = input('Input the day you want to fetch:like 20181231\n')
request_url = []
for i in [1,2,3,4,5,6]:
    for j in range(1,25):
        urls = creat_url(int(today))
        f = lambda x:'0'+str(x) if x<10 else str(x)
        url_s= urls + '_'+str(i)+'-'+str(f(j))+'.htm'
        request_url.append(url_s)

#request_url[:5]

news = []
for i in request_url:
    try:
        s = get_html(i)
        p = get_content(s)
        t= text_htmls(p)
        r = replace_p(t)
        news.append(r)
        print('News have been download!')
    except:
        print('Url error,pass it!')
        
with open( today+'.txt','w',encoding='utf-8') as w:
    for new in news:
        w.writelines(new)
        w.writelines('\n'*2)
print('News have been saved!\n')


try:
    import jieba.analyse as analyse
except:
    print("Make sure your're already installed jieba.")
    
str_new = str(news)
top_k_words = analyse.extract_tags(str_new, topK=10, withWeight=False, allowPOS=('n','v'))
print("今日关键词:\n")
for top_,words_ in enumerate(top_k_words):
    print("Top {b} : {a}".format( b = top_ + 1,a = words_))
print("-"*10 + "Finish line" + "-"*10)











