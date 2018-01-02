dict = {'1':'gakki','gakkkki':'2'}
d = {}
# for i in range(1,9999):
#     d[i] = 'a'
#
# print(d)


def p(*kwargs):
    print(type(kwargs), '   ', kwargs)  # 注意这里type(kwargs) 永远是元组


def p(kwargs):
    print(type(kwargs), '   ', kwargs)  # 这样就变成你想要的了
# 字典的操作:
# 字典值更改


dict['1'] = [1, 2, 3]
p(dict)

# 删除
del dict['1']
p(dict)

# ADD
dict[3] = 'Gal Gadot'
p(dict)

# values 返回值列表
p(dict.values())
p(list(dict.values()))

# items() 返回对元组
p(list(dict.items()))


# 读取不存在的key会出错,so 使用get方法时可以填入默认值
dict [4] = ''
p(list(dict.items()))
print(dict.get(1))   # 当你在实际项目中操作是,这里是None是返回值,可能造成问题
print(dict.get(1, '10086')) # 10086 是默认值
print(dict.get(4, '1008611')) # 注意,dict[4] 是存在的,只是为空而已
# 合并update 用d2 覆盖 d1 或者说是粗暴地合并
# 注意,作者强调了好多遍,从左到右的顺序无关,dict无所谓顺序,然鹅目前为止,我无法直观地显示出这一结果
# Guido 保佑 不要是我理解的问题
d1 = {1:2}
d2 = {1:3,'1':123}
d1.update(d2)
print(d1)

# pop 删除一个键,并返回它的值
print(dict.pop(3))
p(dict)
#

table ={
    'Python': 'Guido van Rossum',
    'JavaScript': 'Brendan Eich',
    'C++': 'Bjarne Stroustrup',
    'Philosophy of design': ['明确', '优雅', '简单']
}
for rec in table:
    #  rec is key, table[rec] is value
    print(table[rec], rec)

# 效果等同于  keys() 的返回值是一个迭代器还是一个class (总之是<class 'dict_keys'>)
# 然鹅这里是一个list 喵?喵?喵?
for rec in table.keys():
    print(table[rec], rec)

#  <<<<<<------dict------>>>>>>
# 稀疏矩阵,使用dict创建,避免出现超大的几乎为空的数据结构(数据结构这个词用的不准确,然鹅,暂时想不到更好的描述词语)
# 换句话说就是多多维数组中只有极少数位置上有存储的value
# 未必需要用稀疏矩阵来举例

Matrix = {(2, 3, 4): 10, (7, 23, 1): 10}  # 声明一个dict

# 三种避免Missing-Key 方式
# 最无聊但可能最有效的一种
if (2, 3, 14) in Matrix:  # 默认是键
    print(Matrix[(2, 3, 14)])
else:
    print(0)

# 2
try:
    print(Matrix[(2, 3, 14)])
except KeyError:
    print('改键不存在')
# 常用且优雅
print(Matrix.get((2, 3, 14), 'key not exist'))

# 结构化的一种表示方法(其实就是看着顺眼而已)
# student1 = {  # 虽然明显不对但是 很奇怪,语法不会报错
#     {
#         'name': 'gakki',
#         'age': '23'
#     },
#     {
#         'name': 'Gal',
#         'age': '30'
#     },
# }

student2 = [
    {
        'name': 'gakki',
        'age': '23'
    },
    {
        'name': 'Gal',
        'age': '30'
    }
]
# 这种表达方式很像类
student3 = {}
student3['name'] = 'gakki'
student3['age'] = 23


