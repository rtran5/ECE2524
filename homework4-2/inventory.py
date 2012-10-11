# ECE 2524 Homework 4 Ryan Tran

import argparse
import sys
import fileinput
import csv
import ast
from operator import itemgetter

parser = argparse.ArgumentParser(description='Homework 4: Inventory Management')
parser.add_argument("-f, --DataFile", dest= 'dataFile', help="help ")
args = parser.parse_args()
partsList = []

def add(arg):
    partsList.append(ast.literal_eval(arg))
    print "The new part was added to the Parts database."
    
def remov(arg):
    partsList.remove_record(ast.literal_eval(arg))
    print "The new part was deleted from the Parts database."

         
def set(arg):
    (change, sep, ident) = arg.partition(" for ")
    print "The new part was set in the Parts database."
    
def list(arg):
    writer = csv.DictWriter(sys.stdout, fieldnames = partsList[0].keys(), delimiter='|')
    if arg == "all":
        writer.writeheader()
        writer.writerows(partsList)
    else:
        try:
            if arg.find("sort") > 0:
                (beginning, sort, fieldname) = arg.partition(" sort by ")
                                
        except KeyError as e:
            print "Error\n"

#Read in "parts" file
try:
    with open(args.dataFile, 'rb') as csvfile:
        line = csv.DictReader(csvfile, delimiter='|')
	for row in line:
            partsList.append(row)

except IOError as e:
    print "The file was not found".format(args.dataFile)
    sys.exit(1)

#process command from terminal
for data in iter(sys.stdin.readline, ''):
    cmd = {'add': add, 'remove': remov, 'set':set, 'list': list}
    (action, space, modifier) = data.partition(" ")
    modifier = modifier.rstrip("\n")
    
    try:
        cmd[action](modifier)
    except KeyError as e:
        print "Invalid command\n".format(action)
    
#Write to file
with open(args.dataFile, 'wb') as out:
    wr = csv.DictWriter(out, fieldnames = partsList[0].keys(), delimiter='|')
    wr.writeheader()
    wr.writerows(partsList)
