#!/bin/sh

echo 'Starting python runs'

# run condor submissions
bash commands.txt
populationSize=`ls submissions | wc -l`
echo "expecting $populationSize population members"
outputSize=0
while [ $outputSize -lt $populationSize ]
do
    outputSize=`ls fitnesses | wc -l`
    echo "currently have $outputSize fitness files"
    sleep 2
done

echo 'All files found'