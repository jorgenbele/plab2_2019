#!/usr/bin/env python
# Author: Jørgen Bele Reinfjell
# Date: 14.09.2019 [dd.mm.yyyy]
# File: crypto.py
# Description:
#   Python code for assignment 3 of Plab2 2019
"""
Program implementing various cyphers.
"""

from random import randint
import itertools
import math

# Not included in this project
from crypto_utils import modular_inverse, generate_random_prime


def words(text: str):
    """Generator that yields all words in text"""
    for word in text.split(' '):
        yield word


def primes(bits=1024):
    """Helper function that returns a prime generator
    with a set number of bits"""
    while True:
        yield generate_random_prime(bits)


def first(lst):
    """Helper function that returns the first element in l"""
    for element in lst:
        return element


def randints(start=0, end=1024, limit=None):
    """Generator that yields random ints in a given range
    will stop after 'limit' ints if bool(limit) == true."""
    while True:
        if limit:
            limit = limit - 1
            if limit < 1:
                return
        yield randint(start, end - 1)


def repeatedstr(str_):
    """Generator that repeates the string s forever"""
    saved = [s for s in str_]

    i = 0
    while True:
        yield saved[i]
        i = (i + 1) % len(saved)


def cipher_(func, chr_, alphabet):
    """Helper function for transformation functions"""
    return alphabet[func(ord(chr_) - ord(alphabet[0])) % len(alphabet)]


class Cipher:
    """Cipher >> Cypher"""

    def __init__(self):
        self.alphabet = [chr(i) for i in range(32, 127)]  # [#32, ..., #126]

        # A-Z
        # self.alphabet = [
        #    chr(i) for i in range(ord("A"), ord("Z") + 1)
        # ]  # [#32, ..., #126]

    def encode(self, input_str: str, key):
        """Encode string input_str"""

    def decode(self, enc_str: str, key):
        """Decode an encoded string enc_str"""

    def verify(self, input_str: str, key):
        """Verify that the encoding-decoding pair works correctly"""
        assert self.decode(self.encode(input_str, key), key) == input_str

    def generate_keys(self):
        """Generates the keys distributed to both sender and reciever
           Returns: (sender_key, reciever_key)"""

    def possible_keys(self):
        """Generator returning all possible keys"""


class Caesar(Cipher):
    """Caesar chipher impl."""

    def encode(self, input_str: str, key: int):
        """Encode string input_str"""
        return "".join(
            map(lambda x: cipher_(lambda t: t + key, x, self.alphabet), input_str)
        )

    def decode(self, enc_str: str, key: int):
        """Decode an encoded string enc_str"""
        return self.encode(enc_str, -key)

    def verify(self, input_str: str, key: int):
        """Verify that the encoding-decoding pair works correctly"""
        assert self.decode(self.encode(input_str, key), key) == input_str

    def generate_keys(self):
        """Generates the keys distributed to both sender and reciever"""
        return [randint(0, len(self.alphabet) - 1)] * 2

    def possible_keys(self):
        """Return all possible keys"""
        return itertools.takewhile(lambda x: x < len(self.alphabet), itertools.count())


class Multiplicative(Cipher):
    """Multiplicative chipher impl."""

    def encode(self, input_str: str, key: int):
        """Encode string input_str"""
        return "".join(
            map(lambda x: cipher_(lambda t: t * key, x, self.alphabet), input_str)
        )

    def decode(self, enc_str: str, key: int):
        """Decode an encoded string enc_str"""
        inv = modular_inverse(key, len(self.alphabet))
        return "".join(
            map(lambda x: cipher_(lambda t: t * inv, x, self.alphabet), enc_str)
        )

    def generate_keys(self):
        """Generates the keys distributed to both sender and reciever"""
        return [
            first(
                filter(
                    lambda x: math.gcd(x, len(self.alphabet)) == 1,
                    randints(end=len(self.alphabet)),
                )
            )
        ] * 2

    def possible_keys(self):
        """Return all possible keys: gcd(key, len(alphabet) != 1"""
        return filter(lambda x: math.gcd(x, len(self.alphabet)) == 1,
                      itertools.takewhile(lambda x: x < len(self.alphabet), itertools.count()))


