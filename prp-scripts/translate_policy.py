#!/usr/bin/env python

# This file was edit by
# Elad Mintzer 203768460

import re, pprint
import sys

input_file_name = sys.argv[1]
output_policy_name = input_file_name.replace(".out",".json")
output_map_name = input_file_name.replace(".out",".sat_mapper")

def read_file(file_name):
    """Return a list of the lines of a file."""
    f = open(file_name, 'r')
    file_lines = [line.rstrip("\n") for line in f.readlines()]
    f.close()
    return file_lines

def get_lines(file_name, lower_bound = None, upper_bound = None):
    """ Gets all of the lines between the regex lower bound and upper bound. """

    toReturn = []

    # Get the file
    f = open(file_name, 'r')
    file_lines = [line.rstrip("\n") for line in f.readlines()]
    f.close()

    if not lower_bound:
        accepting = True
    else:
        accepting = False
        pattern_low = re.compile(lower_bound, re.MULTILINE)

    if not upper_bound:
        upper_bound = 'THIS IS SOME CRAZY STRING THAT NOONE SHOULD EVER HAVE -- NARF!'

    pattern_high = re.compile(upper_bound, re.MULTILINE)

    for line in file_lines:
        if accepting:
            if pattern_high.search(line):
                return toReturn

            toReturn.append(line)
        else:
            if pattern_low.search(line):
                accepting = True

    return toReturn

index = 0
var_lines = get_lines('output', lower_bound = 'end_metric', upper_bound = 'begin_state')

num_vars = int(var_lines[index])
index += 1

def parse_var(lines, index):

    assert 'begin_variable' == lines[index]
    index += 1

    name = lines[index]
    index += 1

    assert '-1' == lines[index]
    index += 1

    num_vals = int(lines[index])
    index += 1

    vals = []
    for i in range(num_vals):
        if 'NegatedAtom' == lines[index][:11]:
            vals.append("not(%s)" % lines[index].split('Atom ')[-1])
        else:
            vals.append(lines[index].split('Atom ')[-1])
        index += 1

    assert 'end_variable' == lines[index]
    index += 1

    if 2 == len(vals):
        if '<none of those>' == vals[0]:
            vals[0] = "!%s" % vals[1]
        elif '<none of those>' == vals[1]:
            vals[1] = "!%s" % vals[0]

    return (name, vals, index)


mapping = {}

for i in range(num_vars):
    (name, vals, index) = parse_var(var_lines, index)
    for j in range(len(vals)):
        mapping["%s:%s" % (name, j)] = vals[j]

# print "Mapping:\n"
# print '\n'.join(["  %s\t<-> \t %s" % (k,mapping[k]) for k in sorted(mapping.keys())])
# print

def translate_lines(lines):
    di = dict()
    d2 = []
    key = "Nand"
    last_d = 0
    my_list=[]

    for line in lines:
        if 'If' == line[:2]:
            my_list = [mapping[item] for item in line.split(' ')[2:]]
            # print "If holds: %s" % '/'.join(my_list)
            key = ' & '.join(my_list)

        elif "Execute" in line:
            # print line
            my_line = line.replace("Execute: ","").split(" /")[0]
            my_line_st = "({})".format(my_line)
            d = int(line.split("/ d=")[-1]) * 10
            if d <= last_d:
                d = last_d + 1  
            # TODO: replace when needed:
            #d[key] = my_line
            #di[my_line_st] = [key,d]
            di[my_line_st] = [my_list,d]
            d2.append((key.replace("&","and"), my_line_st,d))
            last_d = d

    return di,d2

policy_lines = read_file(input_file_name)
di,d2 = translate_lines(policy_lines)

import json
print "process policy file to "+ output_policy_name
with open(output_policy_name, 'w') as pp:
    json.dump(di, pp)
print "process mapper file to "+ output_map_name
with open(output_map_name, 'w') as mp:
    json.dump(mapping, mp)

 
# DEBUG
# debug_output_policy_name = output_policy_name.replace(".json","_code.py")
# d2.sort(key=lambda tup: -tup[2])

# print "process debug policy file to "+ debug_output_policy_name
# with open(debug_output_policy_name, 'w') as dp:
#     for state, action,d in d2:
#         dp.write("if({}):\n\treturn {} #{}\n".format(state, action,d))
#     json.dump(d2, dp)

 