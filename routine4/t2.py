import matplotlib.pyplot as plt

"""
1.创建一个包含x值得列表
2.创建y值.
3.axis接受4个值:x,y 的最小值,最大值
4.
"""
# x_value = list(range(1, 1000))
# y_value = [x**2 for x in x_value]
#
# # s:点的大小 edgecolors 点轮廓
# plt.scatter(x_value, y_value, s=10, edgecolors='none', c='pink')
# plt.axis([0, 100, 0, 10000])
# plt.show()
# # 颜色映射 (颜色渐变)cmap=plt.cm.Blues
# x_value2 = list(range(1, 100))
# y_value2 = [x*2 for x in x_value2]
# plt.scatter(x_value2, y_value2, s=20, edgecolors='none', c=y_value2,
#             cmap=plt.cm.Blues)
# plt.show()


from random import choice


class RandomWalk():
    """
    生成随机漫步的类, 她接收三个属性
    1.存储随机漫步次数的变量
    2.2个list 存储x,y轴坐标

    """
    def __init__(self, num_points=5000):
        """
        随机漫步的的属性的初始化
        :param num_points:默认的点数
        """
        self.num_points = num_points
        """
        所有随机漫步都是与(0,0)
        """
        self.x_values =[0]
        self.y_values =[0]

    def fill_walk(self):

        while len(self.x_values) < self.num_points:
            x_direction = choice([1, -1])  # 表示要么向左走 ,要么向右走
            x_distance = choice([0, 1, 2, 3, 4]) # 表示走多远,包括零表示可以沿着y轴行进
            x_step = x_direction*x_distance

            y_direction = choice([1, -1])  # 表示要么向左走 ,要么向右走
            y_distance = choice([0, 1, 2, 3, 4]) # 表示走多远,包括零表示可以沿着y轴行进
            y_step = y_direction*y_distance

            if x_step == 0 and y_step == 0:
                continue

            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step

            self.x_values.append(next_x)
            self.y_values.append(next_y)


# rw = RandomWalk()
# rw.fill_walk()
# plt.scatter(rw.x_values, rw.y_values, s=15)
# plt.show()


# while 1 == 1:
#     rw = RandomWalk()
#     rw.fill_walk()
#     plt.scatter(rw.x_values, rw.y_values, s=10)
#     plt.show()
#
#     keep = input("try age?(y/n) ")
#     if keep == 'n':
#         break

while 1 == 1:
    rw = RandomWalk()
    rw2 = RandomWalk()
    rw3 = RandomWalk()
    rw.fill_walk()
    rw2.fill_walk()
    rw3.fill_walk()
    point_numbers = list(range(rw.num_points))
    plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Reds,
                edgecolors='none', s=15)
    plt.scatter(rw2.x_values, rw2.y_values, c=point_numbers, cmap=plt.cm.Blues,
                edgecolors='none', s=15)
    plt.scatter(rw3.x_values, rw3.y_values, c=point_numbers, cmap=plt.cm.Greens,
                edgecolors='none', s=15)
    # 突出起点和终点
    plt.scatter(0, 0, c='black', edgecolors='none', s=50)
    plt.scatter(rw.x_values[-1], rw.y_values[-1], c='yellow', edgecolors='none', s=50)
    plt.scatter(rw2.x_values[-1], rw2.y_values[-1], c='yellow', edgecolors='none', s=50)
    plt.scatter(rw3.x_values[-1], rw3.y_values[-1], c='yellow', edgecolors='none', s=50)
    # 隐藏坐标轴
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)
    # 调整窗口大小
    plt.figure(dpi=128, figsize=(10, 6))  # ????????这啥
    plt.show()

# Python 模拟栈


class Stack:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()   # 返回栈顶元素,并删除它

    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]  # 返回栈顶元素

    def size(self):
        return len(self.items)


s = Stack
print(s.isEmpty())
s.push(4)
s.push('gakki')
print(s.peek())




















