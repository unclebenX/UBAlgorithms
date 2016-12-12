# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:30:58 2016

@author: benjamin
Hamiltonian Circuit Finder
Runs in O(n^5)
"""

import numpy as np
from random import randint, shuffle, random

def dijkstra(G, start, end):
    def findMin(distances, vertices):
        minVal = distances[vertices[0]]
        minIndex = vertices[0]
        for v in vertices:
            if distances[v] < minVal:
                minVal = distances[v]
                minIndex = v
        return minIndex
    n = len(G)
    distances = [(n+1) for i in range(n)]
    distances[start] = 0
    vertices = range(n)
    previousVertex = [None for i in range(n)]
    while vertices!=[]:
        minVertex = findMin(distances, vertices)
        vertices.remove(minVertex)
        for vertex in G[minVertex]:
            if distances[vertex] > distances[minVertex] + 1:
                distances[vertex] = distances[minVertex] + 1
                previousVertex[vertex] = minVertex
    path = []
    currentVertex = end
    while currentVertex != start:
        path.append(previousVertex[currentVertex])
        currentVertex = previousVertex[currentVertex]
    return distances[end], path

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
    for i in range(n):
        if len(G2[i])>2:
            #G2[i][0], G2[i][1] = G2[i][1], G2[i][0]
    return G2
    
def diffGraph(G, cycle):
    n = len(G)
    dG = [[] for i in range(n)]
    for i in range(n):
        if cycle[i] == []:
            for j in G[i]:
                if cycle[j] == []:
                    dG[i].append(j)
    return dG

def findCycle(G):
    n = len(G)
    visitedVertices = [None for i in range(n)]
    visitedVertices[0] = True
    currentVertex = G[0][0]
    path = [(0, currentVertex)]
    previousVertex = 0
    while visitedVertices[currentVertex] != True:
        visitedVertices[currentVertex] = True
        """
        if G[currentVertex][0] == previousVertex:
            v = G[currentVertex][1]
        else:
            v = G[currentVertex][0]
        """
        v = G[currentVertex][0]
        path.append((currentVertex, v))
        previousVertex = currentVertex
        currentVertex = v
    while path[0][0] != currentVertex:
        path.pop(0)
    cycle = [[] for i in range(n)]
    for (i,j) in path:
        cycle[i].append(j)
        cycle[j].append(i)
    return cycle    
    
def findHCycle(G):
    n = len(G)
    currentCycle = findCycle(G)
    for i in range(n):
        for v1 in range(n):
            for v2 in range(n):
                if isHamiltonian(currentCycle):
                    print "broke", i
                    return currentCycle
                if currentCycle[v1] != [] and currentCycle[v2] != []:
                    dG = diffGraph(G, currentCycle)
                    print currentCycle, dG
                    l1, p1 = dijkstra(dG, v1, v2)
                    l2, p2 = dijkstra(currentCycle, v1, v2)
                    if l1 > l2:
                        for edge in p1:
                            currentCycle[edge[0]].remove(edge[1])
                            currentCycle[edge[1]].remove(edge[0])
                        for edge in p2:
                            currentCycle[edge[0]].append(edge[1])
                            currentCycle[edge[1]].append(edge[0])
                        break
    return currentCycle

def isHamiltonian(cycle):
    for e in cycle:
        if len(e)!=2:
            return False
    return True

count = 0    
for i in range(10000):
    k = randint(5, 10)
    G = randomHamiltonianGraph(k)
    H = findHCycle(G)
    val = isHamiltonian(H)
    #print G, H, val
    if val:
        count+=1
    if not val:
        print "ERRORRRRRR!!!"
        print G, H
print count