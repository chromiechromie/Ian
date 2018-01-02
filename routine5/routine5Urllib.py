import urllib.request
import urllib3
import urllib.error
import socket
http = urllib3.PoolManager()
res = urllib.request.urlopen('https://www.baidu.com/')
# print(res.read().decode('utf-8'))
try:
    response = urllib.request.urlopen('http://httpbin.org/', timeout=1) # 相应时间超过1s
except urllib.error.URLError as e:
    if isinstance(e.resson, socket.timeout):
        print('time out')

print(type(response)) # <class 'http.client.HTTPResponse'>

response2 = urllib.request.urlopen('http://httpbin.org/')
print(response2.status)                      # 返回状态码
print(response2.getheaders())   # 返回头
# print(response2.getheaders('Server'))  # 这个为啥不能用??? 会抛异常
# read 获取相应体内容,decode转为utf-8
print(response2.read().decode('utf-8'))







