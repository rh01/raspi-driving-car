# coding: utf-8

import cPickle as pickle
import base64
from collections import defaultdict
from flask import flash, session
import cryptlib

from Crypto.Random import random
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA

def exec_form(ctype, form):
    answer = ""
    other_params = {}

    if ctype == "classic":
        return exec_classic(form)
    elif ctype == "des":
        return exec_des(form)
    elif ctype == "rsa":
        return exec_rsa(form)
    elif ctype == "lfsr":
        return exec_lfsr(form)
    elif ctype == "dsa":
        return exec_dsa(form)

    return form, other_params

def exec_classic(form):
    other_params = {}

    key1 = int(form.key1.data)
    key2 = int(form.key2.data)

    if form.encrypt.data:
        text = form.text.data
        form.text.data = ""
        form.cipher.data = cryptlib.affine_encrypt(text, key1, key2)

    elif form.decrypt.data:
        cipher = form.cipher.data
        form.cipher.data = ""
        form.text.data = cryptlib.affine_decrypt(cipher, key1, key2)

    elif form.stat.data:                                                    # 统计原文/密文中各字符的出现次数
        text = form.text.data.lower()
        cipher = cryptlib.affine_encrypt(text, key1, key2)
        form.cipher.data = cipher

        freq_dict = defaultdict(lambda: [0, 0])
        count = 0
        for c in text:
            if 97<=ord(c)<=122:
                freq_dict[c][0] += 1
                count += 1
        for c in cipher:
            if 97<=ord(c)<=122:
                freq_dict[c][1] += 1
        freq_list = [(x[0].upper(),
                            round(float(x[1][0])/count, 4),
                            round(float(x[1][1])/count, 4))
                         for x in freq_dict.items()]
        freq_list.sort(key=lambda x: x[0])

        d = dict()
        for i,j,k in freq_list:
            i = str(i)
            d[i]  = j
        other_params["freq_list"] = d

    return form, other_params

def exec_des(form):
    key = form.key.data
    other_params = {}
    if form.encrypt.data:
        text = form.text.data
        key = form.key.data

        des = cryptlib.DES(key)
        form.cipher.data = unicode(des.DES_encrypt(text.encode("utf-8")), 
                            encoding="utf-8")

    elif form.decrypt.data:
        cipher = form.cipher.data
        key = form.key.data

        des = cryptlib.DES(key)
        try:
            form.text.data = unicode(des.DES_decrypt(cipher.encode("utf-8")),
                            encoding="utf-8")
        except base64.binascii.Error:
            flash(u"密文格式错误，请检查密文格式！")
        except UnicodeDecodeError:
            form.text.data = u""
            flash(u"密文/密钥错误，无法进行解密！")

    return form, other_params

def exec_rsa(form):
    other_params = {}
    if form.encrypt.data:
        text = form.text.data.upper()

        rsa = cryptlib.RSA()
        form.cipher.data = unicode(rsa.RSA_encrypt(text.encode("utf-8")), 
                            encoding="utf-8")

    elif form.decrypt.data:
        cipher = form.cipher.data
        rsa = cryptlib.RSA()
        form.text.data = unicode(rsa.RSA_decrypt(cipher.encode("utf-8")),
                            encoding="utf-8")

    return form, other_params

def exec_lfsr(form):
    other_params = {}

    # 产生生成序列
    seq_list = []
    for num in range(32):
        seq_list.append(cryptlib.LFSR_gen_seq(num))
    other_params["seq_list"] = seq_list

    # key = 19
    if form.validate_on_submit():
        key = int(form.key.data)

        if form.encrypt.data:
            text = form.text.data

            lfsr = cryptlib.LFSR(key)
            form.cipher.data = unicode(lfsr.LFSR_encrypt(text.encode("utf-8")), 
                                encoding="utf-8")

        elif form.decrypt.data:
            cipher = form.cipher.data

            lfsr = cryptlib.LFSR(key)
            try:
                form.text.data = unicode(lfsr.LFSR_decrypt(cipher.encode("utf-8")),
                                encoding="utf-8")
            except base64.binascii.Error:
                flash(u"密文格式错误，请检查密文格式！")
            except UnicodeDecodeError:
                form.text.data = u""
                flash(u"密文/密钥错误，无法进行解密！")

    return form, other_params

def exec_dsa(form):
    other_params = {}
    message = form.text.data.encode("utf-8")

    hash_ = SHA.new(message)
    form.sha.data = hash_.hexdigest()
    h = hash_.digest()

    # 恢复key
    if not session.get("key"):
        key = DSA.generate(1024)
        session["key"] = pickle.dumps(key)
    else:
        key = pickle.loads(session["key"])

    if form.sign.data:
        k = random.StrongRandom().randint(1,key.q-1)
        sig = key.sign(h, k)
        form.signature.data = "%s, %s"%(hex(sig[0])[2:-1], hex(sig[1])[2:-1])

    elif form.verify.data:
        ssig = form.signature.data.split(", ")
        try:
            sig = (int(ssig[0], base=16), int(ssig[1], base=16))
        except (IndexError, UnicodeEncodeError):
            flash(u"签名格式错误！")
        else:
            if key.verify(h, sig):
                flash(u"签名验证成功！")
            else:
                flash(u"签名验证失败！")

    return form, other_params
