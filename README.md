Caltech SURF 2018: Evolutionary Pythia Tune with Distributed Computing
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

**STEP 2: Set up the cluster**

Place the files in the directory `headnode` onto the head node of the cluster. (The only dependency required on the head node is numpy.) Build an image from the Dockerfile, then edit the `template.jdl` file appropriately to match your system configuration and Docker image path.

**STEP 3: Run the tune**

Run `python headrunner.py` on the head node for the optimization to proceed. It will output fitness histories and parameter histories as `.txt` files in the `headnode` directory.