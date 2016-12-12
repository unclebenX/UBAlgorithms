# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 12:47:45 2016

@author: uncleben
"""
#
#def reversePath(P):
#    P2 = []
#    for (i,j) in path:
#        P2.append()

def copyDoubleList(l):
    temp = []
    for e in l:
        ligne = []
        for x in e:
            ligne.append(x)
        temp.append(ligne)
    return temp
    
def verifHamilton(n, chemin):
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
    
def removeLastEdge(path, vertex):
    for (i,j) in path:
        if i == vertex:
            ind = path.index((i,j))
            path.remove((i,j))
            break
    for k in range(ind):
        (i,j) = path.pop(ind-k-1)
        path.append((j, i))
        
def findHamiltonian(G2):
    G = copyDoubleList(G2)
    inPath = [0, G[0][0]]
    path = [(0,G[0][0])]
    n = len(G)
    lim = 0
    while not verifHamilton(n, path) and lim<100:
        lim+=1
        print len(path), path
        enlarged = False
        for vertex in G[path[-1][1]]:
            if not vertex in inPath:
                inPath.append(vertex)
                path.append((path[-1][1],vertex))
                enlarged = True
                break
            if len(path) == n-1 and vertex==path[0][0]:
                path.append((path[-1][1], vertex))
                enlarged = True
                break
        if not enlarged:
            for vertex in G2[path[-1][1]]:
                if vertex in inPath and (not (vertex, path[-1][1]) in path):
                    if vertex != path[0][0]:
                        path.append((path[-1][1], vertex))
                        removeLastEdge(path, vertex)                        
                    else:
                        path.append((path[-1][1], vertex))
                        if len(path)!=n:
                            path.remove((path[0][0], path[0][1]))
                    break
    return path
    
def dijkstra(G, depart, arrivee):
    openlist = []
    closedlist = [depart]
    print closedlist
    def dijaux(s, poids):
        voisins = G[s]
        for v in voisins:
            if v == arrivee:
                closedlist.append(arrivee)
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
        posmin = 0
        poidsmin = openlist[0][1]
        for i in range(len(openlist)):
            if openlist[i][1] < poidsmin:
                posmin = i
                poidsmin = openlist[i][1]
        closedlist.append(openlist[posmin][0])
        openlist.remove(openlist[posmin])
        if openlist == []:
            for i in range(len(closedlist)):
                closedlist.pop(0)
            return
        dijaux(openlist[posmin][0], poidsmin)
    dijaux(depart, 0)
    return closedlist
                    

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
    
def copylist(l):
    temp = []
    for e in l:
        temp.append(e)
    return temp
    
def getClosure(G):
    n = len(G)
    G_closure = copyDoubleList(G)
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

G = randomhamiltongraph(10, 10)
print G
print dijkstra(G, 0, 11)

#G = [[9, 1], [0, 2, 7], [1, 3, 9], [4, 2, 6], [6, 3, 5], [4, 9, 6], [5, 7, 3, 4], [1, 6, 8], [7, 9], [2, 8, 0, 5]]
#G = [[2, 1, 5, 3, 7], [2, 0], [4, 1, 0, 5, 7, 6, 3], [0, 2, 4], [2, 3, 5], [0, 6, 2, 4], [2, 7, 5], [0, 6, 2]]

    