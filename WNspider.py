# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas
import urllib

'''
import re
m = re.search('doc-i(.*).shtml',url)
id = m.group(1) 0 - all content, 1 - (.*)

'''

'''functions defined'''

def getNewsDetails(link):
    subres = requests.get(link)
    subres.encoding = 'utf-8'

    ssoup = BeautifulSoup(subres.text, 'html.parser')
    pList = ssoup.select('#artibody p')  # .article
    tDiv = ssoup.select('.date-source')  # '.date-source span a'


    try:
        spanList = tDiv[0].select('span')
        date = spanList[0].text
        src = spanList[1].text
    except IndexError:
        try:
            # print('first try', link)
            date = ssoup.select('.time-source')[0].contents[0].strip()  # lstrip('content need to be removed')
            src = ssoup.select('.time-source span a')[0].text
        except IndexError:
            try:
                # print('second try', link)
                date = ssoup.select('#pub_date')[0].contents[0].strip()
                src = ssoup.select('#media_name')[0].text.strip('\n').strip('xa0')
            except IndexError:
                # print('other', link)
                date = '2017年'
                src = '新浪新闻'

    article = []
    # pList = sDiv[0].select('p')
    for p in pList:  # ' '.join([p.text.strip() for p in ssoup.select('#artibody p')])
        if p.text != ' ' and p.text.rfind('function') == -1:
            article.append(p.text.strip())

    sArticle = ' '.join(article)  # '\n'.join(article)

    info = [date, src, sArticle]


    return info

'''main flow'''

kw = 'microsoft'
#kw = '微软'
newsSet = []

for page in range(1, 2):
    # newsurl = 'http://search.sina.com.cn/?q={0}&c=news&from=channel&ie=utf-8'.format(kw)
    newsurl = 'http://search.sina.com.cn/?q={}&c=news&from=channel&ie=utf-8&col=&range=&source=&country=\
    &size=&time=&a=&page={}&pf=2131425464&ps=2134309112&dpc=1'.format(urllib.parse.quote(kw), page)

    res = requests.get(newsurl)

    soup = BeautifulSoup(res.text, 'html.parser')

    dList = soup.select('.box-result .r-info2')

    for div in dList:
        h2 = div.select('h2 a')[0].text
        link = div.select('a')[0]['href']
        # source = div.select('.fgray_time')[0].text

        content = getNewsDetails(link)
        newsSet.append([h2, content[0], content[1], content[2]])
        print(content)

df = pandas.DataFrame(newsSet)
df.columns = ['Tile', 'Date','Source', 'Text']
df.to_json(path_or_buf='newsSete.json', orient='index', force_ascii=False)











