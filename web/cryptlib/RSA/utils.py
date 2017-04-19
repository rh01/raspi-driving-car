# coding: utf-8

import timeit
import random

def calc_mod(x, r, n):
    """Calculate the value of x**r mod n"""
    a, b, c = x, r, 1
    while b != 0:
        while b%2 == 0:
            b = b/2
            a = a*a%n
        else:
            b = b-1
            c = (c*a)%n
    return c

def calc_reverse(m, n):
    """Calculate the value of m^(-1) mod n"""
    N = n
    m %= n
    m, n = n, m
    q = []
    while True:
        q.append(m//n)
        m, n = n, m%n
        if n == 1:
            break
    P, Q = [1, q[0]], [0, 1]
    for i in range(2, len(q)+1):
        P.append(P[i-2]+P[i-1]*q[i-1])
        Q.append(Q[i-2]+Q[i-1]*q[i-1])

    return (-1)**len(q)*P[-1]%N

def is_prime(n, k=5000):
    """Test whether n is a prime, repeat k times."""
    def mill_rab(n):
        b = 0
        while b%2 == 0:
            b = random.randint(2, n-1)      # 产生一个奇数b
        
        s, m = 0, n-1
        while m%2 == 0:                     # n-1 = (2**s)*m
            m //= 2
            s += 1

        if calc_mod(b, m, n) == 1:
            return True
        else:
            for r in xrange(s):
                if calc_mod(b, 2**r*m, n) == n-1:
                    return True
        return False

    if n in [0, 1]:
        return False
    elif n == 2:
        return True
    for i in range(k):
        if not mill_rab(n):
            return False
    return True

if __name__ == '__main__':
    print(calc_reverse(11, 840))
