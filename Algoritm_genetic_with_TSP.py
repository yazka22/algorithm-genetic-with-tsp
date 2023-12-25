# -*- coding: utf-8 -*-
"""
Created on Tue May  3 19:17:42 2022

@author: Yazka
"""

import numpy as np
import random as rd
import matplotlib.pyplot as plt


def countlen(chromo, distance, cityNum):
    lenth = 0
    for iii in range(cityNum - 1):
        lenth += distance[chromo[iii]][chromo[iii + 1]]
    lenth += distance[chromo[cityNum - 1]][chromo[0]]  
    return lenth

def crepopula(cityNum, M):
    popula = []  
    for ii in range(M):
        chromo = np.random.permutation(cityNum).tolist()   
        popula.append(chromo)
    return popula


def countprobabily(popula,distance,cityNum):
    evall = []
    for chromo in popula:
        eval = max(30000 - countlen(chromo, distance,cityNum),0)  
        evall.append(eval)
    seval = sum(evall)
    probabil = evall/seval   
    probabily = probabil.copy()
    for i in range(1,len(popula)):
        probabily[i]=probabily[i]+probabily[i-1]  
    return probabily


def lpd(popula,probabily,M):
    newpopula=[]
    for i in range(M):
        proba = rd.random()
        for ii in range(len(probabily)):
            if probabily[ii] >= proba:
                selechromo = popula[ii]
                break
        newpopula.append(selechromo)
    return newpopula

def crossover_nn(father1, father2,cityNum,distance):
    father_1 = father1.copy()
    father_2 = father2.copy()
    city0 = rd.randint(0, cityNum-1)  
    son = [city0]
    while len(son) < len(father1):
        ord1 = father_1.index(city0)
        ord2 = father_2.index(city0)
        if ord1 == len(father_1)-1 :
            ord1 = -1
        if ord2 == len(father_1)-1 :
            ord2 = -1
        city1 = father_1[ord1 + 1]
        city2 = father_2[ord2 + 1]
        father_1.remove(city0)
        father_2.remove(city0)
        if distance[city0][city1] <= distance[city0][city2]:
            son.append(city1)
            city0 = city1
        else:
            son.append(city2)
            city0 = city2
    return son


import itertools
def variat2(father,cityNum,distance):
    or1 = rd.randint(0, cityNum - 1) 
    or2 = rd.randint(0, cityNum - 1)
    or3 = rd.randint(0, cityNum - 1)
    or4 = rd.randint(0, cityNum - 1)
    or5 = rd.randint(0, cityNum - 1)
    nosame = list(set([or1, or2, or3, or4, or5]))
    ords = list(itertools.permutations(nosame, len(nosame)))
    sons = []               
    sonn = father.copy()
    for ord in ords:
        for ii in range(len(nosame)):
            sonn[nosame[ii]] = father[ord[ii]]
        sons.append(sonn)
    son_leng = []       
    for sonn in sons:
        leng = countlen(sonn, distance, cityNum)
        son_leng.append(leng)
    n = son_leng.index(min(son_leng))   
    return sons[n]


def main():
    M = 10  
    cityNum = 52  
    
    cities = [[565, 575],[25, 185],[345, 750],[945, 685],[845, 655],[880, 660],[25, 230],[525, 1000],[580, 1175],
              [650, 1130],[1605, 620],[1220, 580],[1465, 200],[1530, 5],[845, 680],[725, 370],[145, 665],[415, 635],
              [510, 875],[560, 365],[300, 465],[520, 585],[480, 415],[835, 625],[975, 580],[1215, 245],[1320, 315],
              [1250, 400],[660, 180],[410, 250],[420, 555],[575, 665],[1150, 1160],[700, 580],[685, 595],[685, 610],
              [770, 610],[795, 645],[720, 635],[760, 650],[475, 960],[95, 260],[875, 920],[700, 500],[555, 815],
              [830, 485],[1170, 65],[830, 610],[605, 625],[595, 360],[1340, 725],[1740, 245]]
   
    distance = np.zeros([cityNum,cityNum])
    for i in range(cityNum):
        for j in range(cityNum):
            distance[i][j] = pow((pow(cities[i][0]-cities[j][0],2)+pow(cities[i][1]-cities[j][1],2)),0.5)

    popula = crepopula(cityNum, M)

    for n in range(600):  
       
        pc = 0.8  
        pv = 0.25  
        son = []
        
        crossgroup = []
        for i in range(M):
            cpb = rd.random()
            if cpb < pc:
                crossgroup.append(popula[i])
        if len(crossgroup) % 2 == 1:  
            del crossgroup[-1]
        if crossgroup != []:  
            for ii in range(0, len(crossgroup), 2):
                sonc = crossover_nn(crossgroup[ii], crossgroup[ii + 1], cityNum, distance)
                son.append(sonc)
      
        variatgroup = []
        for j in range(M):
            vpb = rd.random()
            if vpb < pv:  
                variatgroup.append(popula[j])

        if variatgroup != []:
            for vag in variatgroup:
                sonv = variat2(vag, cityNum, distance)  
                son.append(sonv)

        
        populapuls = popula + son
        probabily = countprobabily(populapuls, distance, cityNum)

        
        popula = lpd(populapuls, probabily, M)

    
    opt_chr = popula[0]
    opt_len = countlen(popula[0], distance, cityNum)
    for chr in popula:
        chrlen = countlen(chr, distance, cityNum)
        if chrlen < opt_len:
            opt_chr = chr
            opt_len = chrlen
    print("Mod optim:" + str(opt_chr))
    print("Valoare optimă:" + str(opt_len))

    
    for cor in range(len(opt_chr)-1) :
        x = [cities[opt_chr[cor]][0],cities[opt_chr[cor+1]][0]]
        y = [cities[opt_chr[cor]][1],cities[opt_chr[cor+1]][1]]
        plt.plot(x,y,"b-")
    plt.show()

if __name__ =="__main__":
    main()