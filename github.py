#-*- coding:utf-8 -*-
'''
author:niuniuniuniuniu
github:https://github.com/niuniuniuniuniu
'''
import requests
import re
import sys
import time
import json
from bs4 import BeautifulSoup as bsp
def get_token(urllogin,header):
    try:res=requests.get(urllogin,header)
    except:
        print u"获取token失败"
        sys.exit()
    result=res.text
    key=re.compile(r'name\=\"authenticity_token\"\s*value=\"\S*') 
    match=key.search(result)
    if match:
        authenticity_token=match.group().strip('name="authenticity_token" value=" ')+'=='
    cookie=res.cookies.get('_gh_sess')
    return authenticity_token,cookie
def github_login(urlsession,header,authenticity_token,user,passwd,gh_sess):
    data={"commit":"Sign in",
          "authenticity_token":authenticity_token,
          "login":user,
          "password":passwd}
    cookie={"_gh_sess":gh_sess}
    try:res=requests.post(urlsession,data,headers=header,cookies=cookie)
    except:
        print u"登录失败"
        sys.exit()
    return res.cookies.get('user_session')
    print res.status_code
    print res.history
def github_search(url,session,header,keyword,urllist):
    for key in keyword:
        key=key.replace(' ','+')
        url=url+key+"&type=Code"
        cookie={'user_session':session}
        try:res=requests.get(url,headers=header,cookies=cookie)
        except:
            print u'搜索关键字失败'
            sys.exit()
        soup=bsp(res.text,"html.parser")
        a=soup.find_all('div',class_="d-inline-block col-10")
        for i in a:
            c=i.find_all('a')
            urllist.append(json.loads(c[1]['data-hydro-click'])['payload']['result']['url'])
    return urllist
if __name__=='__main__':
    keyword=['Created by *** on','Created by *** on','*** database','*** mysql']
    urllist=[]
    user="***@qq.com"
    passwd="****"
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer":"https://github.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests":"1"}
    urllogin="https://github.com/login"
    urlsession="https://github.com/session"
    url="https://github.com/search?q="
    authenticity_token,gh_sess=get_token(urllogin,header)
    gh_sess=gh_sess.replace('%3D','=')
    session=github_login(urlsession,header,authenticity_token,user,passwd,gh_sess)
    urllist=github_search(url,session,header,keyword,urllist)
    if len(urllist)>0:
        ids=list(set(urllist))
        for i in ids:
            print i
