import copy
import time
import random as rnd
from chromosome import Chromosome
from projectGroups import Groups
from examiners import Examiners



def populate(groups,examiners):
    chromosomes = []
    for _ in range(population):
        #chromosomes.append(Chromosome(groups,examiners, sessionTime=1.5, parallel=3)) #Choked the timetable to spice things up! (Take much longer)
        chromosomes.append(Chromosome(groups, examiners)) #Normal Execution
    return chromosomes #Chromosome construtor generates random genes in a chromosome

def fitness(chromosomes):
    for gene in chromosomes:
        gene.fitness = gene.getFitness()
        print(gene.fitness)
    return chromosomes

def selection(chromosomes):
    #Pick top fittest 40%
    chromosomes = sorted(chromosomes, key=lambda agent: agent.fitness, reverse=False)
    chromosomes = chromosomes[:int(0.4 * len(chromosomes))]
    return chromosomes

def crossover(chromosomes):
    # Refill the rest (60%) with the fittest (40%)
    children = []
    loop = int((population - len(chromosomes)) / 2)
    for _ in range(loop):
        #Pick two random genes to crossover
        fatherCopy = copy.deepcopy(rnd.choice(chromosomes))
        motherCopy = copy.deepcopy(rnd.choice(chromosomes))

        #Pick two random genes, for example, X&Y
        #Locate X&Y in both chromosomes
        #Swap X1 with Y1 and X2 with Y2
        fatherGene = fatherCopy.timeTable.randomGene()
        motherGene = motherCopy.timeTable.randomGene()

        #Swapping Gene Mother => Father
        fx1,fy1 = fatherCopy.timeTable.findById(motherGene)
        mx1,my1 = motherCopy.timeTable.findById(fatherGene)

        temp = fatherCopy.timeTable.slots[fy1][fx1]
        fatherCopy.timeTable.slots[fy1][fx1] = motherCopy.timeTable.slots[my1][mx1]
        motherCopy.timeTable.slots[my1][mx1] = temp

        #Swapping Gene Father => Mother
        fx2, fy2 = fatherCopy.timeTable.findById(fatherGene)
        mx2, my2 = motherCopy.timeTable.findById(motherGene)

        temp = fatherCopy.timeTable.slots[fy2][fx2]
        fatherCopy.timeTable.slots[fy2][fx2] = motherCopy.timeTable.slots[my2][mx2]
        motherCopy.timeTable.slots[my2][mx2] = temp

        #Append crossed chromosomes
        children.append(fatherCopy)
        children.append(motherCopy)
    chromosomes.extend(children)
    return chromosomes

def mutation(chromosomes):
    #Chance to mutate gene (pick new arbitary examiners)
    #I noticed a significant increase in search speed by lowering the mutation rate as conflicts reduce
    for chromosome in chromosomes:
        if (chromosome.fitness <= 2):
            chance = 0.01
        else:
            chance = 0.04
        for geneGroup in chromosome.timeTable.slots:
            for gene in geneGroup:
                if (rnd.random() < chance and type(gene) != str):
                    gene.mutate()
    return chromosomes

#Extract GROUPS & EXAMINERS from excel sheet
path = "projects.xlsx"
population = 20
generation = 0
groups = Groups(path)
examiners = Examiners(path)
chromosomes = populate(groups,examiners)
start_time = time.time()

#Stop until you find a solution
while all(chromosome.fitness != -1 for chromosome in chromosomes):
    print("Generation: "+ str(generation))
    generation += 1
    chromosomes = fitness(chromosomes)
    chromosomes = selection(chromosomes)
    chromosomes = crossover(chromosomes)
    chromosomes = mutation(chromosomes)

chromosomes = sorted(chromosomes, key=lambda agent: agent.fitness, reverse=False)
chromosomes[0].printChromosome()
end_time = time.time() - start_time
print("\n\t*Found solution in", str(end_time)[0:5]+"s", "after" ,generation ,"generations")