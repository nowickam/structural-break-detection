import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import json

# with open('data\sensor-app-json2.json') as json_data:
#     data2=json.load(json_data)

# with open('data\sensor-app-json.json') as json_data:
#     data=json.load(json_data)


def process_data(sensor_values, sensor_timestamps):
    x_values = {}
    y_values = {}
    z_values = {}
    xyz_values = {}

    # divide the values into separate x, y and z arrays
    for value, timestamp in zip(sensor_values, sensor_timestamps):
        x_values[timestamp] = value['x']
        y_values[timestamp] = value['y']
        z_values[timestamp] = value['z']
        # xyz_values[timestamp] = math.sqrt(math.pow(x_values[timestamp], 2)+math.pow(y_values[timestamp], 2)+math.pow(z_values[timestamp], 2))
        xyz_values[timestamp] = np.abs(value['x'])+np.abs(value['y'])+np.abs(value['z'])

    # calculate the standard deviations
    x_mean = np.mean(list(x_values.values()))
    x_std = np.std(list(x_values.values()))

    y_mean = np.mean(list(y_values.values()))
    y_std = np.std(list(y_values.values()))

    z_mean = np.mean(list(z_values.values()))
    z_std = np.std(list(z_values.values()))

    xyz_mean = np.mean(list(xyz_values.values()))
    xyz_std = np.std(list(xyz_values.values()))

    # and delete the outliers
    for timestamp in list(x_values.keys()):
        if (np.abs(x_mean-x_values[timestamp]) > x_std or np.abs(y_mean-y_values[timestamp]) > y_std or
        np.abs(z_mean-z_values[timestamp]) > z_std or np.abs(xyz_mean-xyz_values[timestamp]) > 5*xyz_std):
            del x_values[timestamp]
            del y_values[timestamp]
            del z_values[timestamp]
            del xyz_values[timestamp]

    return x_values, y_values, z_values, xyz_values


# def initial_plot_data(title,x_values,y_values,z_values,xyz_values,multiple_plots):
#     fig=plt.figure()
#     plt.title(title)
#
#     #if plot separately x, y and z
#     if multiple_plots:
#         x,y=zip(*x_values.items())
#         plt.plot(x,y)
#
#         x,y=zip(*y_values.items())
#         plt.plot(x,y)
#
#         x,y=zip(*z_values.items())
#         plt.plot(x,y)
#
#     #plot only the sum
#     x,y=zip(*xyz_values.items())
#     plt.plot(x,y)
#
#     if multiple_plots:
#         plt.legend(('X','Y','Z','sum'))
#     ax = plt.axes()
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(500))


def plot_data(title, values, timebreaks):
    plt.figure()
    plt.title(title)

    x, y = zip(*values.items())
    plt.plot(x, y)

    for i,tbreak in zip(range(0,len(timebreaks)),timebreaks):
        if tbreak != -1:
            plt.axvline(list(values.keys())[i], c='r')

    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
    plt.xlabel("ms")
    plt.ylabel("g (=9.8m/s^2)")
    plt.show()

# data_list=[data['gyroscope']['2020-2-15'],data['accelerometer']['2020-2-15'],
#             data2['gyroscope']['2020-2-17'],data2['accelerometer']['2020-2-17']]
# names_list=[('gyroscope','2020-2-15'),('accelerometer','2020-2-15'),
#             ('gyroscope','2020-2-17'),('accelerometer','2020-2-17')]
#
# for data,name in zip(data_list,names_list):
#     gyro_values=data.values()
#     gyro_timestamps=data.keys()
#
#     gx_values, gy_values, gz_values,gxyz_values=proccess_data(gyro_values,gyro_timestamps)
#
#     init_plot_data("Records from "+name[0]+", "+name[1],gx_values,gy_values,gz_values,gxyz_values,False)
#     plt.xlabel("ms")
#     if name[0]=='gyroscope':
#         plt.ylabel("rad/s")
#     else:
#         plt.ylabel("g (=9800cm/s^2)")


# plt.show()

