import random as rand
import math
import numpy as np
from statsmodels.regression.linear_model import yule_walker


# Objective function
def mdl(m, n, breakpoints, data):
    # maintain the order
    timestamps = list(breakpoints.keys())
    timestamps.sort()

    terms = []
    m_log = max(1, m)
    terms.append(math.log(m_log, 2))

    terms.append(m*math.log(n, 2))

    terms.append(sum(math.log(breakpoints[i], 2) for i in timestamps))

    term3 = term4 = 0

    for i in range(1, len(breakpoints)):
        ni = timestamps[i]-timestamps[i-1]
        term3 += (breakpoints[timestamps[i]]+2)/2*math.log(ni, 2)

        data_section_values=[]

        for j in range(timestamps[i-1], timestamps[i]-1):
            data_section_values.append(data[1][j])

        # print(data_section_values,breakpoints[i-1][1])
        rho, sigma = yule_walker(data_section_values, breakpoints[timestamps[i-1]])
        print("START:", timestamps[i-1], "END:", timestamps[i]-1, "AR: ", breakpoints[timestamps[i-1]])
        var = math.pow(sigma, 2)
        term4 += ni/2*math.log(2*math.pi*var, 2)
    
    terms.append(term3)
    terms.append(term4)

    terms.append(n/2)

    print("MDL: ", sum(terms))

    return sum(terms) 


# parameters usable by MDL function
def make_mdl_parameters(m, chromosome):
    breakpoints = []
    n = len(chromosome)
    for i in range(n):
        if chromosome[i] != -1:
            breakpoints.append((i, chromosome[i]))
    # number of breaks, length of data, (time,ar-order) tuple
    return m, n, breakpoints
