#math solver using regex, without libraries

import re

expr = str(input("Enter expression: "))
expr = expr.replace(" ", "")     #removes all whitespaces
#print(expr)

if expr[0] not in '+-':     #inserts symbol before term
    expr = '+' + expr

## regex guide :
# [] - set of characters
# . - any character except newline
# ^ - starts with
# * - zero or more occurrences
# ? - zero or one occurrence
# \d - digit
# variables logic - term must have symbol, optional digit, optional variable, optional exponentiation

variables = re.findall('[+-].\d*[\.\d]*[A-Za-z]?[\^\d]*', expr)  #to extract all terms
d = {}

#vs - term with symbol and coefficient, tvs - temp variable symbol, v - value
for vs in variables:
    tvs = vs
    #print(vs)
    sym = re.findall('[A-Za-z][\^]?[\d]?', vs)  #to extract all variables

    if(sym):   #for variables
        k = sym[0]
        tvs = vs.replace(k, '')       #now holds value of coefficient as str
    else:     #for constants
        k = 'constant'

    if len(tvs) > 1:  #variable has coefficient
        v = int(tvs)
    else:
        v = 1
        if tvs[0] == '-':   #negative number
            v = -1
    #print(vs, tvs, k, v)

    if k in d.keys():
        d[k] = d[k] + v
    else:
        d[k] = v

#print(d)

#printing resultant equation
for key in d:
    if d[key] < 0:             #-ve
        if key != 'constant':
            if d[key] == -1:            #only print symbol if coefficient = 1
                print("-", end = "")
                print(key, sep = "", end = " ")
            else:
                print(d[key], key, sep="", end=" ")
        else:
            print(d[key], sep = "", end = " ")
    elif d[key] > 0:            #+ve
        if key != 'constant':
            if d[key] == 1:
                print("+", end="")
                print(key, sep="", end=" ")
            else:
                print("+", end = "")
                print(d[key],key, sep = "", end = " ")
        else:
            print("+", end="")
            print(d[key], sep = "", end = " ")

