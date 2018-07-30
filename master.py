import argparse
import os
import sys
import json
from utils.general_utils import load_config,str_to_bool,params_to_tune,generate_pars_dict
from pythia_space.pythia_functions import get_objective_func
from skopt.space import Real
from skopt.optimizer import Optimizer
from skopt import expected_minimum
import numpy as np
from genetic_algorithm import GA

def main(args, preprocess=False, genetic=True, bayesian=False):
    config_file = args.config_file
    generations = args.generations
    iterations = generations
    populationSize = args.population_size
    maxEvents = args.max_events
    
    
    print config_file
    config = load_config(config_file) 
    WorkHOME = os.environ['WorkHOME']

    generate_pars_dict()    

    print 'WorkHOME = {}'.format(WorkHOME)

    blocks = []
    for i in range(1,4):
        blocks.append(str_to_bool(config['block{}'.format(i)]))

    paramNames = params_to_tune(blocks)
    
    # ranges to improve monash (+/- 50% of monash tune values, edited so professor params are within range)
    ranges = {'probStoUD' : Real(low=0.1085, high=0.3255, prior='uniform', transform='identity'), 'probQQtoQ' : Real(low=0.0405, high=0.1215, prior='uniform', transform='identity'), 'probSQtoQQ' : Real(low=0.4575, high=1, prior='uniform', transform='identity'), 'probQQ1toQQ0' : Real(low=0.01375, high=0.04125, prior='uniform', transform='identity'), 'mesonUDvector' : Real(low=0.25, high=0.75, prior='uniform', transform='identity'), 'mesonSvector' : Real(low=0.275, high=0.825, prior='uniform', transform='identity'), 'mesonCvector' : Real(low=0.44, high=1.32, prior='uniform', transform='identity'), 'mesonBvector' : Real(low=1.1, high=3, prior='uniform', transform='identity'), 'etaSup' : Real(low=0.3, high=0.9, prior='uniform', transform='identity'), 'etaPrimeSup' : Real(low=0.06, high=0.18, prior='uniform', transform='identity'), 'popcornSpair' : Real(low=0.9, high=1, prior='uniform', transform='identity'), 'popcornSmeson' : Real(low=0.5, high=0.75, prior='uniform', transform='identity'), 'aLund' : Real(low=0.25, high=1.02, prior='uniform', transform='identity'), 'bLund' : Real(low=0.49, high=1.47, prior='uniform', transform='identity'), 'aExtraSquark' : Real(low=0, high=0.0001, prior='uniform', transform='identity'), 'aExtraDiquark' : Real(low=0.485, high=1.455, prior='uniform', transform='identity'), 'rFactC' : Real(low=0.66, high=1.98, prior='uniform', transform='identity'), 'rFactB' : Real(low=0.4275, high=1.2825, prior='uniform', transform='identity'), 'sigma' : Real(low=0.1675, high=0.5025, prior='uniform', transform='identity'), 'enhancedFraction' : Real(low=0.01, high=0.015, prior='uniform', transform='identity'), 'enhancedWidth' : Real(low=1, high=3, prior='uniform', transform='identity'), 'alphaSvalue' : Real(low=0.06825, high=0.20475, prior='uniform', transform='identity'), 'pTmin' : Real(low=0.25, high=0.75, prior='uniform', transform='identity'), 'pTminChgQ' : Real(low=0.25, high=0.75, prior='uniform', transform='identity')}
    
    # ranges that are limits of allowed by pythia
