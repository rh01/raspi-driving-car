# coding: utf-8

import base64
from .utils import byte_LFSR

class LFSR(object):
    def __init__(self, key):
        self.key = key
        self.gen = byte_LFSR(key)

    def LFSR_encrypt(self, message):
        cipher = ""
        for char in message:
            key = next(self.gen)
            cchr = key^ord(char)
            cipher += chr(cchr)
        return base64.encodestring(cipher)

    def LFSR_decrypt(self, cipher):
        cipher = base64.decodestring(cipher)
        message = ""
        for char in cipher:
            key = next(self.gen)
            cchr = key^ord(char)
            message += chr(cchr)
        return message
