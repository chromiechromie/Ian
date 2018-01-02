import routine_base as rb  # 变红无所谓 给函数指定别名

d = {1: 'gakki', 2: 'Arturia', 3: 'Gal'}
o_list = ['char', 'text', 'boolean', 'integer', 'float', 'date', 'binary']

while 'char' in o_list:
    o_list.remove('char')
rb.p(o_list)

rb.pp(o_list, o_list)

# 函数执行过程:
gakki = rb.Person('Gakki', 23)

"""
1.使用实参'Gakki' 和 23  调用Person 中的__init__()方法.
2.__init__()创建一个表示特定的人的实例,并使用我们提供的值'Gakki',23 来设置属性name,age
3.__init__()没有显式地包含return语句,但Python自动返回一个表示Person的实例.
4.这个实例会被存在gakki这个variable中.
FYI : 通常首字母大写的是类,小写的是根据类创建的实例
"""
rb.pp(gakki.name)  # 这里,我们引用的属性,是self.name
gakki.update_id(2)

rb.pp(gakki.id)
gakki.update_age(24)
rb.pp(gakki.age)

# 继承


class Valhalla():

    def __init__(self):
        self.date = ''
        self.master = ''


class Person_extend(rb.Person):
    """
    0.需要在括号内(上面)指定父类的名称 eg:(rb.Person)
    1.继承父类 让Python调用父类的__init__方法
    2.父类,又被称作超类:superclass
    """

    def __init__(self, name, age, date, master, treasure):  # 可以这样搞
        super().__init__(name, age)
        self.treasure = treasure
        self.valhalla = Valhalla()  # 注意Valhalla的位置,要在子类的上面
        self.valhalla.master = master
        self.valhalla.date = date

    def update_treasure(self, treasure):
        self.treasure = treasure

    def update_age(self, age):
        print('无意义')


arturia = Person_extend(name='Arturia', age=500, master='卫宫切嗣', date='中世纪', treasure='Excalibur')
arturia.update_treasure('Excalibur')
rb.pp(arturia.name, arturia.treasure)
rb.pp(arturia.valhalla.master)





