import json
import random as rand
import os
import time

import src.genetic_algorithm as ga
import data.json_read as dr


date = "2020-2-17"
device = "accelerometer"
test = ""
start = time.time()
path = "data/sensor-app-json3.json"

os.makedirs("./output/"+date+test, exist_ok=True)

acc_values, acc_timestamps = dr.open_json(path, device, date)

xyz_values = dr.process_data(acc_values, acc_timestamps)
# change ms to hours
xyz_values[0] = [int(time)/(1000*60*60) for time in xyz_values[0]]
dr.plot_data("Accelerometer from "+date, date+test +
             "/acc_"+date+".png", xyz_values, {})

generations = 50
generation_size = 50
n = len(xyz_values[0])    # length of the data

f = open("output/"+date+"/output.txt", "a")
f.write("\nNUMBER OF GENERATIONS: "+str(generations)+"\n")
f.write("GENERATION SIZE: "+str(generation_size)+"\n")
f.write("DATA LENGTH: "+str(n)+"\n")

chromosomes = []
mdl_values = []
rand.seed()

f.write("GENERATION 0\n")

chromosomes = ga.make_first_generation(n, generation_size, xyz_values)

f.write("TOP: " + str(chromosomes[0][0]) + "\n")

i = 1
while i < generations:
    print("\nGENERATION ", i)
    f.write("\nGENERATION "+str(i)+"\n")

    chromosomes = ga.make_next_generation(
        chromosomes, n, generation_size, xyz_values, f, mdl_values)
    i += 1

result_chromosomes = ga.sort_chromosomes(chromosomes)
f.write("\nMDL: " + str(result_chromosomes[0][0]) + "\n")
for gene in result_chromosomes[0][1]:
    f.write(str(gene)+" ")
print("\n")
duration = time.time()-start
print(duration)
f.write("DURATION: "+str(duration))
f.close()


dr.plot_data("Accelerometer from "+date, date+test+"/acc_"+date+"_"+str(generations) +
             "_"+str(generation_size)+".png", xyz_values, result_chromosomes[0][1])
dr.plot_convergence("Convergence of accelerometer from 2020.03.17", date+test+"/conv_" +
                    date+"_"+str(generations)+"_"+str(generation_size)+".png", generations, mdl_values)
