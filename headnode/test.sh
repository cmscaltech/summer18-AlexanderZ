#!/bin/sh

echo 'running test.sh executable, about to run test.py'
echo $(pwd)
echo $(ls)
python headnode/test.py
echo 'finished running python'