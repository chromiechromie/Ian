# time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# print(time)
myData = {1: 'Aragaki Yui', 2: 'GAKKI', 3: 'Nagasawa Masami'}


# import datetime
# now_time = datetime.datetime.now()


def pr_time():
    import time
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(time)


if 1 == 1:
    print('xx')


def xx():
    print('----------分割线ヾ(◍°∇°◍)ﾉﾞ分割线----------')


def log(text):
    def decorator1(func):  # 接收参数为函数
        def decorator2(*args, **kw):  # 万能参数
            print(' %s %s(): '
                  % (text, func.__name__))  # 输出传入函数的名字
            return func(*args, **kw)  # 执行被装饰的函数

        return decorator2

    return decorator1


@log('execute')
def now():
    pr_time()


now()

xx()
# 偏函数 Partial function


print(int('13344'))  # 强转为int
print(int('13344', base=16))  # 将16位转为10进制
print(int('13344', base=10))
# print(int(myData[2])) invalid literal

import functools

int2 = functools.partial(int, base=2)  # 函数参数过多,functools.partial 可以创建一个新的函数,固定住一部分参数

print(int2('10001'))

