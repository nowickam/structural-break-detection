import random as rand
import math
import numpy as np

generations=50
SIZE = 20
n = 10    #length of the data
chromosones=[]
p=3         #AR order, later random
rand.seed(0)

# #Objective function
# def MDL(parameter_tuple):
#     #for now
#     return rand.uniform(0,10)

# #parameters usable by MDL function
# def make_mdl_parameters(m,chromosone):
#     breakpoints=[]
#     n=len(chromosone)
#     for i in range(n):
#         if chromosone[i]!=-1:
#             breakpoints.append((i,chromosone[i]))
#     return (m,n,breakpoints)

#Map parameters onto a chromosone
def make_chromosone(m):
    #fill with n -1
    chromosone=np.full((1,n),-1)[0]
    #mark m genes with p AR order
    for i in range(m):
        j=int(rand.uniform(0,n))
        while(chromosone[j]!=-1):
            j=int(rand.uniform(0,n))
        chromosone[j]=p
    mdl=apply_function(m,chromosone)
    return (mdl,chromosone)

#Start with an initial set of chromosomes
def make_first_generation():
    chromosones = []
    for i in range(SIZE):
        #various number of breaks
        m=int(rand.uniform(1,n/2))
        chromosones.append(make_chromosone(m))
    return chromosones

#Apply objective function to an individual
def apply_function(m,chromosone):
    mdl=MDL(make_mdl_parameters(m,chromosone))
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
def crossover(parent_1, parent_2):
    m=int(rand.uniform(1,n/2))
    chromosone=[]

    for i in range(n):
        choice=rand.uniform(0,1)
        if choice < 0.5:
            chromosone.append(parent_1[1][i])
        else:
            chromosone.append(parent_2[1][i])

    mdl=apply_function(m,chromosone)
    return (mdl,chromosone)

#Produce offspring by: taking a gene from parent || changing own gene
def mutation(parent):
    m=int(rand.uniform(1,n/2))
    chromosone=[]
    pi1=rand.uniform(0,1)
    pi2=rand.uniform(0,1-pi1)

    for i in range(n):
        choice=rand.uniform(0,1)
        if choice < pi1:
            chromosone.append(parent[1][i])
        elif choice<pi1+pi2:
            chromosone.append(-1)
        else:
            chromosone.append(p)

    mdl=apply_function(m,chromosone)
    return (mdl,chromosone)

def make_next_generation(previous_chromosones):
    next_generation=[]
    sorted_chromosones=sort_chromosones(previous_chromosones)
    pi=rand.uniform(0,1)

    for i in range(SIZE):
        choice=rand.uniform(0,1)
        if(choice<pi):
            parent_1=random_choice(sorted_chromosones)
            parent_2=random_choice(sorted_chromosones)
            while parent_1==parent_2:
                parent_2=random_choice(sorted_chromosones)
            next_generation.append(crossover(parent_1,parent_2))
        else:
            parent=random_choice(sorted_chromosones)
            next_generation.append(mutation(parent))
    return next_generation

chromosones=make_first_generation()
print(chromosones)
print("\n")

i=1 
while i<generations:
    print("GENERATION ",i)
    
    sorted_chromosones=sort_chromosones(chromosones)

    for gene in chromosones:
        print(gene)
    print("\n")
    chromosones=make_next_generation(chromosones)
    i+=1


