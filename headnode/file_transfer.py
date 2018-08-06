import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', help='batch number', type=int)
parser.add_argument('-t', '--total', help='total number of files (batch size)', type=int)
args = parser.parse_args()

for i in range(args.total):
    f = open('./surf2018/f' + str(i) + '.txt', 'r')
    contents = f.read()
    print 'contents ' + contents
    f.close()
    f = open(str(args.num*args.total + i) + '.txt', 'w+')
    f.write(contents)
    f.close()