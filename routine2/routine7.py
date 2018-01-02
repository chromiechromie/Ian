from bs4 import BeautifulSoup
import requests
url ='https://www.tripadvisor.cn/Tourism-g294211-China-Vacations.html'
url2 ='http://www.jianshu.com/p/14be3adf60d7'
web_data1 = requests.get(url)
web_data2 = requests.get(url2)
soup = BeautifulSoup(web_data1.text,'lxml') #注意 是web_data1.text
soup2 = BeautifulSoup(web_data2.text,'lxml') #注意 是web_data1.text
# print(soup)
# titles = soup.select('#BODYCON > div:nth-child(2) > div:nth-child(1) > div > div.photoLinksWrapper > div.navLinks > ul > li.trips > a')
# print(titles)
# titles2 =soup2.select('body > nav > div > a.btn.sign-up')
# print(titles2)
# titles3 =soup2.select('a.btn ')
# print(titles3)
titles4 =soup2.select('div.note')
print(titles4)
