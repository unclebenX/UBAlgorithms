# -*- coding: utf-8 -*-
"""
Created on Thu May 21 22:23:16 2015

@author: uncleben

CALCUL D'UN PERMANENT <=> EXISTENCE D'UNE ALLOCATION EQUITABLE.
"""

import random    
import time
    
def is_null_submatrix(M,liste_i,liste_j):
    for i in liste_i:
        for j in liste_j:
            if M[i][j]!=0:
                return False
    return True

def get_lc(n,p):
    return get_lc_rec(n,p,0)

def get_lc_rec(n,p,a):
    if p>=n-a+1:
        return []
    if p==0:
        return [[]]
    t1 = get_lc_rec(n,p-1,a+1)
    t2 = get_lc_rec(n,p,a+1)
    for i in range(len(t1)):
        t1[i].append(a)
    return t1+t2
    
print get_lc(4,1)
        
    
def has_null_submatrix(M):
    n=len(M[0])
    for m in range(n):
        l_i=get_lc(n,m+1)
        l_j=get_lc(n,n-m)
        for li in l_i:
            for lj in l_j:
                if is_null_submatrix(M,li,lj):
                    return True
    return False
    
M = [[0,1,1],[0,1,0],[0,1,1]]
print has_null_submatrix(M)

def randomSetMatrix(n):
    M = []
    for i in range(n):
        L = []
        for j in range(n):
            a = random.randint(1,10)
            if a>7:
                L.append(1)
            else:
                L.append(0)
        M.append(L)
    return M
    
def printMatrix(M):
    for L in M:
        print L

M=randomSetMatrix(16)
printMatrix(M)
a = time.time()
print has_null_submatrix(M)
print time.time()-a