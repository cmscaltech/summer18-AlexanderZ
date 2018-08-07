from genetic_algorithm import GA
import numpy as np
import subprocess
import argparse

def main(args):
    populationSize = args.population_size
    generations = args.generations
    maxEvents = args.max_events
    numMachines = args.machines
    
    # ranges to improve monash (+/- 50% of monash tune values, edited so professor params are within range)
    ranges = {'probStoUD' : [0.1085, 0.3255], 'probQQtoQ' : [0.0405, 0.1215], 'probSQtoQQ' : [0.4575, 1], 'probQQ1toQQ0' : [0.01375, 0.04125], 'mesonUDvector' : [0.25, 0.75], 'mesonSvector' : [0.275, 0.825], 'mesonCvector' : [0.44, 1.32], 'mesonBvector' : [1.1, 3], 'etaSup' : [0.3, 0.9], 'etaPrimeSup' : [0.06, 0.18], 'popcornSpair' : [0.9, 1], 'popcornSmeson' : [0.5, 0.75], 'aLund' : [0.25, 1.02], 'bLund' : [0.49, 1.47], 'aExtraSquark' : [0, 0.0001], 'aExtraDiquark' : [0.485, 1.455], 'rFactC' : [0.66, 1.98], 'rFactB' : [0.4275, 1.2825], 'sigma' : [0.1675, 0.5025], 'enhancedFraction' : [0.01, 0.015], 'enhancedWidth' : [1, 3], 'alphaSvalue' : [0.06825, 0.20475], 'pTmin' : [0.25, 0.75], 'pTminChgQ' : [0.25, 0.75]}

    # ranges that are limits of allowed by pythia
    # ranges = {'probStoUD': [0, 1], 'probQQtoQ': [0, 1], 'probSQtoQQ': [0, 1], 'probQQ1toQQ0': [0, 1], 'mesonUDvector': [0, 3], 'mesonSvector': [0, 3], 'mesonCvector': [0, 3], 'mesonBvector': [0, 3], 'etaSup': [0, 1], 'etaPrimeSup': [0, 1], 'popcornSpair': [0.9, 1], 'popcornSmeson': [0.5, 1], 'aLund': [0.2, 2], 'bLund': [0.2, 2], 'aExtraSquark': [0, 2], 'aExtraDiquark': [0, 2], 'rFactC': [0, 2], 'rFactB': [0, 2], 'sigma': [0, 1], 'enhancedFraction': [0.01, 1], 'enhancedWidth': [1, 10], 'alphaSvalue': [0.06, 0.25], 'pTmin': [0.1, 2], 'pTminChgQ': [0.1, 2]}

    paramNames = ['alphaSvalue', 'pTminChgQ', 'pTmin', 'rFactC', 'bLund', 'rFactB', 'aExtraSquark', 'sigma', 'aExtraDiquark', 'probStoUD', 'etaSup', 'probQQ1toQQ0', 'mesonSvector', 'mesonUDvector', 'probQQtoQ', 'etaPrimeSup', 'probSQtoQQ', 'mesonBvector', 'mesonCvector']
    paramRanges = []
    for p in paramNames:
        paramRanges.append(ranges[p])
    
    monashParams = {'probStoUD': 0.217, 'probQQtoQ': 0.081, 'probSQtoQQ': 0.915, 'probQQ1toQQ0': 0.0275, 'mesonUDvector': 0.50, 'mesonSvector': 0.55, 'mesonCvector': 0.88, 'mesonBvector': 2.20, 'etaSup': 0.60, 'etaPrimeSup': 0.12, 'popcornSpair': 0.90, 'popcornSmeson': 0.50, 'aLund': 0.68, 'bLund': 0.98, 'aExtraSquark': 0.00, 'aExtraDiquark': 0.97, 'rFactC': 1.32, 'rFactB': 0.855, 'sigma': 0.335, 'enhancedFraction': 0.01, 'enhancedWidth': 2.0, 'alphaSvalue': 0.1365, 'pTmin': 0.5, 'pTminChgQ': 0.5}    
    professorParams = {'probStoUD': 0.19, 'probQQtoQ': 0.09, 'probSQtoQQ': 1.00, 'probQQ1toQQ0': 0.027, 'mesonUDvector': 0.62, 'mesonSvector': 0.725, 'mesonCvector': 1.06, 'mesonBvector': 3.0, 'etaSup': 0.63, 'etaPrimeSup': 0.12, 'popcornSpair': 0.90, 'popcornSmeson': 0.50, 'aLund': 0.3, 'bLund': 0.8, 'aExtraSquark': 0.00, 'aExtraDiquark': 0.50, 'rFactC': 1.00, 'rFactB': 0.67, 'sigma': 0.304, 'enhancedFraction': 0.01, 'enhancedWidth': 2.0, 'alphaSvalue': 0.1383, 'pTmin': 0.4, 'pTminChgQ': 0.4}
    monashParamValues = []
    professorParamValues = []
    for p in paramNames:
        monashParamValues.append(monashParams[p])
        professorParamValues.append(professorParams[p])

    avgFitnessHistory = []
    fitnessHistory = []
    bestParams = []
    paramHistory = []
    metrics = ['chi2', 'wasserstein', 'ks_2samp', 'entropy', 'mod-log-likelihood']
    metric = metrics[3]
    prefix = metric + '_'    

    subprocess.call(['git', 'clone', 'https://github.com/quantummind/surf2018.git'])
    subprocess.call(['tar', 'czf', 'surf2018.tar.gz', 'surf2018'])   
    subprocess.call(['rm', '-rf', 'surf2018'])

    f = open('template.jdl', 'r')
    template = f.read()
    f.close()

    condorCommands = template
    for i in range(numMachines):
        condorCommands += 'Executable = submissions/' + str(i) + '.sh\nError = ../error/job.' + str(i) + '\nOutput = ../out/job.' + str(i) + '\nLog = ../log/job.' + str(i) + '\nQueue 1\n'
    f = open('submit.jdl', 'w+')
    f.write(condorCommands)
    f.close()
    header = '#!/bin/sh\ntar -xzf surf2018.tar.gz\ncd surf2018/pythia_space\nmake PYTHIA8_HOME=/root_download/pythia8235\ncd ../\nexport WorkHOME=/srv/surf2018\n'
    subprocess.call(['chmod', '+x', './process_commands.sh'])
    subprocess.call(['rm', '-r', 'submissions'])
    subprocess.call(['mkdir', 'submissions', 'log', 'error', 'out'])
    
    initialPopulation = [monashParamValues, professorParamValues]
    opt = GA(paramRanges, populationSize, generations, initialPopulation=initialPopulation)
    pn = ','.join(paramNames)
    batch_size = populationSize//numMachines
    for g in range(generations):
        subprocess.call(['rm', '-r', 'fitnesses'])
        subprocess.call(['mkdir', 'fitnesses'])
        population = opt.ask()
        
        ne = str(int(maxEvents/0.6*(1/(1+(1-(g+1)/generations)**3) - 0.4)))
        pv = ''
        for i in range(populationSize):
            #fitness = get_objective_func(params, metric, N_events=1000000/0.6*(1/(1+(1-(g+1)/generations)^3) - 0.4))
            pv += ',' + ','.join(str(v) for v in population[i])
            
            if (i+1) % batch_size == 0:
                cmd = 'python master.py -c 8 -p "' + pv[1:] + '" -n "' + pn + '" -m ' + metric + ' -e ' + ne + ' -i f\n'
                cmd += 'cd ../\npython file_transfer.py -n ' + str(i // batch_size) + ' -t ' + str(batch_size) + '\n'
                f = open('submissions/' + str(i // batch_size) + '.sh', 'w+')
                f.write(header + cmd)
                f.close()
                subprocess.call(['chmod', '+x', 'submissions/' + str(i // batch_size) + '.sh'])
                pv = ''
    
        subprocess.call(['./process_commands.sh', str(populationSize)])
    
        fitnesses = []
        for i in range(populationSize):
            f = open('./fitnesses/' + str(i) + '.txt')
            fitness = float(f.read())
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generations', help='number of generations', type=int, default=50)
    parser.add_argument('-p', '--population-size', help='population size', type=int, default=400)
    parser.add_argument('-e', '--max-events', help='maximum number of events to run (final stage of population)', type=int, default=250000)
    parser.add_argument('-m', '--machines', help='number of machines in cluster to run on (population must be divisible by this)', type=int, default=20)
    args = parser.parse_args()
    main(args)