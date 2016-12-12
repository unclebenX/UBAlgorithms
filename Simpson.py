# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:14 2015

@author: uncleben

Algorithme de calcul exact de \beta
"""

import math
import time

def calcule_simpson(f,N):
    l=[]
    inter = 1./N
    for k in range(N):
        s = inter*((f((k+0.)/N)/6.)+(f((k+1.)/N)/6.)+((2./3.)*f((k+.5)/N)))        
        l.append(s)
    return l
    
def somme(l):
    S = 0.
    for e in l:
        S+=e
    return S
    
#Attention, complexité atomique. HANDLE WITH CARE.
def Beta(vals,N_pas):
    parts = range(N_pas)
    valeurs = [calcule_simpson(f,N_pas) for f in vals]
    n_joueurs = len(vals)
    return beta_recursif(parts,valeurs,n_joueurs,[[] for i in range(n_joueurs)])

def beta_recursif(parts,valeurs,n_joueurs,parts_joueurs):
    global s
    if len(parts) == 0:
        l = []
        for i in range(n_joueurs):
            l.append(somme([valeurs[i][k] for k in parts_joueurs[i]]))
        return min(l)
    p = parts.pop()
    l2 = []
    for i in range(n_joueurs):
        parts2 = list(parts)
        parts_joueurs[i].append(p)
        l2.append(beta_recursif(parts2,valeurs,n_joueurs,parts_joueurs))
        parts_joueurs[i].remove(p)
    return max(l2)

"""ZONE FONCTIONS"""
            
def calcul_integrale(f,i,j,pas):
    integrale=0
    x=i
    while x<j:
        integrale+=f(x)*pas
        x+=pas
    return integrale

def v1(x):
    return 2.*x

def v2(x):
    return 1.
    
I3 = calcul_integrale(lambda x : math.sin(20*x) + 1.,0.,1.,0.000001)

def v3(x):
    global I3
    return (math.sin(20*x) + 1)/I3

I4 = calcul_integrale(lambda x : math.exp(x**2),0.,1.,0.00001)

def v4(x):
    global I4
    return math.exp(x**2)/I4
    
I5 = calcul_integrale(lambda x : -((x-.5)**2),0.,1.,0.00001)

def v5(x):
    global I5
    return -((x-.5)**2)/I5
    
def integrale_sup(vals2, n):
    I = 0
    actuel = 0.
    inter = 1./n
    m = len(vals2)
    for i in range(n):
        I+=inter * max([vals2[j](actuel) for j in range(m)])
        actuel += inter
    return I
    
"""ZONE EXECUTION"""



vals = [v2,v5]
#print Beta(vals,27)

print
print "Calcul des Beta"
print
s = (1./len(vals))*integrale_sup(vals,10000)
print "Valeur maximale : ", s
print

b=time.time()

for N in range(1,27):
    a = time.time()
    b = Beta(vals,N)
    print N, b, s-b, time.time()-a

#print Beta(vals, 26)
    
print "Temps d'exécution :", time.time()-b
print