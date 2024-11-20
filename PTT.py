# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 15:15:22 2024

@author: ASUS
"""
#以下程式碼可以爬取PTT八卦版第一頁的內容
import requests as rq
from bs4 import BeautifulSoup as bs
header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
payload={'from': '/bbs/Gossiping/index.html','yes':'yes'}  #處理網頁18禁問題
session=rq.Session()
session.post('https://www.ptt.cc/ask/over18',data=payload,
             headers=header)
r=session.get('https://www.ptt.cc/bbs/Gossiping/index.html')

if r.status_code==rq.codes.ok:
    cut=r.text.split('r-list-sep')[0] #只抓取分隔線以上的內容
    soup=bs(cut,'html.parser')
    title=soup.select('div.title>a')
    date=soup.select('div.meta>div.date')
    for i,d in zip(title,date):
        if i.text[0:3]!='Re:': #過濾網友回復的內容
            print('---------------------------------')
            print(i.text) #印出貼文標題
            print('---------------------------------')
            r2=session.get('https://www.ptt.cc'+i.get('href'),
                        headers=header) #抓取貼文的超連結,並照訪
            soup2=bs(r2.text,'html.parser')
            sptime=soup2.select('div.article-metaline>span.article-meta-value')[2].text
            print(r2.text.split('※ 發信站: 批踢踢實業坊(ptt.cc)')[0].split(sptime)[1].split('</span></div>')[1].split('<span class="f2">')[0]) #去除留言以及多餘的元素
            print(d.text) #印出日期
            