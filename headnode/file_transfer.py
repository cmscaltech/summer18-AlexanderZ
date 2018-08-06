import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', help='number for file to save as', type=int)
parser.add_argument('-t', '--total', help='total number of files', type=int)
args = parser.parse_args()

numFiles = len(allFiles)
for i in range(numFiles):
    f = open('./surf2018/f' + str(i) '.txt', 'r')
    contents = f.read()
    print 'contents ' + contents
    f.close()
    f = open((args.num*numFiles + i) + '.txt', 'w+')
    f.write(contents)
    f.close()