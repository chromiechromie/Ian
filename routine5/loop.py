# continue 跳过奇数
x = 10
if 1 == 1:
    print(x * 2)
    while x:
        x = x - 1
        if x % 2 != 0:
            continue    # 跳到循环顶部 跳到while 不是if
        print(x, end=' ')
print(end='\n')
a = [[2, 3], [0, 3], [1, 2]]
b = dict([(0, 1), ('a', 'b')])
for x, y in b.items():
    ...

'''
    任何赋值目标在语法上都能用在for循环这个关键字上
'''
for x, y in a:
    print(x, y)

for i in a:
    if 1 == 1:
        ...
else:  # 可以理解为,不碰到break 就总是会执行
    print('wtf', end='!')

'''
    *x 可以收集多个元素
'''
for x in a:
    x.extend(x)

for a, *b, c in a:
    print(a, b, c)

'''
    range(10) ==> 0~9
    range(1,10) ==> 1~9
    range(4,-1,-2) 步进值
'''
print(list(range(4, -1, -2)))
print(list(range(4, -1, 2)))  # 这样的返回值是[]

'''
    for 和 range
'''
# 遍历索引值
# 你的代码
count = 0
for a in [0, 1, 2]:
    print(count, 'is', a)
    count += 1
# 别人家的代码
print('别人家的代码')
list1 = [0, 1, 2]
for a in range(len(list1)):
    print(a, 'is', list1[a])

str = '阿斯顿发生法司法'
# 2 为分片中的步长
for i in str[::2]:
    print(i)

list2 = [i + 1 for i in list1]
# 注意下面这种方式是不行的,zip接收的argument #2 must support iteration
# list3 = zip(list1,list2.append('gakki'))
list2.append('gakki')
print(list2)
list3 = list(zip(list1, list2))
print(list3)

'''
    zip构造dict
    zip 截断到最短的可迭代对象 (先这么叫着)
'''
dict1 = dict(zip(list1, list2))
print(dict1)

'''

'''

for (k, v) in enumerate(dict1):  # ????
    print(k, v)
for k in enumerate(dict1):  # ????
    print(k)

for k, v in dict1.items():
    print(k, v)

with open('D:/routine/python/IO.txt', 'r') as f:
    lines = f.readlines()
lines = [line.rstrip() for line in lines]
# print(lines)
str_path = 'D:/routine/python/IO.txt'
f = open(str_path, 'r')
# for i in f:
#     print(i, end='')

print(type(f))
str_list = f.readlines()
print(type(str_list))

'''
    迭代文件
    看起来最low,实际上最好用
    1.readlines 从内存的使用来看,效果不佳
    2.一次迭代一行,
'''
f = open('D:/routine/python/IO.txt', 'r')
for i in f:
    print(i, end='')

'''

'''
lines = f.readlines()

'''
    文件层面的列表解析
    readlines 返回一个列表,列表中的每个元素都有一个'\\n'
'''

lines = [i.rstrip() for i in open('D:/routine/python/IO.txt') if i[0] == 'p']

# 将两个list_str 中的字符两两拼装


list2.pop(-1)
list2.append(10)
list_str = [x + y for x in list1 for y in list2 if x + y]
# 返回一个3*3的笛卡尔积
print(list_str)

'''
    enumerate & dict
'''

dict_f = {
    key: value for key,
    value in enumerate(
        open('D:/routine/python/IO.txt')) if value[0] == 'p'}

print(dict_f)

'''
    map 返回值是迭代器以节省内存
'''

m = map(abs, [1, 2, -3])

'''
    可迭代对象 ==> 迭代器Iterator

'''
dict_num = dict(a=1, b=2, c=3)
print(type(dict_num.keys()))
# next(dict_num.keys()) 会报错,因为dict_num.keys() 是一个可迭代对象
# 但是 for循环是可以接收它的
# 只是不能使用next()内置函数
for i in dict_num.keys():
    print(i)
# 可迭代对象转为迭代器
k = dict_num.keys()
k = iter(k)
print(next(k))
# 列表解析无法返回多个list list_key, list_val = [ (v,k) for v,k in dict_num.items()]


def intersect(l1, l2):
    '''
    :param l1: list
    :param l2: list
    :return: list 两个list的交集
    '''

    res = [i for i in l1 if i in l2]
    return res


l1 = [1, 2, 3]
l2 = [2, 3, 4]

l3 = intersect(l1, l2)
print(l3)


def xx():
    global xxxx
    xxxx = 'gakki'


# print('函数运行之前,x会被声明但并没有被赋值', xxxx)
xx()
print('感觉global还是少用为妙', xxxx)
'''
    工厂函数(了解即可)
    lambda 和 类 将会解决这个问题
'''
# 留给 本机
x = 22


def f1():
    x = 11

    def f2(x=x):
        print(x)
    f2()


f1()

'''
    函数赋值
    参数的不可变性?????
'''

A = 1
B = [0, 1]


def changer(a, b):
    # 这个变量不会被影响,因为他是不可变类型,仅仅是把本地变量a 修改为引用一个完全不同的对象,
    # 并没有改变调用者作用于中 的名称A 的绑定
    a = 10
    # 它传入的是一个可变的对象 这里涉及到共享引用的机制
    b[0] = 'gakki'


changer(A, B)

print('不可变参数(整数):A==>', A)
print('可变参数(list):B==>', B)

'''
    函数参数匹配模式
'''


def parameter_t(a, b, c=2, d=1, *args, **kwargs):
    print(a, b, c, d, args, kwargs)

# 默认位置从左到右匹配


parameter_t(0, 1, 2, 3)

# 关键字参数
# 关键字必须唯一
# 位置函数优先级最高,不要与他产生冲突

parameter_t(a=1, b=2, c=3, d=4)

# 默认参数 函数头部变量d默认值为1

parameter_t(0, 2, c=3)

# 收集参数*arg
# 位匹配的参数会被收集到arg元组中

parameter_t(1, 2, 3, 3, 4, 5)

# 收集参数(二)
# 仅接收关键字参数
# **kwargs 为字典

parameter_t(1, 2, 3, 3, 4, 5, name='Ian')  # 1 2 3 3 (4, 5) {'name': 'Ian'}

# 解包参数
# 但我们不能预测将要传入函数的参数的数量时

# parameter_t((1, 2, 3)) 此时 我们相当于令a = 元组(1,2,3) b参数没有赋值

args = (1, 2, 3)
parameter_t(*args)   # 1 2 3 1 () {}

# 同理 **kwargs 对字典类生效 换句话说是关键字参数
kwargs = dict(a=1, b=2, d='gakki')
parameter_t(**kwargs)  # 1 2 2 gakki () {}

# 解包混用

parameter_t(1, 2, *args)  # 1 2 1 2 (3,) {}

# 混用 加强版


def tracer(func, *pargs, **kargs):
    print('calling:', func.__name__)
    return func(*pargs, **kargs)


def func(a, b, c, d):
    return a + b + c + d  # 注意这种表达式不能str 与 int混用


print(tracer(func, 1, 2, c=3, d=4))

# Keyword-Only 参数
# 在*b 之后 必须使用关键字参数 kwonly(1,2,3) 这种会抛异常
# *表示不接受变量长度的参数列表


def kwonly(a, *b, c):
    print(a, b, c)


kwonly(1, 2, c=3)  # 1 (2,) 3

# ** 不要与keyword连用

