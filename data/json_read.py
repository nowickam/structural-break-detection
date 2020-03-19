import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json

with open('db_read\sensor-app-json2.json') as json_data:
    data2=json.load(json_data)

with open('db_read\sensor-app-json.json') as json_data:
    data=json.load(json_data)

def proccess_data(sensor_values, sensor_timestamps):
    x_values={}
    y_values={}
    z_values={}
    xyz_values={}

    for value,timestamp in zip(sensor_values,sensor_timestamps):
        x_values[timestamp]=value['x']
        y_values[timestamp]=value['y']
        z_values[timestamp]=value['z']
        xyz_values[timestamp]=np.abs(value['x'])+np.abs(value['y'])+np.abs(value['z'])

    x_mean=np.mean(list(x_values.values()))
    x_std=np.std(list(x_values.values()))

    y_mean=np.mean(list(y_values.values()))
    y_std=np.std(list(y_values.values()))

    z_mean=np.mean(list(z_values.values()))
    z_std=np.std(list(z_values.values()))

    xyz_mean=np.mean(list(xyz_values.values()))
    xyz_std=np.std(list(xyz_values.values()))

    for timestamp in list(x_values.keys()):
        if (np.abs(x_mean-x_values[timestamp])>x_std or np.abs(y_mean-y_values[timestamp])>y_std or 
        np.abs(z_mean-z_values[timestamp])>z_std or np.abs(xyz_mean-xyz_values[timestamp])>xyz_std):
            del x_values[timestamp]
            del y_values[timestamp]
            del z_values[timestamp]
            del xyz_values[timestamp]

    return x_values, y_values, z_values, xyz_values



def plot_data(title,x_values,y_values,z_values,xyz_values,multiple_plots):
    fig=plt.figure()
    plt.title(title)

    if multiple_plots:
        x,y=zip(*x_values.items())
        plt.plot(x,y)

        x,y=zip(*y_values.items())
        plt.plot(x,y)

        x,y=zip(*z_values.items())
        plt.plot(x,y)

    x,y=zip(*xyz_values.items())
    plt.plot(x,y)

    if multiple_plots:
        plt.legend(('X','Y','Z','sum'))
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(500))

data_list=[data['gyroscope']['2020-2-15'],data['accelerometer']['2020-2-15'],
            data2['gyroscope']['2020-2-17'],data2['accelerometer']['2020-2-17']]
names_list=[('gyroscope','2020-2-15'),('accelerometer','2020-2-15'),
            ('gyroscope','2020-2-17'),('accelerometer','2020-2-17')]

for data,name in zip(data_list,names_list):
    gyro_values=data.values()
    gyro_timestamps=data.keys()

    gx_values, gy_values, gz_values,gxyz_values=proccess_data(gyro_values,gyro_timestamps)

    plot_data("Records from "+name[0]+", "+name[1],gx_values,gy_values,gz_values,gxyz_values,False)
    plt.xlabel("ms")
    if name[0]=='gyroscope':
        plt.ylabel("rad/s")
    else:
        plt.ylabel("g (=9.8m/s)")

plt.show()