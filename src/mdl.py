import random as rand
import math
import numpy as np

#Objective function
def MDL(parameter_tuple):
    m=parameter_tuple[0]
    breakpoints=parameter_tuple[1]

    terms=[]
    terms[0]=math.log(m,2)


    return rand.uniform(0,10)

#parameters usable by MDL function
def make_mdl_parameters(m,chromosone):
    breakpoints=[]
    n=len(chromosone)
    for i in range(n):
        if chromosone[i]!=-1:
            breakpoints.append((i,chromosone[i]))
    return (m,n,breakpoints)