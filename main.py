import json
import random as rand
import os
import time

import src.genetic_algorithm as ga
import data.read_data as dr


DATE = "2020-2-17"
DEVICE = "accelerometer"
start = time.time()
PATH = "data/sensor-app-json.json"

os.makedirs("./output/"+DATE, exist_ok=True)

data = dr.open_json(PATH, DEVICE, DATE)

# values_name is the name of the column with y-values
# timestamps_name is the name of the column with x-values
# data = dr.open_csv(PATH, values_name, timestamps_name)

# change ms to hours
data[0] = [int(time)/(1000*60*60) for time in data[0]]
dr.plot_data("Accelerometer from "+DATE, DATE +
             "/acc_"+DATE+".png", data, {})

GENERATIONS = 50
GENERATION_SIZE = 20
n = len(data[0])    # length of the data

chromosomes = []
mdl_values = []
rand.seed()

f = open("output/"+DATE+"/output.txt", "a")
f.write("\nNUMBER OF GENERATIONS: "+str(GENERATIONS)+"\n")
f.write("GENERATION SIZE: "+str(GENERATION_SIZE)+"\n")
f.write("DATA LENGTH: "+str(n)+"\n")

f.write("GENERATION 0\n")
chromosomes = ga.make_first_generation(n, GENERATION_SIZE, data)
f.write("TOP: " + str(chromosomes[0][0]) + "\n")

# main evolution loop
i = 1
while i < GENERATIONS:
    print("\nGENERATION ", i)
    f.write("\nGENERATION "+str(i)+"\n")

    chromosomes = ga.make_next_generation(
        chromosomes, n, GENERATION_SIZE, data, f, mdl_values)
    i += 1

result_chromosomes = ga.sort_chromosomes(chromosomes)

f.write("\nMDL: " + str(result_chromosomes[0][0]) + "\n")
for gene in result_chromosomes[0][1]:
    f.write(str(gene)+" ")
duration = time.time()-start
print(duration)
f.write("DURATION: "+str(duration))
f.close()

dr.plot_data("Accelerometer from "+DATE, DATE+"/acc_"+DATE+"_"+str(GENERATIONS) +
             "_"+str(GENERATION_SIZE)+".png", data, result_chromosomes[0][1])
dr.plot_convergence("Convergence of accelerometer from 2020.03.17", DATE+"/conv_" +
                    DATE+"_"+str(GENERATIONS)+"_"+str(GENERATION_SIZE)+".png", GENERATIONS, mdl_values)
