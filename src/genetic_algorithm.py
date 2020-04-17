import random as rand
import math
import numpy as np

from .mdl import *

MAX_M = 20
# TODO randomize
AR_ORDER = 1
TAB = 6
NEXT_GEN = 10


# Map parameters onto a chromosome
def make_chromosome(n, m, data):
    p = int(rand.uniform(1,5))
    # fill with n -1
    chromosome = np.full((1, n), -1)[0]
    j_values = [0, n - 1]
    # first break at 0
    chromosome[0] = p
    # mark m genes with p AR order
    for i in range(m):
        p = int(rand.uniform(1,5))
        # breaks cannot be closer to themselves than th ar order
        # j=int(rand.uniform(0,n))
        search = True
        while search:
            search = False
            j = int(rand.uniform(0, n))
            if chromosome[j] == -1:
                for k in range(j-p-TAB, j+p+TAB):
                    if k in j_values:
                        search = True
                        break
        j_values.append(j)

        chromosome[j] = p
    # last break at n
    chromosome[n-1] = p
    mdl_result = apply_function(m, chromosome, data)
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


# Apply objective function to an individual
def apply_function(m, chromosome, data):
    mdl_result = mdl(make_mdl_parameters(m, chromosome), data)
    return mdl_result


# Sort according to the values of objective function (ascending)
def sort_chromosomes(chromosomes):
    chromosomes.sort(key=lambda gene: gene[0])
    return chromosomes[:NEXT_GEN]


# Parent chromosomes are randomly selected (proportional to the rank of their objective function values)
# Can choose one chromosome for mutation or two for crossover
def random_choice(sorted_chromosomes):
    mdl_sum = 0

    for chromosome in sorted_chromosomes:
        mdl_sum += 1/chromosome[0]

    probabilities = []

    for chromosome in sorted_chromosomes:
        probabilities.append(1/chromosome[0]/mdl_sum)

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
    chromosome = []
    # wait for order time for the next possible order
    breaks = 0
    bias = 0.2

    # first break at 0
    p = int(rand.uniform(1,5))
    chromosome.append(p)
    wait = TAB*p

    # choose with pi probability, when there is no p close, p is in the beginning and the end
    for i in range(n-2):
        choice = rand.uniform(0, 1)
        p1 = parent_1[1][i]
        p2 = parent_2[1][i]
        # it is easy to omit the order in parent so bias
        # if p1 > -1:
        #     choice -= bias
        # if p2 > -1:
        #     choice += bias
        if choice < 0.5 and wait <= 0 and i < n-2-p1-TAB:
            chromosome.append(p1)
            # max in a case it is -1 so that we dont have to wait unnecessarily
            wait = max(0, p1+TAB*p1)
        elif choice >= 0.5 and wait <= 0 and i < n-2-p2-TAB:
            chromosome.append(p2)
            wait = max(0, p2+TAB*p2)
        else:
            chromosome.append(-1)
        wait -= 1
        # check if there are more breaks than the max number of breaks in a chromosome
        if chromosome[i+1] > -1:
            breaks += 1
        # if breaks>=m:
        #     for j in range (i+1,n):
        #         chromosome.append(-1)
        #     break

    # last break at n
    p = int(rand.uniform(1,5))
    chromosome.append(p)

    print("BREAKS: ", breaks)
    mdl_result = apply_function(breaks, chromosome, data)
    return mdl_result, chromosome


# Produce offspring by: taking a gene from parent || changing own gene
def mutation(parent, n, data):
    print("MUTATION")
    p = int(rand.uniform(1,5))    
    chromosome = []
    pi1 = 0.9
    pi2 = 0.0999
    breaks = 0

    # first break at 0
    chromosome.append(p)
    wait = TAB*p

    for i in range(n-2):
        choice = rand.uniform(0, 1)
        if choice < pi1 and wait <= 0 and i < n-2-p-TAB:
            chromosome.append(parent[1][i])
            wait = parent[1][i]+TAB*parent[1][i]
        elif choice > pi1+pi2 and wait <= 0 and i < n-2-p-TAB:
            p = int(rand.uniform(1,5))
            chromosome.append(p)
            wait = p+TAB*p
        else:
            chromosome.append(-1)
        wait -= 1
        if chromosome[i+1] > -1:
            breaks += 1
        # if breaks>=m:
        #     for j in range (i+1,n):
        #         chromosome.append(-1)
        #     break

    # last break at n
    p = int(rand.uniform(1,5))
    chromosome.append(p)
    
    print("BREAKS: ", breaks)
    mdl_result = apply_function(breaks, chromosome, data)
    return mdl_result, chromosome


def make_next_generation(previous_chromosomes, n, generation_size, data, f, mdl_values):
    next_generation = []
    sorted_chromosomes = sort_chromosomes(previous_chromosomes)
    mdl_values.append(sorted_chromosomes[0][0])
    f.write("TOP: "+str(sorted_chromosomes[0][0])+"\n"+str(sorted_chromosomes[0][1])+"\n")
    # if there is just one chromosome repeating
    if sorted_chromosomes.count(sorted_chromosomes[0]) == len(sorted_chromosomes):
        return sorted_chromosomes
    # crossover probability
    pi = 0.75
    
    for i in range(generation_size):
        print("CHROMOSOME: ", i)
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