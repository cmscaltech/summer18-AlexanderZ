#!/bin/sh

echo 'cloning github'
git clone https://github.com/quantummind/surf2018.git
echo 'changing into cloned directory'
cd surf2018/pythia_space
echo 'making pythia'
make PYTHIA8_HOME=/root_download/pythia8235
echo 'changing back to surf2018 directory'
cd ../
echo 'running test.sh executable, about to run test.py'
echo $(pwd)
echo $(ls)
python headnode/test.py
echo 'running file transferer'
cd ../
python file_transfer.py
echo 'finished running python'