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
generation_size = 200
n = len(xyz_values)    #length of the data
chromosones=[]
ar_order=3         #AR order, later random
rand.seed()

f=open("output.txt","a")
f.write("GENERATION 0\n")

chromosones=ga.make_first_generation(n,generation_size,xyz_values)
# print(chromosones)
# print("\n")
for i in chromosones:
    f.write("MDL: "+str(chromosones[0][0])+"\n")

i=1 
while i<generations:
    print("GENERATION ",i)
    f.write("GENERATION "+str(i)+"\n")
    
    sorted_chromosones=ga.sort_chromosones(chromosones)

    # for gene in chromosones:
    #     print(gene)
    # print("\n")
    chromosones=ga.make_next_generation(chromosones,n,generation_size, xyz_values,f)
    i+=1

result_chromosones=ga.sort_chromosones(chromosones)
f.write("MDL: "+str(result_chromosones[0][0])+"\n")  
for gene in result_chromosones[0][1]: 
    f.write(str(gene)+" ")
    f.write("\n\n")
print("\n")
f.close()
