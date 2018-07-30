Caltech SURF 2018: Automated Pythia Tune
=====================================================

This is an improvement using genetic algorithms and fitting experimental data (instead of simulated data) compared to the original Bayesian optimization framework for tuning a Monte Carlo event generator, as described in the [article](https://arxiv.org/abs/1610.08328) below:

    Event generator tuning using Bayesian optimization
    Philip Ilten, Mike Williams, Yunjie Yang
    arXiv:1610.08328


### Set up and run the TuneMC framework

**STEP 1: Install Spearmint and PYTHIA**

1. Follow the instructions on [PYTHIA](http://home.thep.lu.se/Pythia/) (a popular Monte Carlo event generator widely used in High Energy Physics event simulation, e.g. LHC physics) for installation. (Note: no special package flags are needed during Pythia installation.) 
2. Git clone the repository code. 
3. In `./pythia_space`, complile `pythia_gen.cc` with a `PYTHIA8_HOME` argument set to the top-level directory of your installation, i.e. compile it by typing `$ make PYTHIA8_HOME=<path/to/pythia/top-level>` 

The framework should now be ready to use. If you like, you are welcome to familiarize yourself with basic usage of Spearmint and/or PYTHIA by looking at the examples they provide.

**STEP 2: Set up the tune**

The tuning configuration is specified in the `tune_config.json` file at the top-level directory. The user should specify all the variables in this json file. The meaning of these variables are explained below: 

- `N_events`: number of PYTHIA events to generate per query 
- `n_cores`: number of virtual cores to parallelize the PYTHIA event generation, e.g. if `N_events` is 100,000 and `n_cores` is 5, then the generation is parallelized with 5 processes and each core generates 20,000 events 
- `block1(2,3)`: the "block" to tune. The meaning of these blocks is described in our [article](https://arxiv.org/abs/1610.08328). Block1 is a 3-parameter tuning problem, while block2 and block3 have 6 and 11 parameters respectively. Whether to tune a block is specified by a Pythonic boolean, `"True"` or `"False"`. At least one of the three needs to be `"True"`, you can also choose to turn on two or even all three blocks 

**STEP 3: Run the tune**

Now you should be able to run a MC tuning by simply executing the `master.py` code with command `$ python master.py -c <tune_config.json>` at the top-level, where `<tune_config.json>` should be the config file described in the previous step. Additional options for the genetic algorithm tune are `--generations`, `--population-size`, and `--max-events`.
