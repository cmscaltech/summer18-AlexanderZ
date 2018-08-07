import numpy as np
from copy import deepcopy

class GA(object):
    """
    A genetic algorithm optimizer that gives the steps of evolutionary optimization.
    
    Parameters
    
    dimensions [list, shape=(n_dims,2,)]
        List of search space dimensions.
    
    the argument num_iterations in ask specifies the number of generations
    """
    
    nonuniformityMutationConstant = 3
    
    def __init__(self, dimensions, populationSize, maxGenerations, initialPopulation=[]):
        self.paramRanges = dimensions
        self.numParams = len(self.paramRanges)
        self.populationSize = populationSize
        self.numElite = populationSize // 5
        self.fitness = np.array([None]*populationSize)
        self.maxGenerations = maxGenerations
        
        population = initialPopulation
        for i in range(len(population), populationSize):
            chromosome = []
            for j in range(0, self.numParams):
                gene = np.random.uniform(self.paramRanges[j][0], self.paramRanges[j][1])
                chromosome.append(gene)
            population.append(chromosome)
        self.population = population
        
    
    def ask(self):
        popCopy = deepcopy(self.population)
#         print('Asked for:', popCopy)
        return popCopy
    
    # needs params/results to have length populationSize
    def tell(self, params, results, generation):
        searchIn = self.ask()
        for i in range(len(searchIn)):
            for j in range(len(params)):
                if params[j] == searchIn[i] and self.fitness[i] is None:
#                     print('Found told params')
                    self.fitness[i] = results[j]
#         print('Fitness:', self.fitness)
        if None not in self.fitness:
#             print('Population before stepping:', self.population)
            bestFitness = self.step(generation)
            return self.population[0], bestFitness
#             print('Population after stepping:', self.population)
        
        return self.population[0], self.fitness[0]
        
    
    def step(self, generation):
        print('Stepping in generation', generation, 'with fitness:',self.fitness)
        children = []
        newFitness = [None]*self.populationSize
        
        # elitism: copy fittest organisms
        eliteIndices = self.fitness.argsort()[-self.numElite:][::-1]
        for i in range(len(eliteIndices)):
            children.append(self.population[eliteIndices[i]])
        
        bestFitness = self.fitness[eliteIndices[0]]
        
        i = self.numElite
        while i < self.populationSize:
            p1 = self.tournament_select()
            p2 = self.tournament_select()
            children.append(self.mutate(self.crossover(p1, p2), generation))
            i += 1
        
        self.population = children
        self.fitness = np.array(newFitness)
        
        return bestFitness
    
    def tournament_select(self):
        arr = list(range(self.populationSize))
        ind1 = np.random.randint(self.populationSize)
        arr.remove(ind1)
        ind2 = np.random.choice(arr)
        
        if self.fitness[ind1] > self.fitness[ind2]:
            return ind1
        else:
            return ind2
    
    def crossover(self, p1, p2):
        moreFit = p1
        lessFit = p2
        if self.fitness[p2] > self.fitness[p1]:
            moreFit = p2
            lessFit = p1
        
        child = []
        for i in range(self.numParams):
            gene = np.random.random() * (self.population[moreFit][i] - self.population[lessFit][i]) + self.population[moreFit][i]
            gene = self.cap_gene(gene, i)
            child.append(gene)
        
        return child
    
    def cap_gene(self, gene, i):
        if gene < self.paramRanges[i][0]:
            gene = float(self.paramRanges[i][0])
        elif gene > self.paramRanges[i][1]:
            gene = float(self.paramRanges[i][1])
        return gene
    
    def mutate(self, chromosomeOrig, generation):
        chromosome = list(chromosomeOrig)
        for i in range(self.numParams):
            mutation = 1 - np.power(np.random.random(), np.power(1 - generation/self.maxGenerations, self.nonuniformityMutationConstant))
            
            if np.random.random() > 0.5:
                mutation *= self.paramRanges[i][1] - chromosome[i]
            else:
                mutation *= -(chromosome[i] - self.paramRanges[i][0])
            chromosome[i] += mutation
            chromosome[i] = self.cap_gene(chromosome[i], i)
        return chromosome
    