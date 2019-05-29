# -*- coding: utf-8 -*-
"""
Created on Wed May 29 23:20:55 2019

@author: farewell
"""
#pa qu <fan ren xiu xian zhuan>
import re 
import time
import requests
from bs4 import BeautifulSoup

main_html = "https://www.biquke.com/bq/71/71535/"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
}
response = requests.get(main_html,headers=headers)
response.encoding = 'UTF-8'
response = response.text
soup = BeautifulSoup(response,'lxml')

end_html = []
req  = r'<a href="(.*)?"\stitle.*'
for i in soup.find_all('a'):
    i = str(i)
    resu = re.findall(req,i)
    if len(resu)  == 0:
        pass
    else:
        end_html.append(resu[0])
#end_html[:5]
titles = []
req  = r'title="(.*)?">'
for i in soup.find_all('a'):
    i = str(i)
    resu = re.findall(req,i)
    if len(resu)  == 0:
        pass
    else:
        titles.append(resu[0])
#titles[:5]
url_pool = [main_html + str(ends) for ends in end_html]

singel_url = url_pool[4]
response = requests.get(singel_url,headers=headers)

response.encoding = 'UTF-8'
soup = BeautifulSoup(response.text,'lxml')

novel = soup.find_all(attrs = {'id':'content'})

book = []
print("Start down loading...")
for page,name in zip(url_pool,titles):
    time.sleep(0.5)
    response = requests.get(page,headers=headers)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text,'lxml')
    novel = soup.find_all(attrs = {'id':'content'})[0]
    content = novel.get_text()
    book.append(content)
    print(">>>",end =">")
    #For single page download:
    '''
    with open(name+'.txt','w',encoding='utf-8') as f:
        f.writelines(content)
        print('pages saved!')
    '''

with open('./download/mdzx.txt','w',encoding='utf-8') as w:
    for i,j in zip(book,titles):
        w.writelines(j)
        w.writelines(i)
print('\nFile saved')