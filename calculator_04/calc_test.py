#!/usr/bin/env python

import unittest

from calc import *

class TestStack(unittest.TestCase):
    def test_empty(self):
        s = Stack()
        self.assertEqual(s.size(), 0)
        self.assertTrue(s.is_empty())

    def test_pop1(self):
        s = Stack(items=[1])
        self.assertEqual(s.size(), 1)
        self.assertFalse(s.is_empty())
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())

    def test_push_pop(self):
        s = Stack(items=[1, 2, 3])
        self.assertEqual(s.size(), 3)
        self.assertFalse(s.is_empty())
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.items, [1, 2])
        s.push(3)
        self.assertEqual(s.items, [1, 2, 3])

class TestQueue(unittest.TestCase):
    def test_empty(self):
        s = Queue()
        self.assertEqual(s.size(), 0)
        self.assertTrue(s.is_empty())

    def test_pop1(self):
        s = Stack(items=[1])
        self.assertEqual(s.size(), 1)
        self.assertFalse(s.is_empty())
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())

    def test_push_pop(self):
        s = Stack(items=[1, 2, 3])
        self.assertEqual(s.size(), 3)
        self.assertFalse(s.is_empty())
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.items, [1, 2])
        s.push(4)
        self.assertEqual(s.items, [1, 2, 4])



class TestFunction(unittest.TestCase):
    def test_exp(self):
        import numpy as np
        exp = Function(np.exp)
        self.assertEqual(exp(10), 22026.465794806718)

class TestOperator(unittest.TestCase):
    def test_add(self):
        import numpy as np
        add = Operator(np.add)
        self.assertEqual(add(10, 20), 30)

class TestCalculator(unittest.TestCase):
    def test_exp_mult_add(self):
        import numpy as np
        c = Calculator()
        exp, add, mult = (c.functions['exp'], c.operators['+'], c.operators['*'])
        self.assertEqual(exp(add(1, mult(2, 3))), 1096.6331584284585)

    def test_eval_rpn_exp_mult_add(self):
        import numpy as np
        c = Calculator()
        exp, add, mult = (c.functions['exp'], c.operators['+'], c.operators['*'])
        inp = [3, 2, mult, 1, add, exp]
        self.assertEqual(exp(add(1, mult(2, 3))), c.eval_rpn(inp))

    def test_shunting_yard(self):
        import numpy as np
        c = Calculator()
        exp, add, mult = (c.functions['exp'], c.operators['+'], c.operators['*'])
        inp = [exp, '(', 1, add, 2, mult, 3, ')']
        self.assertEqual(c.shunting_yard(inp), [1, 2, 3, mult, add, exp])

    def test_eval_shunting_yard(self):
        import numpy as np
        c = Calculator()
        exp, add, mult = (c.functions['exp'], c.operators['+'], c.operators['*'])
        inp = [exp, '(', 1, add, 2, mult, 3, ')']
        self.assertEqual(np.exp(1+2*3), c.eval(inp))

    def test_parse(self):
       c = Calculator()
       exp, add, mult = (c.functions['exp'], c.operators['+'], c.operators['*'])
       tokens = list(c.tokens('exp(1 + 2 * 3)'))
       self.assertEqual(tokens, [exp, '(', 1, add, 2, mult, 3, ')'])
       self.assertEqual(np.exp(1+2*3), c.eval(tokens)) #.shunting_yard(tokens))

if __name__ == '__main__':
    unittest.main()
