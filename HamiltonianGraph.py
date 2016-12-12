# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:13:25 2016

@author: benjamin
"""

import numpy as np

def randomHamiltonianGraph(n):
    #Generates a random hamiltonian graph of size n, with all vertices with degree
    #lower than 3, and hamiltonian cycle [0,1,2,...,n,0]
    G = [[] for i in range(n)]
    for i in range(n):
        G[i].append((i+1)%n)
        G[i].append((i-1)%n)
    for k in range(n):
        vertex = randint(0,n-1)
        if vertex not in G[k] and k!=vertex and len(G[k])<3 and len(G[vertex])<3:
            G[k].append(vertex)
            G[vertex].append(k)
    perm = np.random.permutation(n)
    for i in range(n):
        for j in range(len(G[i])):
            G[i][j] = perm[G[i][j]]
    G2 = [None for i in range(n)]
    for i in range(n):
        G2[perm[i]] = G[i]
    return G2
    
def deleteEdge(G, i, j):
    if j in G[i]:
        G[i].remove(j)
    if i in G[j]:        
        G[j].remove(i)

def deleteAllEdges(G,i):
    for j in range(len(G)):
        deleteEdge(G,i,j)
    
def killEdge(G, reachedVertices):
    for v in reachedVertices:
        if len(G[v])>=2:
            v1 = G[v].pop(1)
            print "Deleted ", (v, v1)
            return
        
def build(G):
    n = len(G)
    selectedEdges = []
    doubledVertices = []
    reachedVertices = []
    k=0
    while len(selectedEdges) < n and k < 15:
        didSomething = False
        for i in range(n):
            if len(G[i]) == 2:
                v1, v2 = G[i][0], G[i][1]
                if (i,v1) not in selectedEdges and (i,v2) not in selectedEdges and i not in doubledVertices and i not in reachedVertices:                  
                    selectedEdges.append((i,v1))
                    selectedEdges.append((i,v2))
                    reachedVertices += [i,v1,v2]
                    deleteAllEdges(G,i)
                    doubledVertices.append(i)
                    deleteEdge(G,i,v1)
                    deleteEdge(G,i,v2)
                    didSomething = True
                if (i,v1) not in selectedEdges and i in reachedVertices and v1 in reachedVertices:
                    deleteEdge(G,i,v1)
                    print "Deleted from 2 ", (i,v1), reachedVertices
                    didSomething = True
                    break
                if (i,v2) not in selectedEdges and i in reachedVertices and v2 in reachedVertices:
                    deleteEdge(G,i,v2)
                    print "Deleted from 2.1 ", (i,v2), reachedVertices
                    didSomething = True
                    break
            if didSomething:
                break
            if len(G[i]) == 1:
                v1 = G[i][0]
                if (i,v1) not in selectedEdges and i in reachedVertices and v1 not in reachedVertices:
                    selectedEdges.append((i,v1))
                    deleteAllEdges(G,i)
                    doubledVertices.append(i)
                    reachedVertices.append(v1)
                    didSomething = True
                if (i,v1) not in selectedEdges and len(selectedEdges) == n-1:
                    selectedEdges.append((i,v1))
                    didSomething = True
            print selectedEdges, doubledVertices, reachedVertices, i
        if not didSomething:
            killEdge(G, reachedVertices)
        k+=1
    return True, len(selectedEdges)==n, selectedEdges

#G = randomHamiltonianGraph(6)
G = [[1, 2, 5], [3, 0], [0, 4, 3], [5, 1, 2], [2, 5], [4, 3, 0]]

print G
s = build(G)
print s
        