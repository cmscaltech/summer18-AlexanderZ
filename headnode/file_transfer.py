import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', help='number for file to save as')
args = parser.parse_args()

f = open('./surf2018/f.txt', 'r')
contents = f.read()
print 'contents ' + contents
f.close()
f = open(args.num + '.txt', 'w+')
f.write(contents)
f.close()