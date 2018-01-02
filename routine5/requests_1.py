import requests

# responese = requests.get('https://www.baidu.com/') # 发送请求
# print(responese.text)
# print(responese.headers)
# print(responese.status_code)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
response = requests.get('https://www.zhihu.com/', headers=headers)  # 发送请求 知乎的话,必须加上user-agent
print(response.text)

response = requests.get('https://ss0.bdstatic.com/k4oZeXSm1A5BphGlnYG/icon/95520.png')  # 发送请求
# print(response.content)
# with open('D/1.gif', 'wb') as f:
#     f.write(response.content)
#     f.close()

from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.zhihu.com/')

