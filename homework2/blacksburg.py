# ECE 2524 Homework 2 Problem 2 Ryan Tran

print "ACCOUNT INFORMATION FOR BLACKSBURG RESIDENTS"
import sys
if len(sys.argv) == 2:
	f = open(sys.argv[1], 'r')
	for line in f:
		str1 = line
		if 'Blacksburg' in str1:
			print str1.split()[4] + ", " + str1.split()[1] + ", " + str1.split()[0] + ", " + str1.split()[2] 
