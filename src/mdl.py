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

        rho, sigma = yule_walker(data_section_values, breakpoints[timestamps[i-1]])
        var = math.pow(sigma, 2)
        term4 += ni/2*math.log(2*math.pi*var, 2)
    
    terms.append(term3)
    terms.append(term4)

    terms.append(n/2)

    return sum(terms) 
