# ECE 2524 Homework 2 Problem 1 Ryan Tran


print "ACCOUNT INFORMATION FOR BLACKSBURG RESIDENTS"


with open('/etc/passwd', 'r') as f:
    for line in f:	
	str1 = line
	print str1.split(':')[0], "	" , str1.split(':')[6]
	
	
        
