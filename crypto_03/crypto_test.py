import unittest

from crypto import *

def check_cipher(test_instance, inp, *cipher_args, **cipher_kwargs):
    test_instance.assertEqual( \
        do_cipher(test_instance, inp, *cipher_args, **cipher_kwargs), \
        inp
    )


def do_cipher(test_instance, inp, *cipher_args, **cipher_kwargs):
    return test_instance.cipher.decode( \
        test_instance.cipher.encode(inp, *cipher_args, **cipher_kwargs), \
        *cipher_args, **cipher_kwargs)


class TestCaesarCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = Caesar()


    def test_empty(self):
        check_cipher(self, '', 1)


    def test_simple_0(self):
        check_cipher(self, 'THIS IS A TEST', 0)


    def test_simple_1(self):
        check_cipher(self, 'THIS IS A TEST', 1)


    def test_simple_2(self):
        check_cipher(self, 'THIS IS A TEST', 2)


    def test_simple_26(self):
        check_cipher(self, 'THIS IS A TEST', 26)


class TestMultiplicative(unittest.TestCase):
    def setUp(self):
        self.cipher = Multiplicative()


    def test_empty(self):
        check_cipher(self, '', 1)


    def test_simple_0(self):
        do_cipher(self, 'THIS IS A TEST', 0) == '              '


    def test_simple_1(self):
        check_cipher(self, 'THIS IS A TEST', 1)


    def test_simple_2(self):
        check_cipher(self, 'THIS IS A TEST', 2)


    def test_simple_26(self):
        check_cipher(self, 'THIS IS A TEST', 26)


class TestAffine(unittest.TestCase):
    def setUp(self):
        self.cipher = Affine()


    def test_empty_0_1(self):
        check_cipher(self, '', (0, 1))


    def test_simple_2_3(self):
        do_cipher(self, 'THIS IS A TEST', (2, 3)) == '              '


    def test_simple_3_4(self):
        check_cipher(self, 'THIS IS A TEST', (3, 4))


    def test_simple_2_2(self):
        check_cipher(self, 'THIS IS A TEST', (2, 2))


    def test_simple_4_3(self):
        check_cipher(self, 'THIS IS A TEST', (4, 3))



class TestRSA(unittest.TestCase):
    def setUp(self):
        self.cipher = RSA()
        self.bits = 100
        #self.privk, self.pubk = self.cipher.generate_keys(bits=self.bits)
        # 100 bits RSA keys
        self.privk = (3604617187326575099830723150055960731708890534417407738144869, 1670829181481326629478187490659425613113621340486702173415875)
        self.pubk = (3604617187326575099830723150055960731708890534417407738144869, 1708897424260872604511253961052260057236751681005790699060459)


    def test_empty(self):
        inp = ''
        e = self.cipher.encode(inp, self.pubk, bits=self.bits)
        d = self.cipher.decode(e, self.privk, bits=self.bits)
        self.assertEqual(d, inp)


    def test_simple_1(self):
        inp = 'KODE'
        e = self.cipher.encode(inp, self.pubk, bits=self.bits)
        d = self.cipher.decode(e, self.privk, bits=self.bits)
        self.assertEqual(d, inp)


    def test_simple_2(self):
        inp = 'THIALSDLJ lkjasdf poUIASD 123 |09802 39812'
        e = self.cipher.encode(inp, self.pubk, bits=self.bits)
        d = self.cipher.decode(e, self.privk, bits=self.bits)
        self.assertEqual(d, inp)


class TestHacker(unittest.TestCase):
    def setUp(self):
        with open('english_words.txt') as f:
            self.wordlist = set(map(lambda s: s.strip(), f.readlines()))


    def test_caesar_zigzagged_24(self):
        c = Caesar()
        inp, key = 'zigzagged', 24
        e = c.encode(inp, key)
        h = Hacker(c)
        h.set_wordlist(self.wordlist)
        self.assertEqual(h.operate_cipher(e), key)


    def test_caesar_abc_1(self):
        c = Caesar()
        inp, key = 'abc', 1
        e = c.encode(inp, key)
        h = Hacker(c)
        h.set_wordlist(self.wordlist)
        self.assertEqual(h.operate_cipher(e), key)


    def test_multiplicative_zigzagged_24(self):
        c = Multiplicative()
        inp, key = 'zigzagged', 24
        e = c.encode(inp, key)
        h = Hacker(c)
        h.set_wordlist(self.wordlist)
        self.assertEqual(h.operate_cipher(e), key)


    def test_multiplicative_deprogramming_11(self):
        c = Multiplicative()
        inp, key = 'deprogramming', 11
        e = c.encode(inp, key)
        h = Hacker(c)
        h.set_wordlist(self.wordlist)
        self.assertEqual(h.operate_cipher(e), key)


    def test_affine_deprogramming_11(self):
        c = Affine()
        inp, key = 'deprogramming', (1, 11)
        e = c.encode(inp, key)
        h = Hacker(c)
        h.set_wordlist(self.wordlist)
        self.assertEqual(h.operate_cipher(e), key)

if __name__ == '__main__':
    unittest.main()
