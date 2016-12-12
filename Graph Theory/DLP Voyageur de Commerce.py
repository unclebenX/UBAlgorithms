# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:23:45 2015

@author: uncleben

Hopcroft-Karp - 2e version

Algorithme de Hopcroft-Karp pour la recherche d'un
couplage dans un graphe bipartite - ie
d'une allocation combinatoire équitable.

G : graphe sous la forme d'une matrice ; chaque ligne
contient la liste des sommets reliés à un autre sommet.

M est un matching : liste de tuples.
"""

import random

def decisionGraph(G,X,Y,M):
    G2 = list(G)
    for i in range(len(G2)):
        if i not in X:
            G[i]=[]
    for e in M:
        G2[e[1]]=[e[0]]
    return G2
#    
#def imp_dfs(G,i):
#    marques = []
#    peres = []
#    def dfs_aux(j,G,marques,dad):
#        marques.append(j)
#        peres.append(dad)
#        for e in G[j]:
#            if e not in marques:
#                dfs_aux(e,G,marques,j)        
#    dfs_aux(i,G,marques,i)
#    return marques, peres

def imp_dfs(G,i):
    n = len(G)
    marques = []
    peres = []
    def dfs_aux(j,G,marques,dad,aretes,parite):
        marques.append(j)
        peres.append(dad)
        for e in G[j]:
            if e not in marques:
                if parite == 0:
                    if not (j,e) in aretes:
                        dfs_aux(e,G,marques,j,aretes+[(e-n,j+n)],(parite+1)%2)
                if parite != 0:
                    dfs_aux(e,G,marques,j,aretes,(parite+1)%2)
    dfs_aux(i,G,marques,i,[],0)
    return marques, peres

def find_path(y, marques, peres):
    sommets = []
    while peres[marques.index(y)]!=y:
        sommets.append((peres[marques.index(y)],y))
        y = peres[marques.index(y)]
    sommets.reverse()
    return sommets
    
"""
l=[2,4,5,3]
l2 = [3,3,5,5]
print find_path(2,l,l2)
"""

def findFreeVertices(G,A,M,p):
    usedVertices = [e[p] for e in M]
    return [e for e in A if e not in usedVertices]

def findAugmentingPath(G,X,Y,M):
    G2 = decisionGraph(G,X,Y,M)
    V1 = findFreeVertices(G,X,M,0)
    V2 = findFreeVertices(G,Y,M,1)
    p=None
    for v1 in V1:
        marques, peres = imp_dfs(G2,v1)
        for v2 in V2:
            if v2 in marques:
                p = find_path(v2,marques,peres)
                return p
    
def replace(M,path,X,Y):
    for e in path:
        if path.index(e)%2 == 0:
            M.append(e)
        else:
            M.remove((e[1],e[0]))
        
    
def HopcroftKarp(G,X,Y):
    M = []
    n = len(G)/2
    p = findAugmentingPath(G,X,Y,M)
    while p!=[] and p!=None:
        replace(M,p,X,Y)
        G2 = copydoublelist(G)
        for (i,j) in M:
            G2[j-n].remove(i+n)
        p = findAugmentingPath(G2,X,Y,M)
    return M
    
def solveMatrix(M,ma):
    n = len(M)
    L = sortMatrix(M,ma)
    graphe = [[] for i in range(2*n)]
    for k in range(n):
        (i,j)=L.pop(0)
        graphe[i].append(n+j)
    boo = True
    while boo:
        X = range(n)
        Y = range(n,2*n)
        Mat = HopcroftKarp(graphe,X,Y)
        if len(Mat)==n:
            boo = True
            break
        (i,j)=L.pop(0)
        graphe[i].append(n+j)
    Mat2 = [(i,j-n) for (i,j) in Mat]
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

def hopcroftgraph(G2):
    G = []
    n = len(G2)
    for i in range(len(G2)):
        G.append([])
        for j in range(len(G2[i])):
            G[i].append(G2[i][j]+n)
    for i in range(n):
        G.append([])
    H = HopcroftKarp(G, list(range(n)), list(range(n, 2*n)))
    M = [(i,j-n) for (i,j) in H]
    cycles = trouveCycles(M)
    return cycles

def trouveCycles(match2):
    l = []
    match = list(match2)
    while match != []:
        cycle = orderPath(match)
        l.append(cycle)
        for e in cycle:
            match.remove(e)
    return l
        
    
def orderPath(path2):
    path = list(path2)
    if path == []:
        return []
    def orderaux(reste, depart):
        for (i,j) in reste:
            if i == depart:
                reste.remove((i,j))
                return [(i,j)]+orderaux(reste,j)
        return []
    return orderaux(path, path[0][0])
                
    
    
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
        i = randint(len(aretespossibles))
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
            i = randint(len(l))
            toreturn.append(l[i])
            l.remove(l[i])
        return toreturn
    for i in range(n):
        G[i] = permute(G[i])
    return G
    
def hamilton(G2):
    G = copydoublelist(G2)
    n = len(G)
    lim = 0
    aretes = []    
    
    H = hopcroftgraph(G)
    if len(H)==1:
        return H
    
    while True and lim < 100:
        for cycle in H:
            for (i,j) in cycle:
                G[i].remove(j)
                G[j].remove(i)
                H = hopcroftgraph(G)
                if sum([len(e) for e in H])!=n:
                    G[i].append(j)
                    G[j].append(i)
                lim+=1
        if len(H)==1:
            return H
    return H
        
        
    
G = randomhamiltongraph(100, 100)
H = hamilton(G)
print H, len(H[0]), len(H)