class Affine(Cipher):
    """Affine chipher impl."""

    def __init__(self):
        super().__init__()
        self.caesar = Caesar()
        self.multiplicative = Multiplicative()

    def encode(self, input_str: str, key: (int, int)):
        return self.caesar.encode(self.multiplicative.encode(input_str, key[0]), key[1])

    def decode(self, input_str: str, key: (int, int)):
        return self.multiplicative.decode(self.caesar.decode(input_str, key[1]), key[0])

    def generate_keys(self):
        """Generates the keys distributed to both sender and reciever"""
        return [
            (
                first(self.multiplicative.generate_keys()),
                first(self.caesar.generate_keys()),
            )
        ] * 2

    def possible_keys(self):
        """Return all possible keys: gcd(key, len(alphabet) != 1"""
        return itertools.product(self.multiplicative.possible_keys(), self.caesar.possible_keys())


class Unbreakable(Cipher):
    """Unbreakable chipher impl."""

    def encode(self, input_str: str, key: int):
        """Encode string input_str"""
        return "".join(
            map(
                lambda x: cipher_(
                    lambda t: t + ord(x[1]), x[0], self.alphabet),
                zip(input_str, repeatedstr(key)),
            )
        )

    def decode(self, input_str: str, key: str):
        """Decode """
        return "".join(
            map(
                lambda x: cipher_(
                    lambda t: t - ord(x[1]), x[0], self.alphabet),
                zip(input_str, repeatedstr(key)),
            )
        )

    def generate_keys(self, limit=10):
        """Generates the keys distributed to both sender and reciever"""
        return [
            "".join(
                map(
                    lambda x: cipher_(lambda t: t, x, self.alphabet),
                    map(chr, randints(start=0, end=len(self.alphabet), limit=limit)),
                )
            )
        ] * 2

    def possible_keys(self):
        """All possible keys: the language generated by self.alphabet"""
        # This is not feasable


def text_to_int_blocks(text, block_size=1024):
    data = text.encode('utf_8')
    return map(lambda c: int.from_bytes(data[c:min(c+block_size, len(data))], 'big', signed=False),
               range(0, len(data), block_size))


def int_blocks_to_text(blocks, block_size=1024):
    return ''.join(map(lambda x: (x.to_bytes(2*block_size, byteorder='big', signed=False))
                       .decode(encoding='UTF-8', errors='ignore')
                       .lstrip('\0'), blocks))


class RSA(Cipher):
    """RSA impl."""

    def encode(self, input_str: str, key: int, bits=1024):
        """Encode string input_str"""
        block_size = bits//4
        n, e = key
        return list(
            map(lambda t: pow(t, e, n), text_to_int_blocks(input_str, block_size))
        )

    def decode(self, blocks: list, key: str, bits=1024):
        """Decode """
        block_size = bits//4
        n, d = key
        return int_blocks_to_text(map(lambda c: pow(c, d, n), blocks), block_size)

    def generate_keys(self, bits=1024):
        """Generates the keys distributed to both sender and reciever"""
        g = primes(bits=bits)
        p = first(g)
        q = first(filter(lambda x: x != p, g))

        n = p * q
        oe = (p - 1) * (q - 1)
        d = False
        while not d:
            e = randint(3, oe - 1)
            d = modular_inverse(e, oe)

        return ((n, d), (n, e))  # reciever (private), sender (public)


class Person:
    """Person"""

    def __init__(self, key=None, cipher=None):
        self.key = key
        self.cipher = cipher

    def set_key(self, key):
        """Set key"""
        self.key = key

    def get_key(self):
        """Get key"""
        return self.key

    def operate_cipher(self, inp=None):
        pass


class Sender(Person):
    """Sender"""

    def operate_cipher(self, inp=None):
        return self.cipher.encode(inp, self.key)


class Reciever(Person):
    """Reciever"""

    def operate_cipher(self, inp=None):
        return self.cipher.decode(inp, self.key)


class Hacker(Person):
    """Hacker"""

    def __init__(self, cipher):
        super().__init__(cipher=cipher)
        self.wordlist = None

    def set_wordlist(self, wordlist):
        self.wordlist = wordlist

    def operate_cipher(self, inp=None):
        """Check all possible keys one by one and return the first key that
        results in a string only consisting of words from self.wordlist"""
        return first(
            filter(lambda key: is_lexical_match(self.cipher.decode(inp, key), self.wordlist),
                   self.cipher.possible_keys())
        )


def is_lexical_match(inp: str, wordlist: set):
    """Check if input string consists only of complete words"""
    # NOTE: This only works on letters, not punctuation etc.
    return all([(w in wordlist) for w in words(inp)])
