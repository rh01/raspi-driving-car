# coding: utf-8

def __str_to_list(str_):
    return [ord(c)-ord("a") for c in str_]

def __list_to_str(list_):
    # print list_
    return "".join(map(lambda n: chr(n+97), list_))

def __getNeg(u, n):
    n1, n2 = n, u
    b1, b2 = 0, 1
    q, r = n1/n2, n1%n2

    while r:
        n1, n2 = n2, r
        t = b2
        b2 = b1-q*b2
        b1 = t;
        q, r =  n1/n2, n1%n2

    if b2 < 0:
        b2 += n
    return b2

def affine_encrypt(text, key1, key2):
    text = text.lower()
    text_keys = __str_to_list(text)
    k = text_keys
    crypt_keys = map(lambda n: (key1+key2*n)%26 if 0<=n<=25 else n, text_keys)
    crypt_keys = filter(lambda n: n+95 in xrange(256), crypt_keys)
    crypt_text = __list_to_str(crypt_keys)
    return crypt_text

def affine_decrypt(text, key1, key2):
    text = text.lower()
    neg_key2 = __getNeg(key2, 26)
    text_keys = __str_to_list(text)
    decrypt_keys = map(lambda n: neg_key2*(n-key1)%26 if 0<=n<=25 else n, text_keys)
    decrypt_keys = filter(lambda n: n+95 in xrange(256), decrypt_keys)
    decrypt_text = __list_to_str(decrypt_keys)
    return decrypt_text
