import random as rand
import math
import numpy as np
from statsmodels.regression.linear_model import yule_walker


# Objective function
def mdl(parameter_tuple, data):
    m = parameter_tuple[0]
    n = parameter_tuple[1]
    breakpoints = parameter_tuple[2]

    terms = []
    m_log = max(1, m)
    terms.append(math.log(m_log, 2))

    terms.append(m*math.log(n, 2))

    terms.append(sum(math.log(i[1], 2) for i in breakpoints))

    term3 = term4 = 0

    for i in range(1, len(breakpoints)):
        ni = breakpoints[i][0]-breakpoints[i-1][0]
        term3 += (breakpoints[i][1]+2)/2*math.log(ni, 2)

        data_section_values=[]

        for j in range(breakpoints[i-1][0], breakpoints[i][0]-1):
            data_section_values.append(data[1][j])

        # print(data_section_values,breakpoints[i-1][1])
        rho, sigma = yule_walker(data_section_values, breakpoints[i-1][1])
        print("START:", breakpoints[i-1][0], "END:", breakpoints[i][0]-1, "AR: ", breakpoints[i-1][1])
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
