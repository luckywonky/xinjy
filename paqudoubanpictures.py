import time
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
baseurl = 'https://read.douban.com'
path = '/ebooks/'
absoluteurl = baseurl + path
html = urlopen(absoluteurl)
bsObj = BeautifulSoup(html,'lxml')
tags = bsObj.find('ul',class_='list categories-list')
for i in tags.children:
    path = i.a['href']
    absoluteurl=baseurl+path+'?cat=book&sort=top&start='
    k = 0
    while k<999:
        absoluteurl = absoluteurl + str(k)
        html1 = urlopen(absoluteurl)
        bsObj1 = BeautifulSoup(html1,'lxml')
        a = bsObj1.findAll('div', class_='cover shadow-cover')
        b = bsObj1.findAll('div', class_='title')
        time.sleep(5)
        c = [urlretrieve(i.img['src'],'E:\python project\spider\downloaded\%s.jpg'%j.get_text()) for (i,j) in zip(a,b)]