# -*- coding: utf-8 -*-

import numpy as np

def Approx_Beta(vals,N):
    inter = .001
    prop = 1./(len(vals))-inter
    b = True
    while b:
        prop+=inter
        vals2 = list(vals)
        #print prop
        try:
            Appel_calcul(vals2,N,prop)
        except:
            b = False
    return prop

def Appel_calcul(vals,N,prop):
    parts = [(i/(N+0.), (i+1.)/N) for i in range(N)]
    n=len(vals)
    Calcul_rec(vals,parts,n,prop,N,n)
    
def Calcul_rec(vals, parts, n, prop, N, n_initial):
    if n!=1:
        """ trie la liste des [parts,joueur,vals] en fonction de l'écart entre le premier sur la part et le second """
        liste_triee = tri(parts, vals)
        """ Balance le joueur et les parts qu'il doit recevoir selon le protocole """
        joueur, part_joueur, valuation, indice_premier = allocation(liste_triee,prop,n,n_initial,N)
        """S'il ne restait qu'un joueur, l'algorithme est terminé"""
        """Sinon, on reprend avec les parts restantes après épuration"""
        new_list=epure(liste_triee, part_joueur)
        vals.pop(indice_premier)
        """print joueur, valuation"""
        Calcul_rec(vals, new_list, n-1, prop, N, n_initial)
    else:
        c = calcul_dernier(vals[0][0],prop,N,parts)
        if not c:
            raise('FatError')
        
def calcul_dernier(fonction,prop,N,parts):
    integrande=0
    for l in parts:
        integrande+=fonction(l[0])/N
    return integrande > prop

        
def comp((a,b,c,d,x),(e,f,g,h,y)):
    if d < h:
        return 1
    if d==h:
        return 0
    return -1
    
def somme(l):
    S = 0.
    for e in l:
        S+=e
    return S
        
def tri(parts,vals):
    l = []
    nombre_parts = len(parts)
    for i in range(nombre_parts):
        valeur_sur_part = [vals[j][0](parts[i][1]) for j in range(len(vals))]
        indice_premier = np.argmax(valeur_sur_part)
        num_premier = vals[indice_premier][1]
        valeur_premier = valeur_sur_part[indice_premier]
        ecart = valeur_premier/somme(valeur_sur_part)
        l.append([parts[i],num_premier,valeur_premier,ecart,indice_premier])
    l.sort(comp)
    return l
    
def epure(liste_triee, part_joueur):
    """
    Liste_triée:
    part, valeur, joueur, écart
    """
    new_list=[]
    for part in [liste_triee[i][0] for i in range(len(liste_triee))]:
        if part not in part_joueur:
            new_list.append(part)
    return new_list

def allocation(liste_triee,prop,n,n_initial,M):
    integrande=[0 for i in range(n_initial)]
    liste_part=[[] for i in range(n_initial)]
    for l in liste_triee:
        integrande[l[1]]+=l[2]/M
        liste_part[l[1]].append(l[0])
        if integrande[l[1]]>prop:
            return l[1],liste_part[l[1]],integrande[l[1]],l[4]
            #Renvoie le joueur, et sa liste de parts.
            

vals = [[v1,0],[v2,1],[v3,2],[v4,3],[v5,4]]
print Approx_Beta(vals, 10000)
