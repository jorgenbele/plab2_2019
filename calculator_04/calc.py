#!/usr/bin/env python
# Author: Jørgen Bele Reinfjell
# Date: 18.09.2019 [dd.mm.yyyy]
# File: calc.py
# Description:
#   Python code for assignment 2 of Plab2 2019

from sys import stdin
from numbers import Number as Num

import numpy as np


def first(lst):
    """Helper function that returns the first element in l"""
    for element in lst:
        return element


def is_float(str_):
    try:
        float(str_)
        return True
    except ValueError:
        return False


def words(str_: str):
    for s in str_.split():
        yield s


def upper(lst):
    return map(lambda x: x.upper(), lst)


class Container:
    "Container"

    def __init__(self, items=None):
        if items:
            self.items = items
        else:
            self.items = []

    def size(self):
        "size"
        return len(self.items)

    def is_empty(self):
        "is_empty"
        return self.size() == 0

    def push(self, item):
        "push"
        self.items.append(item)

    def pop(self):
        "pop"
        raise NotImplementedError

    def peek(self):
        "peek"
        raise NotImplementedError


class Queue(Container):
    def __init__(self, items=None):
        super().__init__(items=items)

    def pop(self):
        "pop"
        assert not self.is_empty()
        return self.items.pop(0)

    def peek(self):
        "peek"
        assert not self.is_empty()
        return self.items[0]


class Stack(Container):
    "stack"

    def __init__(self, items=None):
        super().__init__(items=items)

    def pop(self):
        "pop"
        assert not self.is_empty()
        return self.items.pop(self.size() - 1)

    def peek(self):
        "peek"
        assert not self.is_empty()
        return self.items[self.size() - 1]


class Function:
    "function"

    def __init__(self, func):
        self.func = func

    def __call__(self, element: Num):
        "__call__"
        return self.func(element)

    def __name__(self):
        "__name__"
        return 'Function({})'.format(self.func.__name__)

    def __repr__(self):
        "__repr__"
        return 'Function({})'.format(self.func.__name__)


class Operator:
    "operator"

    def __init__(self, operation, strength=None):
        self.operation = operation
        self.strength = strength

    def __call__(self, *args, **kwargs):
        "__call__"
        return self.operation(*args, **kwargs)

    def __name__(self):
        "__name__"
        return 'Operator({})'.format(self.operation.__name__)

    def __repr__(self):
        "__repr__"
        return 'Operator({})'.format(self.operation.__name__)


class Calculator:
    "calculator"

    def __init__(self):
        self.functions = {
            'exp': Function(np.exp),
            'log': Function(np.log),
            'sin': Function(np.sin),
            'cos': Function(np.cos),
            'sqrt': Function(np.sqrt),
        }

        self.operators = {
            '+': Operator(np.add, 0),
            '*': Operator(np.multiply, 1),
            '/': Operator(np.divide, 1),
            '-': Operator(np.subtract, 0),
        }

    def eval(self, lst: list):
        "eval"
        return self.eval_rpn(self.shunting_yard(lst))

    def eval_rpn(self, lst: list):
        "eval_rpn"
        s = Stack()
        for l in lst:
            if isinstance(l, Num):
                s.push(l)
            elif isinstance(l, Function):
                s.push(l(s.pop()))
            elif isinstance(l, Operator):
                s.push(l(*reversed([s.pop(), s.pop()])))
        return s.pop()

    def shunting_yard(self, lst: list):
        "shunting yard"
        oq = Queue()
        os = Stack()
        for l in lst:
            if isinstance(l, Num):
                oq.push(l)
            elif isinstance(l, Function):
                os.push(l)
            elif isinstance(l, str) and l == '(':
                os.push('(')
            elif isinstance(l, str) and l == ')':
                while os.peek() != '(':
                    oq.push(os.pop())
                os.pop()

            elif isinstance(l, Operator):
                while not os.is_empty() \
                        and (isinstance(os.peek(), Function) or isinstance(os.peek(), Operator)) \
                        and os.peek().strength >= l.strength:
                    oq.push(os.pop())
                os.push(l)

        while not os.is_empty():
            oq.push(os.pop())

        return oq.items

    def tokens(self, str_: str):
        "tokens"
        s = str_.replace('(', ' ( ')
        s = s.replace(')', ' ) ')

        for w in upper(words(s)):
            if is_float(w):
                yield float(w)
            elif w in self.operators.keys():
                yield self.operators[w]
            elif w in self.functions.keys():
                yield self.functions[w]
            else:
                yield w


c = Calculator()


def lines():
    while True:
        yield stdin.readline().strip()


if __name__ == '__main__':
    list(map(lambda x: print('==>', c.eval(c.tokens(x)), flush=True), lines()))
