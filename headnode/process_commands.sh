#!/bin/sh

echo 'Starting python runs'

# run condor submissions
condor_submit submit.jdl
populationSize=$1
echo "expecting $populationSize population members"
outputSize=0
while [ $outputSize -lt $populationSize ]
do
    outputSize=`ls fitnesses | wc -l`
    echo "currently have $outputSize fitness files"
#     echo $(condor_q)
    sleep 30
done

echo 'All files found'