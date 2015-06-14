from collections import Counter


class Stack:
    def __init__(self, iterable):
        self.ls = list(iterable)

    def push(self, key):
        self.ls.append(key)

    def pop(self, key=None):
        return self.ls.pop() if key is None else self.ls.pop(key)

    @property
    def top(self):
        '''
            Top of the stack.
            stack[-1]
        '''
        try:
            return self.ls[-1]
        except IndexError:
            return None

    @property
    def bottom(self):
        try:
            return self.ls[0]
        except IndexError:
            return None


class IndentStack(Stack):
    def push(self, key) -> str:
        ret = '{}{{'.format(self.top)
        super().push(key)
        return ret

    def pop(self) -> str:
        self.ls.pop()
        ret = '{}}}'.format(self.top)
        return ret

    def __getitem__(self, index):
        return self.ls[index]


class LineCounter(Counter):
    def push(self, key):
        '''
        Increase key by one.
        '''
        self[key] += 1
