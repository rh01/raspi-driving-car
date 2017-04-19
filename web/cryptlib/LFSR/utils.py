# coding: utf-8

import re
import sys

def str_LFSR(init, limited=False):
    """\
    移位寄存器，生成字符串形式的01序列
    init: 一个长度为5的01字串
    limited: 若为True, 则只生成一个周期序列
    """
    f = lambda x: "0" if x[0]==x[3] else "1"
    if not re.match(r"^[01]{5}$", init):
        raise ValueError("Parameter must be 0-1 string of length 5")
    arr = init

    while True:
        yield arr[0]
        t = f(arr)
        arr = arr[1:]+t
        if limited and arr==init:
            break

def byte_LFSR(init):
    """\
    移位寄存器，无限生成序列
    init: 一个长度为5的01字串
    生成值: int
    """
    if not 0<init<=31:
        raise ValueError("Parameter init must be in (0, 31]")

    def f(x):
        a1 = (x&1<<4)>>4
        a4 = (x&1<<1)>>1
        return a1^a4

    reg = init
    while True:
        buf = 0
        for i in range(8):
            fback = f(reg)
            output = (reg&0b10000)>>4

            buf = buf<<1 | output
            reg = (reg<<1)|fback

        yield buf

def gen_seq(num):
    s = bin(num)[2:]
    gen = str_LFSR(bin(num)[2:].zfill(5), limited=True)
    genarray = "".join(list(gen))
    return [num, len(genarray), genarray]

if __name__ == '__main__':
    for num in range(31):
        gen = str_LFSR(bin(num)[2:].zfill(5), limited=True)
        genarray = "".join(list(gen))
        print num, len(genarray), genarray

    gen = byte_LFSR(19)
    for num in range(31):
        print next(gen),
