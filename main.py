import json
import random as rand
import math
import numpy as np

import src.genetic_algorithm as ga
import src.mdl as mdl
import data.json_read as dr

with open('data\sensor-app-json2.json') as json_data:
    load_data=json.load(json_data)
    data=load_data['accelerometer']['2020-2-17']

acc_values=data.values()
acc_timestamps=data.keys()

x_values, y_values, z_values,xyz_values=dr.proccess_data(acc_values,acc_timestamps)

generations=50
generation_size = 10
n = len(xyz_values)    #length of the data
chromosones=[]
ar_order=3         #AR order, later random
rand.seed(0)


chromosones=ga.make_first_generation(n,generation_size,xyz_values)
# print(chromosones)
# print("\n")

i=1 
while i<generations:
    print("GENERATION ",i)
    
    sorted_chromosones=ga.sort_chromosones(chromosones)

    # for gene in chromosones:
    #     print(gene)
    # print("\n")
    chromosones=ga.make_next_generation(chromosones,n,generation_size, xyz_values)
    i+=1

for gene in chromosones:
    print(gene)
print("\n")
