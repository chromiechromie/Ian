myData = {1: 'Aragaki Yui', 2: 'GAKKI', 3: 'Nagasawa Masami'}


def xx():
    print('----------分割线ヾ(◍°∇°◍)ﾉﾞ分割线----------')


# # 打开文件
# f = open('D:/routine/python/routine3IO.txt', 'r')
# # 读取文件内容
# str1 = f.read()
# print(str1)
# # 很重要
# f.close()
#
# # 正确写法
# try:
#     f = open('D:/routine/python/routine3IO.txt', 'r')
#     print(f.read())
# finally:
#     if f:
#         f.close()

# 正正确写法
with open('D:/routine/python/routine3IO.txt', 'r') as f:  # 相当于try catch
    print(f.read())

with open('D:/routine/python/routine3IO.txt', 'r') as f:  # 相当于try catch
    for line in f.readlines():
        print(line.strip())  # 把末尾的/n 去掉 --- 啥意思!!!∑(ﾟДﾟノ)ノ

# 图片 , 视频属于二进制文件
with open('D:/routine/python/routine3IOA.jpg', 'rb') as f:  # 相当于try catch
    print(f.read())
with open('D:/routine/python/routine3IO.txt', encoding='utf-8') as f:  # 定义字符编码类型
    print(f.read())

# 写文件

with open('D:/routine/python/routine3IO.txt', 'w') as f2:
    f2.write('2.Hello World2')

# 内存中的IO

from io import StringIO

f3 = StringIO()
f3.write('hwll')
print(f3.getvalue())
#
# f4 = StringIO('xxxx\nxxxx')
#     while True:
#         s = f4.readlines()
#         if s == '':
#             break
#         print(s.strip())


# import pickle
#
# d = dict(name='a', id=2, score=99)
# #
# # with open('D:/routine/python/routine3IO.txt', 'rb') as f5:
# #     pickle.dump(d, f5)
#
# f6 = open('D:/routine/python/routine3IO.txt', 'rb')
# pickle.dump(d, f)
# f.close()

xx()
import json

d = dict(myData)
j1 = json.dumps(d)
print(type(j1))
print(j1)

j2 = json.loads(j1)
print(j2)

class per(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age


s = per(myData[1],myData[2])
print(s.name)

def per2dict(per):
    return {
        'name':per.name,
        'age':per.age
    }
print(json.dumps(s,default=per2dict))


xx()
# 总结 将dict转为json

myData2 = {"1": "Aragaki Yui", "2": "GAKKI", "3": "Nagasawa Masami"}
# json_dict = json.loads(myData2)
# for v in json_dict.item:
#     print(v)
dict_json = json.dumps(myData2)
dict_json = json.dumps(myData)
print(type(dict_json))
print(dict_json)
# 总结 将json转为dict
json_obj = dict_json
json_dict = json.loads(json_obj)
print(type(json_dict))
for k,v in json_dict.items():
    print(k,v)
