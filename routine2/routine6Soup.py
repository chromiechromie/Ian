from bs4 import BeautifulSoup

with open('D:/temp/111.html','r',encoding='utf-8') as web_data:
    Soup = BeautifulSoup(web_data,'lxml')
    images = Soup.select('body>div.home_banner>a>img')
    # images = Soup.select('body>div')
    # print(images)
with open('C:/Users/Ian/WebstormProjects/untitled/app/view1/js_Routine/routine1h5_form.html','r',encoding='utf-8') as web_data2:
    Soup = BeautifulSoup(web_data2, 'lxml')
    # ?source = Soup.select('body')
    # print(source)
    # source2 =Soup.select('body > div.t2')
    # print(source2)
    img =Soup.select('body > div.t2 > img')
    print(img)
    t1 = Soup.select('body > div.t1 > div > div.div1 > img') # 注意必须加入空格
    print(t1)
    print('xxxxxxxxxxxxxxxxxxxx')
    t3 = Soup.select('body > div.t1 > img ')
    print(t3)

    a1 = Soup.select('body > div.t3 > a ')
    print(a1)
for text in a1:
    print(text.get_text())  #筛选出标签信息

for imgs,text in zip(t1, a1):
    data={
        'text' : text.get_text(),   #注意这里是text
        'imgs' : imgs.get('src')
    }
    print(data)