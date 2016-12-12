# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:25:40 2016

@author: ben / greg


Hamiltonien - 2e version (voir VDC - augmentation cycles pour 1ere version)

G : graphe hamiltonien ou non

But : trouver le plus grand cycle dans G, si possible hamiltonien par conséquent

"""

from random import *
import time
from math import sqrt
#import pylab as pl
    
def imp_dfs(sommets, G,i):
    marques = []
    peres = []
    def dfs_aux(j,G,marques,dad):
        marques.append(j)
        peres.append(dad)
        unique = False
        for e in G[j]:
            if e not in marques and e not in sommets and len(G[e])==2:
                dfs_aux(e,G,marques,j)
                unique = True
        if not unique:
            for e in G[j]:
                if e not in marques and e not in sommets:
                    dfs_aux(e,G,marques,j)
    dfs_aux(i,G,marques,i)
    return marques, peres

def find_path(y, marques, peres):
    sommets = []
    while peres[marques.index(y)]!=y:
        sommets.append((peres[marques.index(y)],y))
        y = peres[marques.index(y)]
    sommets.reverse()
    return sommets
    
def randomgraph(n):
    l = [[] for i in range(n)]
    for i in range(n):
        k = 2
        for j in range(k):
            while True:
                s = randint(0, n)
                if s != i and (not s in l[i]):
                    l[i].append(s)
                    l[s].append(i)
                    break
            if len(l[i])>k:
                break
    return l
    
def dijkstra(G, sommetsinterdits, depart, arrivee):
    openlist = []
    closedlist = [depart]
    print "depart", depart
    def dijaux(s, poids):
        voisins = G[s]
        for v in voisins:
            if not v in sommetsinterdits:
                print v
                if v == arrivee:
                    closedlist.append(arrivee)
                    print "fini2"
                    return
                inclosedlist = False
                posopen = 0
                inopenlist = False
                for e in closedlist:
                    if e == v:
                        inclosedlist = True
                        break
                for i in range(len(openlist)):
                    e = openlist[i]
                    if e[0] == v:
                        inopenlist = True
                        posopen = i
                        break
                if not inclosedlist:
                    if inopenlist:
                        openlist[posopen] = (openlist[posopen][0],min(openlist[posopen][1], poids+1))
                    else:
                        openlist.append((v, poids+1))
        if openlist == []:
            for i in range(len(closedlist)):
                closedlist.pop(0)
            return
        
        posmin = 0
        poidsmin = openlist[0][1]
        for i in range(len(openlist)):
            if openlist[i][1] < poidsmin:
                posmin = i
                poidsmin = openlist[i][1]
        closedlist.append(openlist[posmin][0])
        smin = openlist[posmin]
        openlist.remove(openlist[posmin])
        dijaux(smin[0], poidsmin)
    dijaux(depart, 0)
    return closedlist

def PetitEtang(G, depart):
    n = len(G)
    chemin = []
    tempG = copydoublelist(G)
    tempG[0].remove(depart)
    marques, peres = imp_dfs([],tempG, 0)
    if depart in marques:
        p = find_path(depart, marques, peres)
        for e in p:
            chemin.append(e)
    else:
        return [(0, depart)]
    chemin.append((depart, 0))
    
    lim = 0
    
    while True and lim < 5:
        lim += 1
        if len(chemin) == n:
            break
        sommets = [e[0] for e in chemin]
        
        print chemin
        
        augmentationpossible = False
        for arete in chemin:
            sommet1 = arete[0]
            sommet2 = arete[1]
            sommets.remove(sommet1)
            sommets.remove(sommet2)
            G[sommet1].remove(sommet2)
            marques, peres = imp_dfs(sommets, G, sommet1)
            if sommet2 in marques:
                p = find_path(sommet2, marques, peres)
                for e in p:
                    chemin.append(e)
                chemin.remove((sommet1, sommet2))
                augmentationpossible = True
                break
            sommets.append(sommet1)
            sommets.append(sommet2)
            G[sommet1].append(sommet2)
        if not augmentationpossible:
            #augmentation généralisée
            inchemin = []
            for e in chemin:
                inchemin.append(e[0])
            poidsmin = n
            finalpath = []
            depart = 0
            arrivee = 0
            for u in range(len(inchemin)):
                for v in range(u+2,len(inchemin)):
                    if v-u != len(inchemin)-1:
                        (i,j) = (inchemin[u], inchemin[v])
                        sommetsmodifies = copylist(sommets)
                        sommetsmodifies.remove(i)
                        sommetsmodifies.remove(j)
                        print (i,j)
                        print sommetsmodifies
                        p = dijkstra(G, sommetsmodifies, i, j)
                        if p!=[] and len(p) < poidsmin:
                            finalpath = []
                            for k in range(len(p)-1):
                                finalpath.append((p[k], p[(k+1)]))
                            poidsmin = len(p)
                            depart = i
                            arrivee = j
            print (depart, arrivee)
            print finalpath
            taille_dep_arr = 0
            counting = False
            pathinchemin = []
            for e in chemin:
                if e[0] == arrivee:
                    counting = False
                if counting:
                    taille_dep_arr +=1
                    pathinchemin.append(e)
                if e[0] == depart:
                    counting = True
                    taille_dep_arr +=1
                    pathinchemin.append(e)
            print pathinchemin
            if taille_dep_arr <= len(chemin)/2:
                for e in pathinchemin:
                    chemin.remove(e)
            else:
                chemin = []
                for e in pathinchemin[::-1]:
                    chemin.append((e[1], e[0]))
            for e in finalpath:
                chemin.append(e)
    return chemin
                
def hamiltonien(graphe):
    n = len(graphe)
    depart = graphe[0][0]
    G = copydoublelist(graphe)
    Mat = PetitEtang(G, depart)
    Mat2 = [(i,j) for (i,j) in Mat]
    return Mat2
    
def copylist(l):
    temp = []
    for e in l:
        temp.append(e)
    return temp
        
def copydoublelist(l):
    temp = []
    for e in l:
        ligne = []
        for x in e:
            ligne.append(x)
        temp.append(ligne)
    return temp
I = 10000
    
def verifhamilton(n, chemin):
    sommets = [-1]*n
    for e in chemin:
        (i,j)=e
        sommets[i] = j
    if -1 in sommets:
        return False
    current = 0
    while True:
        if sommets[current] == -1:
            return False
        s = current
        current = sommets[s]
        sommets[s] = -1
        if max(sommets)<0:
            break
    return True
        

def graphedense(n):
    l = []
    for i in range(n):
        ligne = []
        for j in range(n):
            if j != i:
                ligne.append(j)
        l.append(ligne)
    return l
    
#def orderPath(Se):
#    S = list(Se)
#    ordonne = []
#    ordonne.append(S.pop(0))
#    for i in range(len(S)):
#        a_chercher = ordonne[-1][1]
#        for e in S:
#            if e[0]==a_chercher:
#                ordonne.append(S.pop(S.index(e)))
#    return ordonne

def orderPath2(Se):
    S = list(Se)
    ordonne = []
    current = 0
    for e in S:
        if e[0] == current:
            ordonne.append(e)
            S.remove(e)
            current = e[1]
            break
    
    while current != 0:
        trouve = False
        for e in S:
            if e[0] == current:
                ordonne.append(e)
                S.remove(e)
                current = e[1]
                trouve = True
                break
            if e[1] == current:
                ordonne.append((e[1], e[0]))
                S.remove(e)
                current = e[0]
                trouve = True
                break
        if not trouve:
            return []
    return ordonne

def sortAretes(G, P):
    triplets = []
    for i in range(len(G)):
        for j in range(len(G[i])):
            triplets.append((i ,G[i][j], P[i][j]))
    def ordre((a,b,c), (a1,b1,c1)):
        if c < c1:
            return 1
        elif c == c1:
            return 0
        else:
            return -1
    triplets.sort(cmp = ordre)
    return [(i,j) for (i,j,k) in triplets]

def voyageurdecommerce(G, P):
    n = len(G)
    L = sortAretes(G, P)
    chemin = []
    while True:
        (i,j)=L.pop(0)
        L.remove((j,i))
        G[i].remove(j)
        G[j].remove(i)
        taille = 0
        G2 = copydoublelist(G)
        H = hamiltonien(G2)
        print (i,j), "enlevee"
        print "H : "+str(orderPath2(H))
        if not verifhamilton(n, H):
            print (i,j), " dans le chemin"
            G[i].append(j)
            G[j].append(i)
            chemin.append((i,j))
        if len(chemin)==n:
            break
    return chemin

def randompoids(G):
    P = []
    for i in range(len(G)):
        P.append([])
        for j in range(len(G[i])):
            P[i].append(0)
    for i in range(len(G)):
        for j in range(len(G[i])):
            p = randint(1, 10)
            P[i][j] = p
            P[G[i][j]][G[G[i][j]].index(i)] = p
    return P
        
    
#compte = 0
#for i in range(10000):
#    G = randomgraph(50)
#    G2 = copydoublelist(G)
#    t = time.time()
#    S = hamiltonien(G)
#    #print "Temps mis : "+str(time.time()-t)+"s"
#    v=verifhamilton(len(G2), S) 
#    if not v:
#        compte+=1
#    print "Chemin hamiltonien : "+str(v)
#print compte

def getClosure(G):
    n = len(G)
    G_closure = copydoublelist(G)
    degres = []
    for i in range(n):
        degres.append(len(G[i]))
    n = len(G)
    modif = True
    while modif:
        modif = False
        for i in range(n):
            for j in range(n):
                if i != j and (not j in G_closure[i]) and (not i in G_closure[j]):
                    if degres[i]+degres[j] >= n:
                        G_closure[i].append(j)
                        G_closure[j].append(i)
                        degres[i] = degres[i]+1
                        degres[j] = degres[j]+1
                        modif = True
        
    return G_closure
    
    
#G = [[2, 1, 3, 4], [0, 2, 7], [0, 1, 4, 5, 9], [0, 8, 9], [2, 0, 7, 6], [6, 2, 7, 8], [5, 4, 8], [1, 4, 5], [3, 6, 5], [3, 2]]

def randomhamiltongraph(n, nbaretes):
    G = []
    aretespossibles = []
    for i in range(n):
        for j in range(n):
            if i != j:
                aretespossibles.append((i,j))
    
    for i in range(n):
        G.append([])
    for k in range(n):
        G[k].append((k+1)%n)
        G[(k+1)%n].append(k)
        aretespossibles.remove((k,(k+1)%n))
        aretespossibles.remove(((k+1)%n,k))
        
    #nbaretes = randint(n/2, n)
    for k in range(nbaretes):
        i = randint(0,len(aretespossibles)-1)
        (a,b)=aretespossibles[i]
        G[a].append(b)
        G[b].append(a)
        aretespossibles.remove((a,b))
        aretespossibles.remove((b,a))
    #permutations des sommets de G pour perturber l'algo (choix du cycle
    #initial trivial sinon)
    def permute(l_m):
        l = copylist(l_m)
        toreturn = []
        for k in range(len(l)):
            i = randint(0,len(l)-1)
            toreturn.append(l[i])
            l.remove(l[i])
        return toreturn
    for i in range(n):
        G[i] = permute(G[i])
    return G
    
def hamiltonien_bourrin(G):
    n = len(G)
    def possibilites(l):
        if len(l[0]) == n:
            return l
        f = []
        for e in l:
            s = e[-1]
            for v in G[s]:
                if not v in e:
                    f.append(e+[v])
        return possibilites(f)
        
    l = possibilites([[0]])
    for e in l:
        if 0 in G[e[-1]]:
            return e
    return []
    

#l = []
#n = 80
#for k in range(1,100):
#    print k
#    prop = 0
#    for u in range(100):
#        m = 0.02*k
#        G = randomhamiltongraph(n, int(m*n*sqrt(n)))
#        #C = getClosure(G)
#        H = hamiltonien(G)
#        v = verifhamilton(len(G),H)
#        if v:
#            prop +=1
#    l.append((m, prop))
#for e in l:
#    print "Proportion "+str(e[0])+" -> taux : "+str(e[1])+"%"
    
#l = []
#valeurs = []
#props = []
#n = 40
#for k in range(1,65):
#    print k
#    prop = 0
#    m = 0.02*k
#    for u in range(100):
#        G = randomhamiltongraph(n, int(m*sqrt(2*n)*n))
#        #C = getClosure(G)
#        H = hamiltonien(G)
#        v = verifhamilton(len(G),H)
#        if v:
#            prop +=1
#    l.append((m, prop))
#    valeurs.append(m)
#    props.append(prop)
    
#for e in l:
#    print "Proportion "+str(e[0])+" -> taux : "+str(e[1])+"%"

#pl.plot(valeurs,props)


G = [[9, 1], [0, 2, 7], [1, 3, 9], [4, 2, 6], [6, 3, 5], [4, 9, 6], [5, 7, 3, 4], [1, 6, 8], [7, 9], [2, 8, 0, 5]]
print G
H = hamiltonien(G)
print H
print verifhamilton(len(G), H)

#G = randomhamiltongraph(400,10000)
#print "got graph"
#C = getClosure(G)
#print "got closure"
#print verifhamilton(len(C),hamiltonien(C))