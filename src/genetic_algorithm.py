import random as rand
import math
import numpy as np

from .mdl import *

MAX_M = 20
TAB = 8
NEXT_GEN = 10
AR_ORDER_MAX = 4


# Map parameters onto a chromosome
def make_chromosome(n, m, data):
    p = int(rand.uniform(1,AR_ORDER_MAX+1))
    # fill with n -1
    chromosome = {}
    j_values = [0, n - 1]
    # first break at 0, last break at n
    chromosome[0]=p
    chromosome[n-1] = p
    # mark m genes with p AR order
    for i in range(m):
        p = int(rand.uniform(1,AR_ORDER_MAX+1))
        # breaks cannot be closer to themselves than the multiple of ar order
        search = True
        while search:
            search = False
            j = int(rand.uniform(0, n))
            # if there is break in this place
            if j not in chromosome:
                # if there is break in the surrounding
                for k in range(j-p-TAB, j+p+TAB):
                    if k in chromosome:
                        search = True
                        break
        j_values.append(j)

        chromosome[j] = p

    mdl_result = mdl(m, n, chromosome, data)
    return mdl_result, chromosome


# Start with an initial set of chromosomes
def make_first_generation(n, generation_size, data):
    chromosomes = []
    print("GENERATION 0")
    for i in range(generation_size):
        # various number of breaks
        m = int(rand.uniform(5, MAX_M))
        print("CHROMOSOME: ", i, "BREAKS: ", m)
        chromosomes.append(make_chromosome(n, m, data))
    return chromosomes
    

# Sort according to the values of objective function (ascending)
def sort_chromosomes(chromosomes):
    chromosomes.sort(key=lambda gene: gene[0])
    return chromosomes[:NEXT_GEN]


# Parent chromosomes are randomly selected (proportional to the rank of their objective function values)
# Can choose one chromosome for mutation or two for crossover
def random_choice(sorted_chromosomes):
    mdl_sum = 0
    probabilities = []

    # minimize the mdl depending on its sign
    if sorted_chromosomes[0][0]>0:
        for chromosome in sorted_chromosomes:
            mdl_sum += 1/chromosome[0]

        for chromosome in sorted_chromosomes:
            probabilities.append(1/chromosome[0]/mdl_sum)
    else:
        for chromosome in sorted_chromosomes:
            mdl_sum += chromosome[0]

        for chromosome in sorted_chromosomes:
            probabilities.append(chromosome[0]/mdl_sum)

    choice = rand.uniform(0, 1)
    j = 0
    acc = probabilities[j]

    while acc < choice:
        j += 1
        acc += probabilities[j]

    return sorted_chromosomes[j]


# Produce offspring by taking genes (parameters of MDL function) from both parents at random
def crossover(parent_1, parent_2, n, data):
    print("CROSSOVER")
    chromosome = {}
    breaks = 0

    # first break at 0
    p = int(rand.uniform(1,AR_ORDER_MAX+1))
    chromosome[0]=p
    # wait for order time for the next possible order
    wait = TAB*p

    # choose with pi probability, when there is no p close, p is in the beginning and the end
    for i in range(1, n-2):
        choice = rand.uniform(0, 1)

        p1 = parent_1[1].get(i, -1)
        p2 = parent_2[1].get(i, -1)

        if choice < 0.5 and wait <= 0 and i < n-2-p1-TAB:
            if p1 > -1:
                chromosome[i] = p1
                wait = p1+TAB*p1
        elif choice >= 0.5 and wait <= 0 and i < n-2-p2-TAB:
            if p2 > -1:
                chromosome[i] = p2
                wait = p2+TAB*p2
        wait -= 1
        if i in chromosome:
            breaks += 1

    # last break at n
    p = int(rand.uniform(1,AR_ORDER_MAX+1))
    chromosome[i] = p

    # print("BREAKS: ", breaks)
    mdl_result = mdl(breaks, n, chromosome, data)
    return mdl_result, chromosome


# Produce offspring by: taking a gene from parent || changing own gene
def mutation(parent, n, data):
    print("MUTATION")
    p = int(rand.uniform(1,AR_ORDER_MAX+1))    
    chromosome = {}
    pi1 = 0.9
    pi2 = 0.0999
    breaks = 0

    # first break at 0
    chromosome[0] = p
    wait = TAB*p

    for i in range(1, n-2):
        choice = rand.uniform(0, 1)
        if choice < pi1 and wait <= 0 and i < n-2-p-TAB:
            p = parent[1].get(i, -1)
            if p > -1:
                chromosome[i] = p
                wait = p+TAB*p
        elif choice > pi1+pi2 and wait <= 0 and i < n-2-p-TAB:
            p = int(rand.uniform(1,AR_ORDER_MAX+1))
            chromosome[i] = p
            wait = p+TAB*p
        wait -= 1
        if i in chromosome:
            breaks += 1

    # last break at n
    p = int(rand.uniform(1,5))
    chromosome[i] = p
    
    # print("BREAKS: ", breaks)
    mdl_result = mdl(breaks, n, chromosome, data)
    return mdl_result, chromosome


def make_next_generation(previous_chromosomes, n, generation_size, data, f, mdl_values):
    next_generation = []
    sorted_chromosomes = sort_chromosomes(previous_chromosomes)
    mdl_values.append(sorted_chromosomes[0][0])
    f.write("TOP: "+str(sorted_chromosomes[0][0])+"\n")
    # if there is just one chromosome repeating
    count = 0
    for chromosome in sorted_chromosomes:
        if chromosome[0] == sorted_chromosomes[0][0]:
            count += 1 
    if len(sorted_chromosomes) == count:
        f.write("FINISHED")
        return sorted_chromosomes

    # crossover probability
    pi = 0.75
    
    for i in range(generation_size):
        # print("CHROMOSOME: ", i)
        choice = rand.uniform(0, 1)
        if choice < pi:
            # choose two parents - until they are different
            parent_1 = random_choice(sorted_chromosomes)
            parent_2 = random_choice(sorted_chromosomes)
            while parent_1 == parent_2:
                parent_2 = random_choice(sorted_chromosomes)
            next_generation.append(crossover(parent_1, parent_2, n, data))
        else:
            parent = random_choice(sorted_chromosomes)
            next_generation.append(mutation(parent, n, data))

    return next_generation