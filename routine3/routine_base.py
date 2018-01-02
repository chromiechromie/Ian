def p(self):
    print(self, '类型为: ', type(self))


def pp(*self):  # 接收多个参数
    print(self, '类型为: ', type(self))


class Person():

    """
    base person类,用于测试

    """

    # 她们的前缀为self
    def __init__(self, name, age):  # 创建新实例时,Python都会自动运行她
        self.name = name  # 获取存储在形参name中的值,并将其存储到变量name中,然后,改变量,被关联到当前创建的实例
        self.age = age
        self.id = 0
    """
    以self为前缀的变量都可供类中所有方法使用
    像这样,可以通过实例去方位的变量称为属性
    注意,type(self.name)好像是元组
    """

    def base_func(self):
        pp(self)

    '''
    self 当Python调用init来创建person实例时,将自动传入实参self.
    每个与类相关联的的方法调用,都会自动传递实参self,
    她是一个纸箱实例本身的引用,让实例能够访问类中的属性和方法
    
    '''
    def update_id(self, id):
        self.id = id

    def update_age(self, age):
        if age < self.age:
            print('你他妈在逆生长吗')
        else:self.age = age



