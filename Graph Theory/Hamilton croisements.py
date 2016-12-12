# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 10:26:49 2016

@author: uncleben / greg
"""

import random
import time

def decisionGraph(G,X,Y,M):
    G2 = list(G)
    for i in range(len(G2)):
        if i not in X:
            G[i]=[]
    for e in M:
        G2[e[1]]=[e[0]]
    return G2

def suivant_cycle(sommet, cycle):
    for (k,l) in cycle:
        if k == sommet:
           return l
    return None
    
def precedent_cycle(sommet, cycle):
    for (k,l) in cycle:
        if l == sommet:
           return k
    return None

def distanceCycle(sommet1, sommet2, cycle):
    distance = -1
    if sommet1==sommet2:
        return 0
    for k in range(2*len(cycle)):
        (i,j) = cycle[k%len(cycle)]
        if i == sommet1:
            distance = k
        if j == sommet2 and distance!=-1:
            return (k-distance+1)
    return 0
    
def getReachable(sommet, pere, G, cycle):
    atteignables = []
    for s in G[sommet]:
        d = distanceCycle(pere, s, cycle)
        if  d>0 and d< distanceCycle(pere, sommet, cycle)-1:
            atteignables.append(s)
    return atteignables

def dfs(G, a, b, cycle):
    n = len(G)
    chemins = [[] for i in range(n)]
    sommets_atteignables = [[] for i in range(n)] #Liste des sommets atteignables en croisant       
    augmentes = [False]*n    
    
    #Initialisation
    print "INITIALISATION DU DFS"
    for i in G[a]:
        if i != suivant_cycle(a,cycle) and suivant_cycle(i,cycle) != a:
            chemins[suivant_cycle(i,cycle)] = [(a,i), (i, suivant_cycle(i,cycle))]
            sommets_atteignables[suivant_cycle(i,cycle)] = getReachable(suivant_cycle(i, cycle),a,G, cycle)
    print "valeur de chemins initiale :", chemins
    print "valeur de sommets_atteignables :", sommets_atteignables
    changement_effectue = True
    while True:
        print ""
        print "NOUVEAU WHILE"
        changement_effectue = False
        
        #On choisit le chemin le plus avancé
        chemin_v = [-1]
        for u in range(len(chemins)):
            if augmentes[u] == False:
                chemin_v = chemins[u]
        if chemin_v == [-1]:
            return []
        i = chemins.index(chemin_v)
        for c in chemins:
            if len(c) > len(chemin_v) and augmentes[chemins.index(c)]==False:
                chemin_v = c
                i = chemins.index(chemin_v)
        chemin = list(chemin_v)
        if chemin == []:
            return []
                
        print "arete", a, b
        print "cycle", cycle
        print "chemins", chemins
        print "att", sommets_atteignables
        print "augmentes", augmentes
        print "chemin", chemin
        s = chemin[-1]
        sommet_actuel = s[1]
        for sommet in sommets_atteignables[sommet_actuel]:
            if sommet == b:
                p = chemin+[(sommet_actuel, sommet)]
                sembcycle = list(cycle)
                sembcycle.remove((a,b))
                for k in range(len(p)):
                    if k%2 == 0:
                        sembcycle.append(p[k])
                    else:
                        sembcycle.remove(p[k])
                sembcycle = orderPath2(sembcycle)
                if len(sembcycle)==n:
                    return p
            if sommet not in [chemin[2*k+1][0] for k in range(int(len(chemin)/2))] and (sommet, sommet_actuel) not in chemin and (sommet!=a and suivant_cycle(sommet,cycle) != a):
                suivant = suivant_cycle(sommet, cycle)
                nouveaux_atteignables = getReachable(suivant,sommet_actuel,G,cycle)
                atteignables = sommets_atteignables[suivant]                    
                if len(atteignables)<=len(nouveaux_atteignables):
                    chemins[suivant] = copylist(chemin) + [(sommet_actuel,sommet), (sommet,suivant)]
                    augmentes[suivant]=False                    
                    sommets_atteignables[suivant] = nouveaux_atteignables                        
                    changement_effectue = True
    
        if changement_effectue == False:
            chemins[i] = []
            augmentes[i]=False
        else:
            augmentes[i]=True
                            

def find_path(y, marques):
    chemin = []
    while True:
        chemin.append(y[0])
        if y[1]==None:
            break
        for m in marques:
            if m[0] == y[1]:
                y = m
                break
    chemin.reverse()
    return chemin
    
def findFreeVertices(G,A,M,p):
    usedVertices = [e[p] for e in M]
    return [e for e in A if e not in usedVertices]

def findAugmentingPath(G,cycle,arete):
    #print arete
    marques = dfs(G, arete[0], arete[1], cycle)
    #print "fin dfs"
    marque = None
    for ((a,b,c),p) in marques:
        if b==arete[1]:
            marque = ((a,b,c),p)
    print marque
    if marque != None:
        print marques
        p = find_path(marque, marques)
        print p
        toreturn = []
        for e in p:
            toreturn.append((e[0],e[1]))
            toreturn.append((e[1], suivant_cycle(e[1], cycle)))
        return toreturn[:-1]+[arete]
        
def orderPath2(Se):
    S = list(Se)
    ordonne = []
    current = 0
    
    while True:
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
        if current == 0:
            break
        if not trouve:
            return []
    return ordonne
        
    
def replace(M,path,X,Y):
    for e in path:
        if path.index(e)%2 == 0:
            M.append(e)
        else:
            M.remove((e[1],e[0]))

def permute(l_m):
    l = copylist(l_m)
    toreturn = []
    for k in range(len(l)):
        i = randint(len(l))
        toreturn.append(l[i])
        l.remove(l[i])
    return toreturn
    
def randomcycle(n):
    l = list(range(n))
    toreturn = [0]*n
    current = 0
    for k in range(len(l)):
        if len(l)>1:
            i = randint(1,len(l))
        else:
            i=0
        toreturn[current]=l[i]
        current = l[i]
        l.remove(l[i])
    return toreturn

def randomhamiltongraph(n, nbaretes):
    G = []
    aretespossibles = []
    for i in range(n):
        for j in range(n):
            if i != j:
                aretespossibles.append((i,j))
                
    sigma = randomcycle(n)
    
    for i in range(n):
        G.append([])
    for k in range(n):
        G[k].append(sigma[k])
        G[sigma[k]].append(k)
        aretespossibles.remove((k,sigma[k]))
        aretespossibles.remove((sigma[k],k))
        
    #nbaretes = randint(n/2, n)
    for k in range(nbaretes):
        i = randint(len(aretespossibles))
        (a,b)=aretespossibles[i]
        G[a].append(b)
        G[b].append(a)
        aretespossibles.remove((a,b))
        aretespossibles.remove((b,a))
    #permutations des sommets de G pour perturber l'algo (choix du cycle
    #initial trivial sinon)
    for i in range(n):
        G[i] = permute(G[i])
    return G
    
def randomhamiltontrigraph(n):
    G = []
    aretespossibles = []
    for i in range(n):
        for j in range(n):
            if i != j:
                aretespossibles.append((i,j))
                
    sigma = randomcycle(n)
    
    for i in range(n):
        G.append([])
    for k in range(n):
        G[k].append(sigma[k])
        G[sigma[k]].append(k)
        aretespossibles.remove((k,sigma[k]))
        aretespossibles.remove((sigma[k],k))
    
    for i in range(n):
        nbaretes = 3
        possibles = []
        for j in range(n):
            if not j in G[i] and j!=i:
                possibles.append(j)
        for k in range(nbaretes-len(G[i])):
            p = randint(len(possibles))
            G[i].append(possibles[p])
            G[possibles[p]].append(i)
            possibles.pop(p)
        
    #permutations des sommets de G pour perturber l'algo (choix du cycle
    #initial trivial sinon)
    for i in range(n):
        G[i] = permute(G[i])
    return G
    
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
    
def hamilton(G):
    n = len(G)
    print "Graphe :", G
    cycle = []
    for i in range(n):
        cycle.append((i, (i+1)%n))
    print "Cycle :", cycle
    fini = False
    while not fini:
        fini = False
        cycleav = list(cycle)
        for (i,j) in cycle:
            if not j in G[i]:
                print (i,j)
                p = dfs(G, i, j, cycle)
                if p == None or p ==[]:
                    p = dfs(G,j,i,cycle)
                print "Chemin augmentant trouvé pour",(i,j),":",p
                if p!=None and p!=[]:
                    cycle.remove((i,j))
                    for k in range(len(p)):
                        if k%2 == 0:
                            cycle.append(p[k])
                        else:
                            cycle.remove(p[k])
                    print cycle
                    cycle = orderPath2(cycle)
                    print "cycle orderpath", cycle
                    reel = True
                    for (i,j) in cycle:
                        if not j in G[i]:
                            reel = False
                    if reel:
                        print "return effectue"
                        fini = True
                        return cycle
                    break
        if cycleav == cycle:
            return []
                        
    
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

def hamilton_bourrin(G):
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

for i in range(10):
    G = randomhamiltontrigraph(10)
    t = time.time()
    print ""
    print ""
    print ""
    print "---------NOUVEAU GRAPHE, numero", i
    print G
    l =  len(hamilton(G))
    print ""
    print ""
    print "Taille du chemin hamiltonien trouvé : ", l
    print "temps mis pour trouver la solution :", (time.time()-t)
    print ""
    print ""
    if l != 10:
        break

#G=[[2, 7, 4, 1], [8, 5, 0], [8, 0, 6], [7, 6, 5], [9, 7, 0], [1, 9, 3], [9, 2, 3], [3, 0, 4], [2, 9, 1], [6, 4, 5, 8]]
#print hamilton_bourrin(G)

#print len(hamilton(G))