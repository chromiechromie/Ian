# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

input_values = []
squares = []
for i in range(1, 9):
    input_values.append(i)

for i in range(1, 16, 2):
    squares.append(i)


def p(*k):
    print(k, type(k))



p(squares)


plt.scatter(2, 323, s=200)
"""

不要写中文,会出现乱码

"""
plt.title('TITLE', fontsize=24)
plt.xlabel('x', fontsize=24)
plt.ylabel('y', fontsize=24)
# plt.show()

"""
绘制一系列点
"""

x_value = list(range(1, 10010))
y_value = [x**3 for x in x_value]

plt.scatter(x_value, y_value, s=40)
plt.axis([0, 1100, 0, 1100000])
# plt.show()

x_value = list(range(1, 99))
y_value = [x**1 for x in x_value]
plt.scatter(x_value, y_value)
# 设置每个坐标轴的取值范围
plt.axis([0, 100, 0, 1000])
plt.show()





