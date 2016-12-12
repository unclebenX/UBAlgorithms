# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:55:20 2016

@author: uncleben
"""

from random import *

def isConnected(G):
    n = len(G)
    visitedVertices = [i == 0 for i in range(n)]
    queue = G[0]
    while queue!=[]:
        vertex = queue.pop()
        visitedVertices[vertex] = True
        for adjacentVertex in G[vertex]:
            if not visitedVertices[adjacentVertex]:
                queue.append(adjacentVertex)
    return not (False in visitedVertices)

def deleteEdge(G, i, j):
    if j in G[i]:
        G[i].remove(j)
    if i in G[j]:        
        G[j].remove(i)
    
def addEdge(G,i,j):
    if j not in G[i]:
        G[i].append(j)
    if i not in G[j]:
        G[j].append(i)
        
def isHamiltonian(growingPath):
    for e in growingPath:
        if len(e) != 2:
            return False
    return True

def edgeKiller(G):
    n = len(G)
    removed = False
    while not isHamiltonian(G):
        for i in range(n):
            if removed:
                break
            for j in range(len(G[i])):
                error = False
                for k in range(n):
                    deleteEdge(G,i,j)
                    for l in range(len(G[k])):
                        if i!=k or (i==k and j!=l):
                            deleteEdge(G,k,l)
                            connected = isConnected(G)
                            addEdge(G,k,l)
                            if not connected:
                                error = True
                                break
                    print "Ended last loop" 
                    if error:
                        break
                if not error:
                    removed = True
                    deleteEdge(G,i,j)
                    print "removed edge", i, j
                    break

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
    return G
    
G = randomHamiltonianGraph(8)
print isConnected(G)
edgeKiller(G)
print isHamiltonian(G)
        
                