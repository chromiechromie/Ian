import unittest

def format_name(f_name, l_name, m_name=''):
    if m_name:
        t_name = f_name+' '+m_name+' '+l_name
    else:
        t_name = f_name+ ' '+l_name

    return t_name


print(format_name(f_name='科洛蒂娅', l_name='奥赛雷丝', m_name='冯'))


class NameTestCase(unittest.TestCase):

    def test_name(self):
        test_value = format_name(f_name='科洛蒂娅', l_name='奥赛雷丝', m_name='冯')
        self.assertEqual(test_value, '科洛蒂娅 冯 奥赛 雷丝')


unittest.main()


class AnonymousSurvey():

    """
        测试类,练习测试方法的使用
    """

    def __init__(self, requirement):

        self.requirement = requirement
        self.respone = []

    def show_it(self):
        self.requirement
        print('The respone of this requirement: ', self.requirement, 'is ', self.respone)




