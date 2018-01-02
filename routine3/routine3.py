str1 = 'tiTle'
myData = {1: 'Aragaki Yui', 2: 'Gakki', 3: 'Nagasawa Masami'}
myData2 = {"1": "Aragaki Yui", "2": "Gakki", "3": "Nagasawa Masami"}
print(str1.title())
# 将首字母大写

# 大小写转换
print(str1.upper())
print(str1.lower())  # 举个栗子用户存入进数据库的信息,应该统一小写,可能会用的到

# 拼接字符串
# 使用+拼接字符串
print(myData[1]+"&"+myData[2])

# \t 加一个空格
print("\tGakki")

# \n 换行符,在" "中使用
print(myData[1], "\n", myData[2]+"^^^"+myData[3])

# 删除空白
# rstrip() 删除末尾空白
str3 = ' gakk i '
print(str3.rstrip()+"x")
print(str3+"x")
str3 = str3.rstrip()  # 删除空白
print(str3+"x")
# ** 幂运算
print(3**3)
# 将带有小数点的统称为浮点数
print(0.2+0.1) # 有意思的数据
a =1
print("x"+ str(a) +"xxc")
myData3 = ['a', 'b', 'c']
myData3.append('x')
print(myData3[-1])
myData3.insert(-1, 'gakki') # 相当于myData3.append('gakki') 所以没有任何意义
print(myData3)
# 删除list 中某个元素 ,长得有点怪??????
del myData3[2]
print(myData3, type(myData3))
# pop 删除并显示倒数第一个值,有点类似于栈    接收参数为想要弹出的位置
print(myData3.pop())
print(myData3)
print(myData3.pop(2))
print(myData3)

print(type(myData))
print(type(myData2))
print(type(myData3))
myData3.remove('a')
print(myData3)

myData3.append('gakki')
myData3.append('Aragaki Yui')
myData3.append('Nagasawa Masami')
myData3.remove('b')
# 排序 sorted() 临时排序
myData3.sort()
print(myData3)
print(len(myData3))
# 注意不要这样用
# print(myData3.sort())
for a in myData3:
    print(a)
# range
for v in range(2,4):
    print(v)
# 第三个参数的意思是,每生成一个数字,下一个数字加2
list_num = list(range(1, 10, 2))
print(list_num)
list_num_squares = []
for v in range(1, 11):
    list_num_squares.append(v**2)
print(list_num_squares)
print(max(list_num_squares), min(list_num_squares), sum(list_num_squares))
# 列表解析 炫技用法
list_num_squares2 = [v**2 for v in range(1, 11)]
print(list_num_squares2)
print(list_num_squares[:3])
# 元组 括号写法
dimensions = (200, 80)

for i in dimensions:
    print(i)

# 判断xx 是否在xx中
if 'gakk i' in myData3:
    print(myData3)

if 'gak ki' not in myData3:
    print(myData3)

myData2[4] = 'Ian'
print(myData2)
myData2['4'] = 'Ian'
del myData2[4]
print(myData2)
myData4 = [
    {
        'id': 1,
        'name': 'Gakki',
        'age': 23
    },
    {
        'id': 2,
        'name': 'Aragaki Yui',
        'age': 24
    },
]
print(myData4, type(myData4))
print(myData, type(myData))
print(myData2, type(myData2))

for k, v in myData.items():
    print("key:", k, "value:", v)
for id, name in myData.items():
    print("ID:", id, "Name:", name)

# 只遍历字典中的值(key) 据说这种输出是无序的
for number in myData.keys():
    print(number)
# 注意 myData 和 myData2 是dict myData4 是list
# ()元组 []list {}dict

# 按顺序遍历key
for num in sorted(myData.keys()):
    print(num)

for values in sorted(myData.values()):
    print(values)
# 注意变量值是会随着for 循环的结束而传递出来的
print(num)

# dict 用法总结
# add
myData[4] = 'Gal'
# del
del (myData[4])
# clear
# myData.clear()
# pop 接收的参数是 key 还是位置 我记得是位置
print(myData.pop(1))


myData[12] = 'Athena'
print(myData)
print(type(myData4))
while myData[12] in myData4:
    myData4.remove(myData[1])
    print(myData4)





