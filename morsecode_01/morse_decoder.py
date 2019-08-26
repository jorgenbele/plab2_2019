#!/usr/bin/env python
# Author: Jørgen Bele Reinfjell
# Date: 26.08.2019 [dd.mm.yyyy]
# File: morse_decoder.py
# Description:
#   Python code for assignment 1 of Plab2 2019

import serial

# Change this to your device.
SERIAL_DEV_PATH = '/dev/ttyUSB0'

MORSE_MAPPING = {
    '01':     'a', '1000':   'b', '1010':   'c', '100':    'd', '0':      'e',
    '0010':   'f', '110':    'g', '0000':   'h', '00':     'i', '0111':   'j',
    '101':    'k', '0100':   'l', '11':     'm', '10':     'n', '111':    'o',
    '0110':   'p', '1101':   'q', '010':    'r', '000':    's', '1':      't',
    '001':    'u', '0001':   'v', '011':    'w', '1001':   'x', '1011':   'y',
    '1100':   'z', '01111':  '1', '00111':  '2', '00011':  '3', '00001':  '4',
    '00000':  '5', '10000':  '6', '11000':  '7', '11100':  '8', '11110':  '9',
    '11111':  '0', ' ': ' '
}

DOT = '0'
DASH = '1'
SHORT_PAUSE = '2'
LONG_PAUSE = '3'
RESET_PAUSE = '4'

from functools import reduce
def decode_morsecode(s):
    """Decode a morse-encoded string s to latin alphanumerics"""
    return ''.join(map(lambda l: MORSE_MAPPING.get(l, '?'), filter(None,
                         reduce(lambda acc, n: acc + [' '] + n, [w.split(SHORT_PAUSE) for w in s.split(LONG_PAUSE)]))))

def morse_input(s):
    """Read morse input from the serial s and return each string
    of chars broken up by short and long pauses"""
    buf = []
    while True:
        b = ser.read().decode('utf-8')
        buf.append(b)
        if b == RESET_PAUSE:
            buf = []
        if b == LONG_PAUSE or b == SHORT_PAUSE:
            yield ''.join(buf)
            buf = []

if __name__ == "__main__":
    with serial.Serial(SERIAL_DEV_PATH, 9600, timeout=None) as ser:
        list(map(lambda x: print(x, end='', flush=True), map(decode_morsecode, morse_input(ser))))
