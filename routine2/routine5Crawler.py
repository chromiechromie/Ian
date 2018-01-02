__author__ ='Ian'
from bs4 import BeautifulSoup

import urllib.request
import urllib.parse
import re
import urllib.request,urllib.parse,http.cookiejar

def getHtml(url):
    cj = http.cookiejar.CookieJar #模拟登陆
    opener =urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders=[('User-Agent',)]


soup = BeautifulSoup(open(''))