#     ranges = {'probStoUD': Real(low=0, high=1, prior='uniform', transform='identity'), 'probQQtoQ': Real(low=0, high=1, prior='uniform', transform='identity'), 'probSQtoQQ': Real(low=0, high=1, prior='uniform', transform='identity'), 'probQQ1toQQ0': Real(low=0, high=1, prior='uniform', transform='identity'), 'mesonUDvector': Real(low=0, high=3, prior='uniform', transform='identity'), 'mesonSvector': Real(low=0, high=3, prior='uniform', transform='identity'), 'mesonCvector': Real(low=0, high=3, prior='uniform', transform='identity'), 'mesonBvector': Real(low=0, high=3, prior='uniform', transform='identity'), 'etaSup': Real(low=0, high=1, prior='uniform', transform='identity'), 'etaPrimeSup': Real(low=0, high=1, prior='uniform', transform='identity'), 'popcornSpair': Real(low=0.9, high=1, prior='uniform', transform='identity'), 'popcornSmeson': Real(low=0.5, high=1, prior='uniform', transform='identity'), 'aLund': Real(low=0.2, high=2, prior='uniform', transform='identity'), 'bLund': Real(low=0.2, high=2, prior='uniform', transform='identity'), 'aExtraSquark': Real(low=0, high=2, prior='uniform', transform='identity'), 'aExtraDiquark': Real(low=0, high=2, prior='uniform', transform='identity'), 'rFactC': Real(low=0, high=2, prior='uniform', transform='identity'), 'rFactB': Real(low=0, high=2, prior='uniform', transform='identity'), 'sigma': Real(low=0, high=1, prior='uniform', transform='identity'), 'enhancedFraction': Real(low=0.01, high=1, prior='uniform', transform='identity'), 'enhancedWidth': Real(low=1, high=10, prior='uniform', transform='identity'), 'alphaSvalue': Real(low=0.06, high=0.25, prior='uniform', transform='identity'), 'pTmin': Real(low=0.1, high=2, prior='uniform', transform='identity'), 'pTminChgQ': Real(low=0.1, high=2, prior='uniform', transform='identity')}
    
    monashParams = {'probStoUD': 0.217, 'probQQtoQ': 0.081, 'probSQtoQQ': 0.915, 'probQQ1toQQ0': 0.0275, 'mesonUDvector': 0.50, 'mesonSvector': 0.55, 'mesonCvector': 0.88, 'mesonBvector': 2.20, 'etaSup': 0.60, 'etaPrimeSup': 0.12, 'popcornSpair': 0.90, 'popcornSmeson': 0.50, 'aLund': 0.68, 'bLund': 0.98, 'aExtraSquark': 0.00, 'aExtraDiquark': 0.97, 'rFactC': 1.32, 'rFactB': 0.855, 'sigma': 0.335, 'enhancedFraction': 0.01, 'enhancedWidth': 2.0, 'alphaSvalue': 0.1365, 'pTmin': 0.5, 'pTminChgQ': 0.5}
    
    # tune 
    professorParams = {'probStoUD': 0.19, 'probQQtoQ': 0.09, 'probSQtoQQ': 1.00, 'probQQ1toQQ0': 0.027, 'mesonUDvector': 0.62, 'mesonSvector': 0.725, 'mesonCvector': 1.06, 'mesonBvector': 3.0, 'etaSup': 0.63, 'etaPrimeSup': 0.12, 'popcornSpair': 0.90, 'popcornSmeson': 0.50, 'aLund': 0.3, 'bLund': 0.8, 'aExtraSquark': 0.00, 'aExtraDiquark': 0.50, 'rFactC': 1.00, 'rFactB': 0.67, 'sigma': 0.304, 'enhancedFraction': 0.01, 'enhancedWidth': 2.0, 'alphaSvalue': 0.1383, 'pTmin': 0.4, 'pTminChgQ': 0.4}
    monashParamValues = []
    professorParamValues = []
    for p in paramNames:
        monashParamValues.append(monashParams[p])
        professorParamValues.append(professorParams[p])
    
    paramRanges = []
    for p in paramNames:
        paramRanges.append(ranges[p])
    
    avgFitnessHistory = []
    fitnessHistory = []
    bestParams = []
    paramHistory = []
    metrics = ['chi2', 'wasserstein', 'ks_2samp', 'entropy', 'mod-log-likelihood']
    metric = metrics[3]
    prefix = metric + '_'
    
    if preprocess:
        trueFitness = get_objective_func(monashParams, metric)
        print 'distance with true params: {}'.format(trueFitness)
        
        fitValues = [0.13208249393929786, 0.51994805609029804, 0.25, 0.77965189303083682, 1.0901868268136528, 1.0405344632358078, 8.0080159491002171e-05, 0.3282750911993525, 1.307123178350605, 0.24494190072820199, 0.34232941807977046, 0.021253594068452883, 0.70945494182953883, 0.31633982796247129, 0.082106591462099546, 0.17715548897442518, 0.93070556103172952, 1.2263012176090409, 0.98127718161464395]
        fitParams = {}
        i = 0
        for p in paramNames:
            fitParams[p] = fitValues[i]
            i += 1
        fitFitness = get_objective_func(fitParams, metric)
        print 'distance with fitted params: {}'.format(fitFitness)
        
