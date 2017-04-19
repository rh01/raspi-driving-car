# coding: utf-8

import DES_Constant as constant
import base64

class DES(object):
    def __init__(self, key):
        self.key = self._key_generate(key)
        self.sub_keys = self._sub_key_generate()

    def DES_encrypt(self, message):
        """\
        DES加密函数
        message: 明文信息
        返回一个base64序列
        """
        if len(message) % 8 != 0:                                               # 用NUL将明文补足64位
            message += '\0'*(8-len(message)%8)
        message_array = self._str2binarray(message)
        cipher_array = []

        for submessage in message_array:
            subcipher = self.encrypt_array(submessage)
            cipher_array.append(subcipher)

        cipher = base64.encodestring(self._binarray2str(cipher_array))[:-1]

        return cipher

    def DES_decrypt(self, cipher):
        """\
        DES解密函数
        cipher: 密文信息, base64序列
        返回明文信息
        """
        cipher = base64.decodestring(cipher)
        if len(cipher) % 8 != 0:                                               # 用NUL将密文补足64位
            cipher += '\x00'*(8-len(cipher)%8)

        cipher_array = self._str2binarray(cipher)
        message_array = []

        for subcipher in cipher_array:
            submessage = self.decrypt_array(subcipher)
            message_array.append(submessage)

        message = self._binarray2str(message_array)

        index = message.find("\0")                                              # 去除解密信息后面的NUL
        if index > 0:
            message = message[:index]
        return message

    def encrypt_array(self, message):
        """\
        0-1序列加密函数
        """
        message = self._IP(message)                                             # 进行初始置换IP
        left, right = message[:32], message[32:]

        for turn in range(16):
            sub_key = self.sub_keys[turn]
            left, right = right, self._binstrxor(left, self._F(right, sub_key)) 

        message = left + right
        message = self._IP_NEG(message)                                         # 进行逆初始置换IP^-1
        return message

    def decrypt_array(self, cipher):
        """\
        0-1序列解密函数
        """
        cipher = self._IP(cipher)                                               # 进行初始置换IP
        left, right = cipher[:32], cipher[32:]

        for turn in reversed(range(16)):
            sub_key = self.sub_keys[turn]
            left, right = self._binstrxor(right, self._F(left, sub_key)), left

        cipher = left+right
        cipher = self._IP_NEG(cipher)                                           # 进行逆初始置换IP^-1
        return cipher

    def _F(self, array, sub_key):
        """\
        DES核心加密函数F
        """
        array = self._E(array)                                                  # 位选择, 32bit -> 48bit
        array = self._binstrxor(array, sub_key)                                 # 将序列与Ki异或

        temp_arr = array
        arrs = []
        while temp_arr:
            arrs.append(temp_arr[:6])                                           # 将序列分成8组，每组6位
            temp_arr = temp_arr[6:]

        finalarr = ""
        for index, b in enumerate(arrs):
            row = int(b[0]+b[5], base=2)
            col = int(b[1:5], base=2)
            output = constant.S[index][row][col]
            finalarr += bin(output)[2:].zfill(4)

        array = self._P(finalarr)

        return array

    @staticmethod
    def _key_generate(key):
        """\
        依据14位二进制数字生成64位的key
        返回一个长度为64位的0-1字符串
        """
        key = bin(int(key, base=16))[2:]
        key = key.zfill(56)                                                     # 补全key前面的0

        byte_key = ""
        for i in range(8):
            byte = key[i*7:i*7+7]
            byte_key += byte+"0"                                                # 为每7位添加校验位(本程序中直接加0)

        return byte_key

    def _sub_key_generate(self):
        """\
        由64位的key字串生成子密钥K1~K16
        返回16个长度为64位的0-1字符串
        """
        rotate_LS = lambda key, n: key[n:]+key[:n]                              # 循环左移函数

        key = self._PC1(self.key)                                               # 对k进行PC-1置换
        sub_keys = []
        c, d = key[0:28], key[28:56]
        for i in range(1, 17):                                                  # 16轮变换
            c, d = rotate_LS(c, constant.LS[i]), rotate_LS(d, constant.LS[i])   # 对C和D进行循环左移变换
            sub_keys.append(self._PC2(c+d))                                     # 将C和D进行PC-2置换生成子密钥

        return sub_keys

    @staticmethod
    def _PC1(key):
        """\
        对64位key进行PC-1变换, 生成56位key
        """
        ans = ""
        for i in range(56):
            ans += key[constant.PC1[i]-1]

        return ans

    @staticmethod
    def _PC2(key):
        """\
        对56位key进行PC-2变换, 生成48位key
        """
        ans = ""
        for i in range(48):
            ans += key[constant.PC2[i]-1]
    
        return ans

    @staticmethod
    def _str2binarray(str_):
        """\
        将字符串转化为64bit的0-1序列组
        """
        byte_array = bytearray(str_)
        binstr = "".join(map(lambda n: bin(n)[2:].zfill(8), byte_array))
        bin_array = []
        while binstr:
            bin_array.append(binstr[:64])
            binstr = binstr[64:]
        return bin_array

    @staticmethod
    def _binarray2str(bin_array):
        """\
        将64位0-1序列组转化为字符串
        """
        binstr = "".join(bin_array)
        string = ""
        while binstr:
            string += chr(int(binstr[:8], base=2))
            binstr = binstr[8:]

        return string

    @staticmethod
    def _IP(array):
        """\
        初始置换函数IP
        """
        ans = ""
        for num in constant.IP:
            ans += array[num-1]
        return ans

    @staticmethod
    def _IP_NEG(array):
        """\
        逆初始置换函数IP^-1
        """
        ans = ""
        for num in constant.IP_NEG:
            ans += array[num-1]
        return ans

    @staticmethod
    def _binstrxor(arr1, arr2):
        """\
        0-1序列异或函数
        """
        ans = ""
        for i in range(len(arr1)):
            if arr1[i] == arr2[i]:
                ans += "0"
            else:
                ans += "1"

        return ans

    @staticmethod
    def _E(array):
        """\
        位选择函数E
        32 bit -> 48 bit
        """
        ans = ""
        for num in constant.E:
            ans += array[num-1]

        return ans

    @staticmethod
    def _P(array):
        """\
        位选择函数P
        48 bit -> 32 bit
        """
        ans = ""
        for num in constant.P:
            ans += array[num-1]

        return ans

def test():
    a = DES("1234567890abcd")
    k = "试试中文Test for Chinese"
    print k
    t = a.DES_encrypt(k)
    print t
    s = a.DES_decrypt(t)
    print s

if __name__ == '__main__':
    test()
