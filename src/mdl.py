import random as rand
import math
import numpy as np

#Objective function
def MDL(parameter_tuple):
    m=parameter_tuple[0]
    n=parameter_tuple[1]
    breakpoints=parameter_tuple[2]

    terms=[]
    terms.append(math.log(m,2))

    terms.append(m*math.log(n,2))

    terms.append(sum(math.log(i[1],2) for i in breakpoints))

    term3=term4=0

    for i in range(1,len(breakpoints)-1):
        ni=breakpoints[i][0]-breakpoints[i-1][0]
        term3+=(breakpoints[i][1]+2)/2*math.log(ni,2)

        # TODO estimate the white noise variance
        # var=np.var(breakpoints[i][1])
        # print(2*math.pi*var)
        term4+=ni/2*math.log(2*math.pi*1,2)
    
    terms.append(term3)
    terms.append(term4)

    terms.append(n/2)

    return sum(terms) 

#parameters usable by MDL function
def make_mdl_parameters(m,chromosone):
    breakpoints=[]
    n=len(chromosone)
    for i in range(n):
        if chromosone[i]!=-1:
            breakpoints.append((i,chromosone[i]))
    #number of breaks, length of data, (time,ar-order) tuple
    return (m,n,breakpoints)
