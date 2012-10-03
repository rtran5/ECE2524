# ECE 2524 Homework 3 Problem 1 Ryan Tran

import sys
import argparse

parser = argparse.ArgumentParser(description='Process some numbers.')
args= parser.parse_args()
multiply = 1

try:
	for line in iter(sys.stdin.readline, ''):
		if line != "\n":
			multiply *= int(line)
		else:
			print multiply

except ValueError as e:
       	e = "Invalid Input"
        sys.stderr.write(e)
        sys.exit(1)
print multiply

