import random
import math

SIZE = 200

#Objective function
def MDL(size, parameters):
    return

#Start with an initial set of chromosomes
def generate_chromosones(size):
    return

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