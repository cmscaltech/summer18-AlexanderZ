import numpy as np
from skopt.space import Real, Integer
from copy import deepcopy

class PSO(object):
    """
    A particle swarm optimizer that gives the steps of particle swarm iterations.
    
    Parameters
    
    dimensions [list, shape=(n_dims,)]
        List of search space dimensions. Each search dimension is an instance of a
        'Dimension' object ('Real' or 'Integer')
    
    the argument num_iterations in ask specifies the number of generations
    """
    
    c1 = 2
    c2 = 2
    v_max = 20   # TODO should be array
    
    def __init__(self, dimensions, populationSize=40, maxGenerations=10000, initialPopulation=[]):
        self.paramRanges = dimensions
        self.numParams = len(self.paramRanges)
        self.populationSize = populationSize
        self.numElite = populationSize // 5
        self.fitness = np.array([None]*populationSize)
        self.maxGenerations = maxGenerations
        
        population = initialPopulation
        for i in range(len(population), populationSize):
            paramSet = []
            for j in range(0, self.numParams):
                gene = float(self.paramRanges[j].rvs()[0])
                paramSet.append(gene)
            population.append(paramSet)
        self.population = np.array(population)
        
        self.velocities = np.zeros((self.populationSize, self.numParams))
        self.bestPreviousPopulation = np.copy(self.population)
        self.bestPreviousFitnesses = np.zeros(self.populationSize)
    
    def ask(self):
        rounded = deepcopy(self.population)
        for i in range(len(self.population)):
            for j in range(len(self.paramRanges)):
                if isinstance(self.paramRanges[j], Integer):
                    rounded[i][j] = int(rounded[i][j])
#         print('Asked for:', rounded)
        return rounded
    
    # needs params/results to have length populationSize
    def tell(self, params, results, generation):
        searchIn = self.ask()
        for i in range(len(searchIn)):
            for j in range(len(params)):
                if params[j].tolist() == searchIn[i].tolist() and self.fitness[i] is None:
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
        print('Stepping in generation', generation, 'with fitness:', self.fitness)
        
        inertia = 0.4 + 0.8*(self.maxGenerations - generation - 1)/(self.maxGenerations - 1)
        
        bestInd = self.fitness.argsort()[-1]
        bestPopulationMember = self.population[bestInd]
        
        self.bestPreviousPopulation[self.fitness > self.bestPreviousFitnesses] = self.population[self.fitness > self.bestPreviousFitnesses]
        self.bestPreviousFitnesses[self.fitness > self.bestPreviousFitnesses] = self.fitness[self.fitness > self.bestPreviousFitnesses]
        
        self.velocities = inertia*self.velocities + self.c1*np.random.random()*(self.population - self.bestPreviousPopulation) + self.c2*np.random.random()*(self.population - bestPopulationMember)
        self.velocities = np.clip(self.velocities, -self.v_max, self.v_max)
        self.population += self.velocities
        
        bestFit = self.fitness[bestInd]
        self.fitness = np.array([None]*self.populationSize)
        
        return bestFit