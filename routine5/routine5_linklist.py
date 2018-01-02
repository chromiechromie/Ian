
class Node(object):
    def __init__(self, val, p=0):
        self.data = val
        self.next = p


class LinkList(object):
    def __init__(self):
        self.head = 0

    def __getitem__(self, key):  # 喵喵喵???

        if self.is_empty():
            print('linklist is empty')

        elif key <0 or key > self.getlength():
            print('the given key is error')

    def is_empty(self):
        if self.getlength() == 0:
            return True
        else:
            return False

    def getlength(self):
        p = self.head
        length = 0
        while p != 0:
            length += 1
            p = p.next

        return length