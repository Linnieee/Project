#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:55:30 2020

@author: linnie
"""

import requests
from bs4 import BeautifulSoup
import pandas 
print('sucess!')

uo = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=20&type=T'


def get_urls(n):
    '''
    【分页网页url采集】函数
    n： 页数菜蔬
    结果： 得到一个分页网页list
    '''
    lst = []
    for i in range(n):
        urli = 'https://book.douban.com/tag/%%E5%%B0%%8F%%E8%%AF%%B4?start=%i&type=T'%(i*20)
         ## 因为后面%具有含义，所以地址里的%需要改成%%
        lst.append(urli)
    return lst


    
def get_dataurls(ui,dict_h,dict_c):
    '''
    【数据信息网页url采集】
    ui：分页网址
    dict_h: user-agent
    dict_c: cookies                     
    '''
    ## 请求访问url
    ri = requests.get(url = ui, headers = dict_h, cookies = dict_c)
    ## 解析页面
    soup = BeautifulSoup(ri.text, 'lxml')
    
    ul =  soup.find('ul', class_ = "subject-list")
    lis = ul.find_all('li')
    lst2 = []
    for li in lis:
        lst2.append(li.find('a')['href'])
    return lst2


def get_data(ui, d_h,d_c):
    '''
    【获取具体的数据信息】
    ui： 数据信息网页
    d_h: user-agent信息
    d_c: cookies 信息
    '''
    ri = requests.get(ui, headers = dict_h, cookies = dict_c)
    soup = BeautifulSoup(ri.text, 'lxml')
    
    dic = {}
    dic['书名'] = soup2.find('div', id = 'wrapper').h1.text.replace('\n','')
    dic['评分'] = soup2.find('div', class_ = 'rating_self clearfix').strong.text.replace(' ','')
    dic['评价人数'] = soup2.find('a', class_ = 'rating_people').text
    infos = soup2.find('div',id = 'info').text.replace(' ','').split('\n')
    for i in infors:
        if ':' in i:
            dic[i.split(':')[0]] = i.split(':')[1]
        else:
            continue
    
    return dic
    

if __name__ == "__main_":
    ## 获取分页网址
    urllist1 = get_urls(10)
    print(urllist1)
    
    ## 获取登录信息
    dict_h = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    dict_c ={}
    cookies = 'bid=LVERotvqgTY; __gads=ID=2b583cd94cdc5207:T=1588654524:S=ALNI_MaKqZig4lO0ys1e0JhQWeBzDblv4A; __utmz=30149280.1592188641.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ll="118168"; __utma=30149280.1488860382.1588654544.1592188641.1594362689.5; __utmc=30149280; ap_v=0,6.0; __utma=81379588.1665461399.1594362690.1594362690.1594362690.1; __utmc=81379588; __utmz=81379588.1594362690.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=D95C1CED89359DABC21D342B60788E596|9bc2c40083d27d7c8769f63838c29c76; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1594362692%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; gr_user_id=1deacb4d-c5cb-460d-8399-c08e942a7474; __yadk_uid=Ne5oDiZfMzojZVsu9TtoiRQXqRy6IWhi; Hm_lvt_cfafef0aa0076ffb1a7838fd772f844d=1594362742; Hm_lpvt_cfafef0aa0076ffb1a7838fd772f844d=1594362742; ct=y; _pk_id.100001.3ac3=bd96d1e1c6b95264.1594362692.1.1594364490.1594362692.; __utmt_douban=1; __utmb=30149280.6.10.1594362689; __utmt=1; __utmb=81379588.5.10.1594362690'
    for i in cookies.split('; '):
        dict_c[i.split('=')[0]] = i.split('=')[1]
    
    ## 获取数据信息网页
  
    urllist2 = []
    for u in urllist1:
        try:
            urllist2.extend(get_dataurls(u,dict_h,dict_c))
            print('数据信息网页获取成功，总共获取%i条网页' % len(urllist2))
        except:
            print('数据信息网页获取失败，分页网址为：',u)
    print(urllist2)
    
    ## 获取每一页采集的数据
    datalist = []
    errorlist = []
    for u in urllist2:
        try:
            datalist.append(get_data(u,dict_h,dict_c))
            print('数据采集成功，总共采集%i条数据' % len(datalist))
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：',u)
    print(datalist)
    
    ## 数据清洗
    datadf = pd.DataFrame(datalist)
    datadf['评分'] = datadf['评分'].astype('float')
    datadf['页数'] = datadf['页数'].str.replace('页','').astype('float')  
    datadf['评价数量'] = datadf['评价数量'].str.split('人').str[0].astype('int')  
    
    ## 导出excel
    datadf.to_excel('result.xlsx')

    print('Finish!!')
       

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    