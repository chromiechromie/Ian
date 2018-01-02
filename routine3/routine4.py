# 关键字实参
def f1(a, b):
    print(a, b)

f1(b=2, a=1)

# 函数默认值
def f2(a, b, c =233):
    print(a, b, c)

f2(1,2)
f2(b=213, a='asdf', c='asdf')
a = True
b = False
if not False and True:
    print("it is True")
else:
    print("False")

def get_formatted_name(f_name, l_name, m_name =''):
    if m_name:
        full_name = f_name.title() +' '+ m_name +' '+l_name
    else:
        full_name = f_name.title() + ' ' + l_name
    return full_name
print(get_formatted_name('科洛蒂娅', '奥赛雷丝','·冯·'))
print(get_formatted_name('科洛蒂娅', '奥赛雷丝'))

def build_person(id, name, age=''):
    person = {id:name}
    if age:
        person['age'] = age
    else:
        print(type(age))
    return person

def p(xx):
    print(xx, '类型为: ', type(xx))

p(build_person(1,'gakki'))
unprinted_designs = ['a', 'b', 'c']
completed_models = []
while unprinted_designs:
    current_designs = unprinted_designs.pop()
    p(current_designs)
    completed_models.append(current_designs)
    p(completed_models)
    p(current_designs)

bb = "x"
cc = "xcxc"
aa = lambda aa: bb and cc or 0
print(aa(11))
x = 2
a = lambda x : x**2
p(a(2))
nums = range(2,40)
for i in range(2,8):
    nums = filter(lambda x: x == i or x % i, nums)
p(nums)

xx = lambda self : self and self**2 and self+2 or 'hello world'

p(xx(3))


def copy(self, default=None):
    default = dict(default or {})
    p(default)
copy(11)

a = None
p(a)

if True and False or True and not True or not False and None:
    p("it is True")
else:
    p('it is False')

# 删除id 为偶数的dict中的元素
i = 0
dict ={}
while i < 10:
    i += 1
    dict[i] = "Gakki"+str(i)

# for i in range(0,10,2):
#     print(i)
#     del dict[i]
# print(dict)
dict1={}
if not dict1: #为空则赋值
    dict1={1:'Gakki'}
p(dict1)

# 在列表中移动元素
print(myData)