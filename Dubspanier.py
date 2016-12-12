# -*- coding: utf-8 -*-
"""
Algorithme de Dubins-Spanier
"""

import pylab as pl
from math import *
import numpy as np
import matplotlib as mp
import random as rnd

couleurs = ['r','b','g','y','gray']

def calcul_integrale(f,i,j,pas):
    integrale=0
    x=i
    while x<j:
        integrale+=f(x)*pas
        x+=pas
    return integrale


def dubspanier_rec(vals, inter, epsilon, position, n):
    a = position
    if len(vals) == 0:
        return []
    prop= 1./n
    m = len(vals)
    current_int = [0. for i in range(n)]
    while a<1.:
        a+=inter
        for i in range(m):
            current_int[i]+=vals[i][0](a)*inter
        if max(current_int)>prop-epsilon:                
            player = vals[np.argmax(current_int)][1]
            vals.pop(np.argmax(current_int))
            v = [(player,position,a,max(current_int))]
            w = dubspanier_rec(vals,inter,epsilon,a,n)
            return v+w
    return None

#Première amélioration.
def dubspanier_rec2(vals, inter, epsilon, position, n):
    a = position
    if len(vals) == 0:
        return []
    #On réajuste la proportionnalité au fur et à mesure pour remplir le gâteau.
    prop= (1.-position)/(len(vals))
    m = len(vals)
    current_int = [0. for i in range(n)]
    while a<1.:
        a+=inter
        for i in range(m):
            current_int[i]+=vals[i][0](a)*inter
        if max(current_int)>prop-epsilon:                
            player = vals[np.argmax(current_int)][1]
            vals.pop(np.argmax(current_int))
            v = [(player,position,a,max(current_int))]
            w = dubspanier_rec2(vals,inter,epsilon,a,n)
            return v+w
    return None
    
#Seconde amélioration.
def dubspanier(vals, inter, epsilon, n):
    prop = 1./n
    vals2 = list(vals)
    l = dubspanier_rec3(vals2, inter, epsilon, 0., prop, n)
    print "BA",l
    m = l[len(l)-1][2]
    while 1.-m>0.03:
        vals2 = list(vals)
        prop += (1.-m)/n
        print "here"
        l = dubspanier_rec3(vals2, inter, epsilon, 0., prop, n)
        print "here"        
        m = l[len(l)-1][2]
    return l

def dubspanier_rec3(vals, inter, epsilon, position, prop, n):
    a = position
    if len(vals) == 0:
        return []
    m = len(vals)
    current_int = [0. for i in range(n)]
    while a<1.:
        a+=inter
        for i in range(m):
            current_int[i]+=vals[i][0](a)*inter
        if max(current_int)>prop-epsilon:                
            player = vals[np.argmax(current_int)][1]
            vals.pop(np.argmax(current_int))
            v = [(player,position,a,max(current_int))]
            w = dubspanier_rec3(vals,inter,epsilon,a,prop,n)
            return v+w
    return None

#print(dubspanier([[v1,1],[v2,2],[v3,3],[v4,4],[v5,5]],0.001,0.000001,5))

def v1(x):
    return 2.*x

def v2(x):
    return 1.
    
I3 = calcul_integrale(lambda x : np.sin(20*x) + 1.,0.,1.,0.000001)

def v3(x):
    global I3
    return (np.sin(20*x) + 1)/I3

I4 = calcul_integrale(lambda x : np.exp(x**2),0.,1.,0.00001)

def v4(x):
    global I4
    return np.exp(x**2)/I4
    
I5 = calcul_integrale(lambda x : -((x-.5)**2),0.,1.,0.00001)

def v5(x):
    global I5
    return -((x-.5)**2)/I5
    
p=3
#I4 = calcul_integrale(lambda x : v2(x)**(p+1)/(v1(x)**p+v2(x)**p+v3(x)**p+v4(x)**p+v5(x)**p),0.,1.,0.00001)
#print I4, "I4"

def dubspanier_plot(vals2,inter,epsilon,n):
    vals = list(vals2)
    l = dubspanier(vals,inter,epsilon,n)
    print(l)
    x = pl.linspace(0.,1.,100)
    fig = mp.pyplot.figure()
    ax = fig.add_subplot(111)
    global couleurs
    for e in enumerate(l):
        (player,debut,fin,val) = e[1]
        tab = list(np.linspace(debut,fin,10))
        data = [vals2[player-1][0](m) for m in tab]
        z = [(debut,0.)] + zip(tab,data) + [(fin,0.)]
        c = couleurs[e[0]]
        mp.pyplot.plot(x,[vals2[player-1][0](i) for i in x],c)
        poly = mp.patches.Polygon(z,facecolor = c)
        ax.add_patch(poly)
        
def calcul_beta(vals2, inter, epsilon, n):
    recherche = 1./n
    b = True
    while b:
        vals = list(vals2)
        try:        
            l = dubspanier_rec3(vals,inter,epsilon,0.,recherche,n)
        except:
            b = False
        recherche += 0.00005
    return recherche
    
#print calcul_beta([[v1,1],[v2,2],[v3,3],[v4,4],[v5,5]],0.001,0.000001,5)
print calcul_beta([[v1,1],[v4,2]],0.001,0.000001,2)    

