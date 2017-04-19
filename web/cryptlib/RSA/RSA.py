# coding: utf-8

from utils import *
import base64
from itertools import izip

class RSA(object):
    def __init__(self):
        self.n = 29*31
        self.e = 11
        self.d = 611

        self.__encryptnum = lambda m: calc_mod(m, self.e, self.n)
        self.__decryptnum = lambda c: calc_mod(c, self.d, self.n)

    def __chr_to_num(self, char):
        if char == " ":
            return 0
        elif char == "\0":
            return 27
        else:
            return ord(char)-64

    def __num_to_chr(self, num):
        if num == 0:
            return " "
        elif num == 27:
            return "\0"
        else:
            return chr(num+64)

    def __text_to_array(self, text):
        """将明文字串变为编码列表"""
        array = []
        if len(text)%2 != 0:                                                    # 补"\0"使字符串为两个字符一组
            text += "\0"

        t = map(self.__chr_to_num, text)
        for item in izip(t[::2], t[1::2]):
            pre, after = tuple(item)
            array.append(pre*28+after)

        return array

    def __array_to_text(self, array):
        """将编码列表变为明文字串"""
        text = ""
        for num in array:
            pre = num//28
            after = num%28
            text += "".join(map(self.__num_to_chr, [pre, after]))
        return text

    def __array_to_cipher(self, array):
        """将编码列表变为密文字串"""
        text = ""
        for num in array:
            pre = num//28
            after = num%28
            text += "".join(map(chr, [pre, after]))
        return base64.encodestring(text)

    def __cipher_to_array(self, cipher):
        """将密文字串变为编码列表"""
        array = []
        t = map(ord, base64.decodestring(cipher))
        for item in izip(t[::2], t[1::2]):
            pre, after = tuple(item)
            array.append(pre*28+after)
        return array

    def RSA_encrypt(self, text):
        text_array = self.__text_to_array(text)
        cipher_array = map(self.__encryptnum, text_array)
        cipher = self.__array_to_cipher(cipher_array)
        return cipher

    def RSA_decrypt(self, cipher):
        cipher_array = self.__cipher_to_array(cipher)
        text_array = map(self.__decryptnum, cipher_array)
        text = self.__array_to_text(text_array)
        if text[-1] == "\0":
            return text[:-1]
        return text

if __name__ == '__main__':
    rsa = RSA()
    a = "I LOVE YOU"
    s = rsa.RSA_encrypt(a)
    print s
    d = rsa.RSA_decrypt(s)
    print d
