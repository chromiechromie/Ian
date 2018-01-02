myData = {1: 'Aragaki Yui', 2: 'GAKKI', 3: 'Nagasawa Masami'}


def xx():
    print('----------分割线ヾ(◍°∇°◍)ﾉﾞ分割线----------')


__author__ = 'Ian'

import sys


def test():
    args = sys.argv
    if len(args) == 1:
        print('h1', args)
    elif len(args) == 2:
        print('h2')
    else:
        print('????')


if __name__ == '__main__':
    test()