def integrale_sup(vals2, n):
    I = 0
    actuel = 0.
    inter = 1./n
    m = len(vals2)
    for i in range(n):
        I+=inter * max([vals2[j][0](actuel) for j in range(m)])
        actuel += inter
    return I
    
def integrale_sup2(vals2, n, p):
    I = 0.
    actuel = 0.
    inter = 1./n
    for i in range(n):
        I+=inter * (vals2[p][0](actuel)**2)/(sum([v[0](actuel) for v in vals2]))
        actuel += inter
    return I
    
#print (.2)*integrale_sup([[v1,1],[v2,2],[v3,3],[v4,4],[v5,5]],10000)
print .5*integrale_sup([[v3,0],[v4,1]],10000)
    
dubspanier_plot([[v1,1],[v2,2],[v3,3],[v4,4],[v5,5]],0.001,0.000001,5)
#dubspanier_plot([[v1,1],[v2,2],[v3,3]],0.001,0.000001,4)

def rand_function(n,nu):
    t = np.linspace(0.,1.,n)
    y = [rnd.random()+.1]
    for i in range(1,n):
        a = rnd.randint(0,1)
        if a == 0 or y[i-1]-nu<0:
            y.append(y[i-1]+(rnd.random()*nu))
        else:
            y.append(y[i-1]-(rnd.random()*nu))
    return t, np.array(y)
    
def discrete_int(t,y):
    I = t[1]*y[0]
    for i in range(1,len(t)):
        I+= (t[i]-t[i-1])*y[i]
    return I
 
def disc_dubspanier(vals, inter, epsilon, position, n):
    a = position
    if len(vals) == 0:
        return []
    prop= 1./n
    m = len(vals)
    current_int = [0. for i in range(n)]
    while a<1.:
        a+=inter
        for i in range(m):
            current_int[i]+=vals[i][0][a*300]*inter
        if max(current_int)>prop-epsilon:                
            player = vals[np.argmax(current_int)][1]
            vals.pop(np.argmax(current_int))
            v = [(player,position,a,max(current_int))]
            w = disc_dubspanier(vals,inter,epsilon,a,n)
            return v+w
    return None
    
def disc_dubspanier2(vals, inter, epsilon, position, n):
    a = position
    if len(vals) == 0:
        return []
    prop= (1.-position)/len(vals)
    m = len(vals)
    current_int = [0. for i in range(n)]
    while a<1.:
        a+=inter
        for i in range(m):
            current_int[i]+=vals[i][0][a*300]*inter
        if max(current_int)>prop-epsilon:                
            player = vals[np.argmax(current_int)][1]
            vals.pop(np.argmax(current_int))
            v = [(player,position,a,max(current_int))]
            w = disc_dubspanier2(vals,inter,epsilon,a,n)
            return v+w
    return None
    
def disc_dubspanier_opti(vals, inter, epsilon, n):
    prop = 1./n
    vals2 = list(vals)
    l = disc_dubspanier3(vals2, inter, epsilon, 0., prop, n)
    m = l[len(l)-1][2]
    while 1.-m>0.03:
        vals2 = list(vals)
        prop += (1.-m)/n
        l = disc_dubspanier3(vals2, inter, epsilon, 0., prop, n)       
        m = l[len(l)-1][2]
    return l

def disc_dubspanier3(vals, inter, epsilon, position, prop, n):
    a = position
    if len(vals) == 0:
        return []
    m = len(vals)
    current_int = [0. for i in range(n)]
    while a<1.:
        a+=inter
        for i in range(m):
            current_int[i]+=vals[i][0][a*300]*inter
        if max(current_int)>prop-epsilon:                
            player = vals[np.argmax(current_int)][1]
            vals.pop(np.argmax(current_int))
            v = [(player,position,a,max(current_int))]
            w = disc_dubspanier3(vals,inter,epsilon,a,prop,n)
            return v+w
    return None

def dubspanier_plot_disc(vals2,inter,epsilon,n):
    vals = list(vals2)
    l = disc_dubspanier2(vals,inter,epsilon,0.,n)
    print l
    x = pl.linspace(0.,1.,300)
    fig = mp.pyplot.figure()
    ax = fig.add_subplot(111)
    global couleurs
    for e in enumerate(l):
        (player,debut,fin,val) = e[1]
        tab = list(np.linspace(debut,fin,100))
        data = [vals2[player-1][0][m*300] for m in tab]
        z = [(debut,0.)] + zip(tab,data) + [(fin,0.)]
        c = couleurs[e[0]]
        mp.pyplot.plot(x,vals2[player-1][0],c)      
        poly = mp.patches.Polygon(z,facecolor = c)
        ax.add_patch(poly)
    
l=[]
for i in range(5):
    t,y = rand_function(300, 0.05)
    I = discrete_int(t,y)
    y = y/I
    l.append((y,i+1))
    
#dubspanier_plot_disc(l,0.01,0.01,5)
    
"""
print discrete_int(np.linspace(0.,1.,300), sup([e[0] for e in l])), "Max"
S = 0
a = disc_dubspanier_opti(l, 0.01, 0.01, 5)
for e in a:
    S+=e[3]
print S, "Valuation totale"
print a
"""