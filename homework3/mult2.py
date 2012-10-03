# ECE 2524 Homework 3 Problem 2 Ryan Tran


import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description='Process some numbers.')

parser.add_argument("infile", nargs='*')

parser.add_argument("--ignore-blank", action = "store_true", help="blank lines are skipped")

parser.add_argument("--ignore-non-numeric", action = "store_true", help="non-intergers are skipped")

args= parser.parse_args()

multiply = 1

try:
	for data in fileinput.input(args.infile):
		if args.ignore_non_numeric:		
			if line != "\n":
				multiply *= int(line)
			else:
				print multiply
		elif args.ignore_blank:		
			if line != "\n":
				multiply *= int(line)
			else:
				print multiply

except ValueError as e:
       	e = "Invalid Input"
        sys.stderr.write(e)
        sys.exit(1)
print multiply

