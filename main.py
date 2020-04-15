import json
import random as rand

import src.genetic_algorithm as ga
import data.json_read as dr


with open('data\sensor-app-json2.json') as json_data:
    load_data = json.load(json_data)
    data = load_data['accelerometer']['2020-2-17']

acc_values = data.values()
acc_timestamps = data.keys()

x_values, y_values, z_values, xyz_values = dr.process_data(acc_values, acc_timestamps)


generations = 50
generation_size = 200
n = len(xyz_values)    # length of the data
chromosomes = []
rand.seed()

f = open("output.txt", "a")
f.write("GENERATION 0\n")

chromosomes = ga.make_first_generation(n, generation_size, xyz_values)

f.write("MDL: " + str(chromosomes[0][0]) + "\n")

i = 1
while i < generations:
    print("\nGENERATION ", i)
    f.write("\nGENERATION "+str(i)+"\n")
    
    chromosomes = ga.make_next_generation(chromosomes, n, generation_size, xyz_values, f)
    i += 1

result_chromosomes = ga.sort_chromosomes(chromosomes)
f.write("\nMDL: " + str(result_chromosomes[0][0]) + "\n")
for gene in result_chromosomes[0][1]:
    f.write(str(gene)+" ")
print("\n")
f.close()


dr.plot_data("Accelerometer from 2020.02.17", xyz_values, result_chromosomes[0][1])
