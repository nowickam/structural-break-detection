import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import json


def process_json_data(sensor_values, sensor_timestamps):
    sum_values = []
    # timestamps
    sum_values.append([])
    # values
    sum_values.append([])

    # divide the values into separate x, y and z arrays
    for value, timestamp in zip(sensor_values, sensor_timestamps):
        sum_values[0].append(timestamp)
        sum_values[1].append(np.abs(value['x'])+np.abs(value['y'])+np.abs(value['z']))

    # calculate quantiles
    sum_q1 = np.percentile(sum_values[1], 25)
    sum_q3 = np.percentile(sum_values[1], 75)

    sum_lower = sum_q1-2.5*(sum_q3-sum_q1)
    sum_upper = sum_q3+2.5*(sum_q3-sum_q1)

    # delete outliers
    for i in range(0,len(sum_values[1])-1):
        if(sum_values[1][i] > sum_upper):
            sum_values[1][i] = sum_upper
        elif(sum_values[1][i] < sum_lower):
            sum_values[1][i] = sum_lower

    sum_values[0] = sum_values[0][50:(len(sum_values[0])-50)]
    sum_values[1] = sum_values[1][50:(len(sum_values[1])-50)]

    return sum_values


def plot_data(title, save, values, timebreaks):
    plt.figure()
    plt.title(title)

    x, y = values[0], values[1]
    plt.plot(x, y)

    for i, tbreak in zip(range(0,len(timebreaks)),timebreaks):
        if tbreak != -1:
            plt.axvline(values[0][i], c = 'r')

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.xlabel("hours")
    plt.ylabel("g (=9.8m/s^2)")
    plt.savefig("output/"+save, bbox_inches='tight')
    plt.show()


def plot_convergence(title, save, generations, mdl_values):
    plt.figure()
    plt.title(title)

    args=list(range(1,generations))

    x, y = args, mdl_values
    plt.plot(x, y)

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.xlabel("generation number")
    plt.ylabel("mdl value")
    plt.savefig("output/"+save, bbox_inches='tight')
    plt.show()