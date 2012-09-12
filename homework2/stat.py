# ECE 2524 Homework 2 Problem 3 Ryan Tran
print "ACCOUNT SUMMARY"
import sys
if len(sys.argv) == 2:
	f = open(sys.argv[1], 'r')
	money = []
	for line in f:
		x = line.split()
		money.append(float(x[2]))
print "Total amount owed = ", sum(money)
print "Average amount owed = ", sum(money)/len(money)
print "Maximum amount owed = ", max(money), " by "
print "Minimum amount owed = ", min(money), " by "
 
