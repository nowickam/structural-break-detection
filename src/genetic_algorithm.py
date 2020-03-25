import random as rand
import math
import numpy as np

SIZE = 200
n = 1500    #length of the data
chromosones=[]
p=3         #AR order, later random
rand.seed(0)

#Objective function
def MDL(parameter_tuple):
    print(parameter_tuple)
    return 22

#parameters usable by MDL function
def make_mdl_parameters(m,chromosone):
    breakpoints=[]
    for i in range(len(chromosone)):
        if chromosone[i]!=-1:
            breakpoints.append((i,chromosone[i]))
    return (m,breakpoints)

#Map parameters onto a chromosone
def make_chromosone(m):
    #fill with -1
    chromosone=np.full((1,n),-1)[0]
    #mark m genes with p AR order
    for i in range(m):
        j=int(rand.uniform(0,n))
        while(chromosone[j]!=-1):
            j=int(rand.uniform(0,n))
        chromosone[j]=p
    mdl=MDL(make_mdl_parameters(m,chromosone))
    return (mdl,chromosone)

#Start with an initial set of chromosomes
def generate_chromosones():
    chromosones = []
    for i in range(SIZE):
        #number of breaks
        m=int(rand.uniform(1,100))
        chromosones.append(make_chromosone(m))
    return chromosones

#Apply objective function to an individual
def apply_function(chromosone):
    #pseudo
    size=chromosone.m
    parameters=chromosone.list_of_ti_pi
    return MDL(size,parameters)

#Sort according to the values of objective function (ascending)
def sort_chromosones(chromosones):
    return

#Parent chromosomes are randomly selected (proportional to the rank of their objective function values)
#Can choose one chromosone for mutation or two for crossover
def random_choice(sorted_chromosones):
    return

#Produce offspring by taking genes (parameters of MDL function) from both parents at random 
def crossover(parent_1, parent_2):
    return

#Produce offspring by: taking a gene from parent || changing own gene
def mutation(parent):
    return

def make_next_generation(previous_chromosones):
    return

print(generate_chromosones())