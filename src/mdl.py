import random as rand
import math
import numpy as np

#Objective function
def MDL(parameter_tuple):
    m=parameter_tuple[0]
    n=parameter_tuple[1]
    breakpoints=parameter_tuple[2]

    terms=[]
    terms[0]=math.log(m,2)

    terms[1]=m*math.log(n,2)

    terms[2]=sum(math.log(i[1],2) for i in breakpoints)

    terms[3]=terms[4]=0

    for i in len(breakpoints):
        ni=breakpoints[i][0]-breakpoints[i-1][0]
        terms[3]+=(breakpoints[i][1]+2)/2*math.log(ni,2)

        var=np.var(breakpoints[i][1])
        terms[4]+=ni/2*math.log(2*math.pi*var,2)

    terms[5]=n/2

    return sum(terms) 

#parameters usable by MDL function
def make_mdl_parameters(m,chromosone):
    breakpoints=[]
    n=len(chromosone)
    for i in range(n):
        if chromosone[i]!=-1:
            breakpoints.append((i,chromosone[i]))
    return (m,n,breakpoints)
