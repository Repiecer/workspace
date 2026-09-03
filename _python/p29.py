class Stack():
    def __init__(self):
        self._items = []
    def push(self, item) -> None:
        self._items.append(item)
    def pop(self):
        return self._items.pop()
    def is_empty(self):
        return not bool(self._items)
    def peek(self):
        return self._items[-1]

def cal_classify(subj:str):
    syms = Stack()
    for sym in subj:
        if sym == '(':
            syms.push(sym)
        else:
            if syms.is_empty():
                return False
            else:
                syms.pop()
    return syms.is_empty()