#         for p in monashParams.keys():
#             params = dict(monashParams)
#             randomFitness = 0
#             for i in range(2):
#                 params[p] = ranges[p].rvs()[0]
#                 randomFitness += get_objective_func(params, metric)
#             randomFitness /= 2
#             print 'distance after randomizing {}: {}'.format(p, randomFitness)
    
    if genetic:
        initialPopulation = [monashParamValues, professorParamValues]
        opt = GA(paramRanges, populationSize, generations, initialPopulation=initialPopulation)
        for g in range(generations):
            population = opt.ask()
            fitnesses = []
            for paramValues in population:
                params = {}
                i = 0
                for p in paramNames:
                    params[p] = paramValues[i]
                    i += 1
                #fitness = get_objective_func(params, metric, N_events=1000000/0.6*(1/(1+(1-(g+1)/generations)^3) - 0.4))
                fitness = get_objective_func(params, metric, N_events=maxEvents/1.001*(0.001 + 1/(1+np.exp(-(g+1-generations/2)/2))))
                fitnesses.append(fitness)
            print 'finished GENERATION {} out of {}'.format(g+1, generations)
            bestFit = opt.tell(population, 1/np.array(fitnesses), g)
            bestParams = bestFit[0]
            print 'best params so far: {}'.format(bestParams)
            paramHistory.append(np.array(bestFit[0]))
            fitnessHistory.append(1/bestFit[1])
            avgFitnessHistory.append(1/(sum(fitnesses)/len(fitnesses)))

        np.savetxt(prefix + 'gaParamHistory.txt', np.array(paramHistory))
        np.savetxt(prefix + 'gaAvgHistory.txt', np.array(avgFitnessHistory))
        np.savetxt(prefix + 'gaMaxHistory.txt', np.array(fitnessHistory))
    
    if bayesian:
        opt = Optimizer(paramRanges, n_initial_points=populationSize)
        for g in range(iterations*populationSize):
            paramValues = opt.ask()
            params = {}
            i = 0
            for p in paramNames:
                params[p] = paramValues[i]
                i += 1
            fitness = get_objective_func(params, metric)
            print 'finished ITERATION {} out of {}'.format(g+1, iterations*populationSize)
            bestFit = opt.tell(paramValues, fitness)
            if len(bestFit.models) > 0 and (g+1) % populationSize == 0:
                # WORKAROUND TO SKOPT BUG
                bad_min = True
                while bad_min:
                    bad_min = False
                    try:
                        bestParams = expected_minimum(bestFit, n_random_starts=populationSize)[0]
                    except ValueError:
                        bad_min = True
                        print('FAILED')
                params = {}
                i = 0
                for p in paramNames:
                    params[p] = bestParams[i]
                    i += 1
                actualFitness = get_objective_func(params, metric)
                paramHistory.append(np.array(bestParams))
                fitnessHistory.append(actualFitness)

        np.savetxt(prefix + 'bayesParamHistory.txt', np.array(paramHistory))
        np.savetxt(prefix + 'bayesHistory.txt', np.array(fitnessHistory))
        

#     new_expt = str_to_bool(config['new_expt'])
#     spearmint_dir = config['spearmint_dir']
#     start_spearmint_tune(spearmint_dir,WorkHOME,new_expt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', help='configuration file for tune')
    parser.add_argument('-g', '--generations', help='number of generations', type=int, default=50)
    parser.add_argument('-p', '--population-size', help='population size', type=int, default=400)
    parser.add_argument('-e', '--max-events', help='maximum number of pythia events to evaluate per parameter set', type=int, default=250000)
    args = parser.parse_args()
    main(args)
#     main(sys.argv[1])