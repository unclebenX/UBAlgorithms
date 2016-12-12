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
    
def imp_dfs(G,i):
    marques = []
    peres = []
    def dfs_aux(j,G,marques,dad):
        marques.append(j)
        peres.append(dad)
        for e in G[j]:
            if e not in marques:
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
    
"""
l=[2,4,5,3]
l2 = [3,3,5,5]
print find_path(2,l,l2)
"""

def findFreeVertices(G,A,M,p):
    usedVertices = [e[p] for e in M]
    return [e for e in A if e not in usedVertices]
    
def nbSommetsAtteignables(sommet, M, G):
    def auxnb(s, l):
        l2 = l+[s]
        res = 1
        for e in G[s]:
            if (not e in l):
                res += auxnb(e, l2)
        return res
    s = sommet[0]
    l = [e[1] for e in M]
    return auxnb(s, l)
    


def findAugmentingPath(G,X,Y,M, M_sauv):
    G2 = decisionGraph(G,X,Y,M)
    V1 = findFreeVertices(G,X,M,0)
    V2 = findFreeVertices(G,Y,M,1)
    p=None
    for v1 in V1:
        marques, peres = imp_dfs(G2,v1)
        for v2 in V2:
            if v2 in marques:
                p = find_path(v2,marques,peres)
                tempM = copylist(M)
                replace(tempM,p,X,Y)
                if len(tempM)==len(G)/2:
                    return copylist(tempM)
                chemin = perm(v1, G, tempM)
                
                print "graphe1 : "+str(G)
                print "M1 : "+str([(i+1, j+1-len(G)/2) for (i,j) in tempM])                
                
                maxi = 0
                todestroy = None
                for sommet in chemin:
                    n = len(G[sommet[0]])
                    if n >= maxi:
                        maxi = n
                        todestroy = sommet
                if todestroy != None:
                    print todestroy
                    G[todestroy[0]].remove(todestroy[1])
                    tempM.remove(todestroy)
                    
                print chemin
                print "graphe : "+str(G)
                print "M : "+str([(i+1, j+1-len(G)/2) for (i,j) in tempM])
                return copylist(tempM)
    
def replace(M,path,X,Y):
    for i in range(len(path)):
        e = path[i]
        if i%2 == 0:
            if not e in M:
                M.append(e)
        else:
            M.remove((e[1],e[0]))
        
    
def HopcroftKarp(G,X,Y):
    M = []
    M_sauv = []
    p = findAugmentingPath(G,X,Y,M, M_sauv)
    i=0
    while True:
        i+=1
        K = findAugmentingPath(G,X,Y,M, M_sauv)
        if K ==None:
            break
        else:
            M = list(K)
    return M

def randomSetMatrix(n):
    M = []
    for i in range(n):
        L = []
        for j in range(n):
            a = random.randint(1,100)
            if a>90:
                L.append(1)
            else:
                L.append(0)
        M.append(L)
    return M
    
def matrixToGraph(M):
    n = len(M)
    l = [[] for i in range(2*n)]
    for i in range(n):
        for j in range(n):
            if M[i][j]==1:
                l[i].append(j+n)
    return l,n
    
def solveHKarpMatrix(M):
    G,n = matrixToGraph(M)
    X = range(n)
    Y = range(n,2*n)
    return HopcroftKarp(G,X,Y)
  
"""  
G = [[3,4],[3],[5,4],[],[],[]]
X = [0,1,2]
Y = [3,4,5]
print HopcroftKarp(G,X,Y)
"""

"""
M = randomSetMatrix(100)
printMatrix(M)
S = solveHKarpMatrix(M)
print S, len(S)
"""

def randomMatrix(n,ma):
    M = []
    for i in range(n):
        l = []
        for j in range(n):
            l.append(randint(1,ma))
        M.append(l)
    return M

def printMatrix(M):
    for l in M:
        s = ""
        for e in l:
            s+=str(e)+" "
        print s

#printMatrix(randomMatrix(17,10))

def sortMatrixBase(M,ma):
    n = len(M)
    L = [[] for i in range(ma)]
    for i in range(n):
        for j in range(n):
            L[M[i][j]].append((i,j))
    return [L[i][j] for i in range(ma) for j in range(len(L[i]))]
    
def sortMatrix(M):
    L = []
    for i in range(len(M)):
        for j in range(len(M[i])):
            L.append((i,j,M[i][j]))
    def ordre((a,b,c), (a1,b1,c1)):
        if c < c1:
            return -1
        elif c == c1:
            return 0
        else:
            return 1
    L.sort(cmp=ordre)
    return [(i,j) for (i,j,k) in L]
    
def solveMatrix(M):
    n = len(M)
    L = sortMatrix(M)
    print L
    graphe = [[] for i in range(2*n)]
    for k in range(n):
        (i,j)=L.pop(0)
        graphe[i].append(n+j)
    boo = True
    while True:
        X = range(n)
        Y = range(n,2*n)
        G = copydoublelist(graphe)
        Mat = HopcroftKarp(G,X,Y)
        if len(Mat)==n:
            break
        (i,j)=L.pop(0)
        graphe[i].append(n+j)
        print "MATRICE" + str([(i+1,j+1-n) for (i,j) in Mat])
        print graphe
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
    
#Pour vérifier qu'il n'y a pas de boucle
def perm(depart, G, M):
    P = [0]*len(G)
    for e in M:
        P[e[0]]=(e[1])
    current = depart
    perm = []
    while True:
        if P[current]%(len(G)/2) == depart:
            return perm+[(current, P[current])]
        s = P[current]
        P[current] = 0
        perm.append((current, s))
        current = s%(len(G)/2)
        if P[current]==0:
            return []
            

def calculeSomme(M,S,n):
    somme = 0    
    for k in range(n):
        (i,j) = S[k]
        somme+=M[i][j]
    return somme

#print calculeSomme(M,S,n)

def printSolvedMatrix(M, S):
    n = len(M)
    for i in range(n):
        s = ""
        for j in range(n):
            if (i,j) in S:
                s+= "  "
            else:
                s+=str(M[i][j])+" "
        print s
        
#printSolvedMatrix(M, S)
        
I = 10000

def voyageurDeCommerce(M):
    n = len(M)
    S = solveMatrix(M)
    return S

M2 = [[I, 1, I, I, 1],[1,I,1,1,I],[I,1,I,1,I],[I, 1, 1, I, 1],[1, 1, I, I, I]]

Res = voyageurDeCommerce(M2)
print [(i+1,j+1) for (i,j) in Res]