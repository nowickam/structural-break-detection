import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import json


# def process_csv_data():
#     eeg_fpz = pd.read_csv('data/woman33_eeg_fpz_cz', sep=";")
#     fig = plt.figure(figsize=(20, 12))
#     sum_values=eeg_fpz['EEG']
    # plt.plot(eeg_fpz['EEG Pz-Oz[uV]'])
    # plt.show

def open_json(path, device,date):
    with open(path) as json_data:
        load_data = json.load(json_data)
        data = load_data[device][date]

    acc_values = data.values()
    acc_timestamps = data.keys()

    return acc_values, acc_timestamps


def process_data(sensor_values, sensor_timestamps):
    sum_values = []
    # timestamps
    sum_values.append([])
    # values
    sum_values.append([])

    # divide the values into separate x, y and z arrays
    for value, timestamp in zip(sensor_values, sensor_timestamps):
        sum_values[0].append(timestamp)
        sum_values[1].append(np.abs(value['x']) +
                             np.abs(value['y'])+np.abs(value['z']))

    # calculate quantiles
    sum_q1 = np.percentile(sum_values[1], 25)
    sum_q3 = np.percentile(sum_values[1], 75)

    sum_lower = sum_q1-2.5*(sum_q3-sum_q1)
    sum_upper = sum_q3+2.5*(sum_q3-sum_q1)

    # delete outliers
    for i in range(0, len(sum_values[1])-1):
        if(sum_values[1][i] > sum_upper):
            sum_values[1][i] = sum_upper
        elif(sum_values[1][i] < sum_lower):
            sum_values[1][i] = sum_lower

    sum_values[0] = sum_values[0][50:(len(sum_values[0])-50)]
    sum_values[1] = sum_values[1][50:(len(sum_values[1])-50)]

    return sum_values

def ar_values(values, chromosome, ar_params):
    y=[]
    c=0
    timestamps=list(chromosome.keys())
    
    for i in range(chromosome[timestamps[0]]):
        y.append(values[1][i])

    for i in range(1, len(timestamps)):
        if i==1:
            start = timestamps[i-1] + chromosome[timestamps[i-1]]
        else:
            start = timestamps[i-1]
        for j in range(start, timestamps[i]):
            val=0
            for k in range(1, chromosome[timestamps[i-1]]+1):
                val += ar_params[i-1][0][k-1]*values[1][j-k]
            if j==start:
                c=values[1][j]-val
            y.append(val+c)
    return y


def plot_data(title, save, values, chromosome, ar_params):
    plt.figure(figsize=(20, 12))
    plt.title(title)

    x, y = values[0], values[1]
    plt.plot(x, y)

    res=ar_values(values, chromosome, ar_params)
    x_ar, y_ar = values[0][0:len(res)], res
    plt.plot(x_ar, y_ar)


    for i in chromosome.keys():
            plt.axvline(values[0][i], c='r')

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plt.xlabel("hours")
    plt.ylabel("g (=9.8m/s^2)")
    plt.savefig("output/"+save, bbox_inches='tight')
    # plt.show()


def plot_convergence(title, save, generations, mdl_values):
    plt.figure(figsize=(20, 12))
    plt.title(title)

    args = list(range(1, generations))

    x, y = args, mdl_values
    plt.plot(x, y)

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.xlabel("generation number")
    plt.ylabel("mdl value")
    plt.savefig("output/"+save, bbox_inches='tight')
    # plt.show()
