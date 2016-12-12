# -*- coding: utf-8 -*-
"""
Spectral encryption algorithm
"""

import random as rnd
import numpy as np

message = "This is badass encryption"
N=1000

def matrixGen(N):
    A = np.eye(N)
    for i in range(N):
        for j in range(i,N):
            r=rnd.randint(1,1000)
            A[i][j]=r
            A[j][i]=r
    return A

def applique_matrice(A,N):
    L = [[rnd.randint(1,1000) for i in range(N)] for j in range(N)]
    AL = [np.dot(A,l) for l in L]
    return L, AL

def calcule_cle(L,AL):
    R = []
    for i in range(len(AL)):
        R.append(np.dot(AL[i],L[i]))
    return R

A = matrixGen(N)
L1, AL1 = applique_matrice(A,N)
L2, AL2 = applique_matrice(A,N)

print calcule_cle(L1,AL2) == calcule_cle(L2,AL1)