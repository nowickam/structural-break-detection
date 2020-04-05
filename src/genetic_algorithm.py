import random as rand
import math
import numpy as np

from .mdl import *

MAX_M=20
#TODO randomize
AR_ORDER=3

#Map parameters onto a chromosone
def make_chromosone(n,m,data):
    p=AR_ORDER
    #fill with n -1
    chromosone=np.full((1,n),-1)[0]
    j_values=[]
    #first break at 0
    chromosone[0]=p
    #mark m genes with p AR order
    for i in range(m):
        #breaks cannot be closer to themselves than th ar order
        #j=int(rand.uniform(0,n))
        search=True
        while search:
            j=int(rand.uniform(0,n))
            if chromosone[j]==-1:
                for k in range(j-p-1,j+p+1):
                    if k in j_values:
                        j=int(rand.uniform(0,n))
                        break
                search=False
        j_values.append(j)

        chromosone[j]=p
    mdl=apply_function(m,chromosone,data)
    return (mdl,chromosone)

#Start with an initial set of chromosomes
def make_first_generation(n, generation_size, data):
    chromosones = []
    print("GENERATION 0")
    for i in range(generation_size):
        #various number of breaks
        m=int(rand.uniform(1,MAX_M))
        print("CHROMOSONE: ",i, "BREAKS: ",m)
        chromosones.append(make_chromosone(n,m,data))
    return chromosones

#Apply objective function to an individual
def apply_function(m,chromosone, data):
    mdl=MDL(make_mdl_parameters(m,chromosone),data)
    return mdl

#Sort according to the values of objective function (ascending)
def sort_chromosones(chromosones):
    chromosones.sort(key=lambda gene: gene[0])
    return chromosones[:10]

#Parent chromosomes are randomly selected (proportional to the rank of their objective function values)
#Can choose one chromosone for mutation or two for crossover
def random_choice(sorted_chromosones):
    mdl_sum=0

    for chromosone in sorted_chromosones:
        mdl_sum+=1/chromosone[0]

    probabilities=[]

    for chromosone in sorted_chromosones:
        probabilities.append(1/chromosone[0]/mdl_sum)

    choice=rand.uniform(0,1)
    j=0
    acc=probabilities[j]

    while acc<choice:
        j+=1
        acc+=probabilities[j]

    return sorted_chromosones[j]

#Produce offspring by taking genes (parameters of MDL function) from both parents at random 
def crossover(parent_1, parent_2,n,data):
    m=int(rand.uniform(1,MAX_M))
    chromosone=[]
    #wait for order time for the next possible order 
    wait=0

    #choose with pi probability, when there is no p close, p is in the beginning and the end
    for i in range(n):
        choice=rand.uniform(0,1)
        p1=parent_1[1][i]
        p2=parent_2[1][i]
        if choice < 0.5 and wait<=0 and i<n-p1 and i>p1:
            chromosone.append(p1)
            wait=p1+1
        elif choice >= 0.5 and wait<=0 and i<n-p2 and i>p2:
            chromosone.append(p2)
            wait=p2+1
        else:
            chromosone.append(-1)
        wait-=1

    mdl=apply_function(m,chromosone,data)
    return (mdl,chromosone)

#Produce offspring by: taking a gene from parent || changing own gene
def mutation(parent,n,data):
    p=AR_ORDER
    m=int(rand.uniform(1,MAX_M))
    chromosone=[]
    pi1=rand.uniform(0,1)
    pi2=rand.uniform(0,1-pi1)
    wait=0

    for i in range(n):
        choice=rand.uniform(0,1)
        if choice < pi1 and wait<=0 and i<n-p and i>p:
            chromosone.append(parent[1][i])
            wait=parent[1][i]+1
        elif choice>pi1+pi2 and wait<=0 and i<n-p and i>p:
            chromosone.append(p)
            wait=p+1
        else:
            chromosone.append(-1)
        wait-=1

    mdl=apply_function(m,chromosone,data)
    return (mdl,chromosone)

def make_next_generation(previous_chromosones,n,generation_size, data):
    next_generation=[]
    sorted_chromosones=sort_chromosones(previous_chromosones)
    pi=rand.uniform(0,1)

    for i in range(generation_size):
        choice=rand.uniform(0,1)
        if(choice<pi):
            #choose two parents - until they are different
            parent_1=random_choice(sorted_chromosones)
            parent_2=random_choice(sorted_chromosones)
            while parent_1==parent_2:
                parent_2=random_choice(sorted_chromosones)
            next_generation.append(crossover(parent_1,parent_2,n,data))
        else:
            parent=random_choice(sorted_chromosones)
            next_generation.append(mutation(parent,n,data))
    return next_generation

