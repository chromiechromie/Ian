import datetime
import time

# datetime.date 年月日构成的日期 相当于日历
# datetime.time 时分秒
# datetime.datetime 时间+日期
# datetime.timedelta 时间间隔对象.一个时间点datetime + timedelta可以的到一个新的时间点(datetime)

# 获取当天日期
today = datetime.date.today()


def p(args):
    print(args, '类型为 ', type(args))


# 获取今天
p(today)
'''
    创建datetime.date类型,接收参数如()内所示
'''

p(datetime.date(2018, 9, 2))  # p(datetime.date(2018,29,2)) 这样是不行滴
'''
    将datetime.date类型转为 str
'''

p(today.strftime('%Y-%m-%d %H:%M:%S'))
'''
    str 转datetime
'''

p(datetime.datetime.strptime(today.strftime('%Y-%m-%d %H:%M:%S'),
                             '%Y-%m-%d %H:%M:%S'))  # 格式是这样滴strptime(str,(format))

# py3.6不认同这种01的写法
# p(datetime.time(21,01,02))
# p(datetime.time(21,01,02)strftime('%Y-%m-%d %H:%M:%S'))

# class 'datetime.time'> 其余与datetime.date相同
p(datetime.time(21, 1, 2))
p(datetime.time(21, 1, 2).strftime('%Y-%m-%d %H:%M:%S'))
'''
    datetime.date.timple() 转成时间戳格式
'''

p(today.timetuple())

p(time.mktime(today.timetuple()))

'''
    datetime 替换年月日
'''
date = datetime.datetime(2018, 2, 26)
date = date.replace(year=2020)
date = date.replace(month=3)
p(date)

'''
    将时间戳转化为date对象
'''
# 时间戳
date = time.mktime(date.timetuple())
t1_date = date
t1_date = datetime.date.fromtimestamp(t1_date)
# 是datetime.datetime 还是datetime.date 类型取决于datetime.?
date = datetime.datetime.fromtimestamp(date)
p(t1_date)
p(date)
'''
    time 类型
'''

'''
    创建一个time对象
'''

t_time = datetime.time(20, 19, 29)
p(t_time)
'''
    格式化输出,返回
    time ==> str
'''
t2_time = t_time.strftime('%Y-%m-%d %H:%M:%S')
p(t2_time)

'''
    time替换
'''
# 注意t_time必须是datetime.x类型
t3_time = t_time.replace(minute=24)
p(t3_time)

'''
    datetime.timedelta
    主要用于时间的加减法
'''
t4_time = datetime.datetime(2018, 2, 26, 20, 27, 28)
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
next_week = t4_time + datetime.timedelta(days=7)
p(yesterday)
p(next_week)
