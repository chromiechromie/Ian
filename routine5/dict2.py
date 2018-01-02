# 创建字典的写法
var = {'name': 'gakki', 'age': '23'} # 其实一二是一种方法,但是书上这样写,能有啥办法
d = {}
d['name'] = 'gakki'
d['age'] = 23
# 注意dict是关键字,只是不报错,不能乱用

var3 = dict(name='gakki', age=23) # 关键字创建字典,看起来有点高大上,但是,键必须都是字符串
# 在程序运行时,把key&value逐步建成序列,通常与zip连用
var3 = dict([('name', 'gakki'), ('age', 45)])
# 键和值都相同的字典的初始化
var4 = dict.fromkeys(['name', 'age'], 'xx')

print(var4)

'''
    广度还是 ->精度<-
'''
# zip
# 字典解析 对每一个key - value 构建一个dict
D = {k: v for (k, v) in zip(['a', 'b', 'c'], [1, 2, 3])}
print(D)

D = {x: x**2 for x in [1, 2, 3]}
print(D)

D = {'a'+x: x*4 for x in 'gakki'}
print(D)

D = {c.lower(): c +'!' for c in ['Gakki', 'Gal']}
print(D)

# --------
# t
