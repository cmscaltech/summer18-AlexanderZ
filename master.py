import argparse
import os
import sys
import json
from utils.general_utils import str_to_bool,params_to_tune,generate_pars_dict
from pythia_space.pythia_functions import get_objective_func
import numpy as np

def main(args):
    paramVals_str = args.params
    names = args.names
    paramValsAll = np.array([float(s.replace('"', '')) for s in paramVals_str.split(',')])
    paramNames = [s.strip() for s in names.split(',')]
    paramValsAll = np.reshape(paramValsAll, (len(paramValsAll)//len(paramNames), len(paramNames)))
    
    WorkHOME = os.environ['WorkHOME']

    generate_pars_dict()
    
    set = 0
    for paramVals in paramValsAll:
        params = {}
        i = 0
        for p in paramNames:
            params[p] = paramVals[i]
            i += 1
    
        fitness = get_objective_func(params, args.metric, args.n_events, args.n_cores)
        f = open(args.id + str(set) + '.txt', 'w+')
        f.write(str(fitness))
        f.close()
        set += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--n-cores', help='number of cores to use', type=int, default=8)
    parser.add_argument('-p', '--params', help='comma-separated matrix of parameter values')
    parser.add_argument('-n', '--names', help='comma-separated parameter names')
    parser.add_argument('-m', '--metric', help='metric for fitness function')
    parser.add_argument('-e', '--n-events', help='maximum number of pythia events to evaluate per parameter set', type=int, default=250000)
    parser.add_argument('-i', '--id', help='id to save in filename')
    args = parser.parse_args()
    main(args)