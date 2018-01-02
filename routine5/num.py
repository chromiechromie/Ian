import random

random.random()
print(random.random())
print(random.choice([1, 2, 3, 4]))
x = 123
c = [3]
c = [3]
myData=[1,2,3,4,5,6,3]
if not c:
    print('常用作非空判断')

a = c in c
#不可以是 可迭代对象 in 可迭代对象>>
a1 = 3 in c

a2 = c not in c

a4 = 3 not in c

a5 = 1 < 2 < 3
# a5 效率高于 a6
a6 = 1 < 2 and 2< 3
#
a7 = 1 == 2 < 3

a8 = False < 3


if 1 == 1:
    print("我是占位符")