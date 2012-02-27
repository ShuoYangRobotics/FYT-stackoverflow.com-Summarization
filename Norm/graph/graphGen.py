import sys
sys.path.append('~/Documents/FYT/fyp/')
from pysource import api
import os
import json
questionpath = "../data/questions/"
answerpath = "../data/answers/"

def parseFile(filename):
    with open(filename) as f: 
        node = api.parse_source(f.read())
    import_names = list(api.get_import_names(node))
    package = []
    funcs = []
    for item in import_names:
        if len(item.split('.')) >1:
            pac = item.split('.')[0]
            fun = item.split('.')[1]
            package.append(pac)
            funcs.append(fun)
        else:
            package.append(item)
    return set(package),set(funcs)

def parseCode(string):
    node = api.parse_source(string)
    import_names = list(api.get_import_names(node))
    package = []
    funcs = []
    for item in import_names:
        if len(item.split('.')) >1:
            pac = item.split('.')[0]
            fun = item.split('.')[1]
            package.append(pac)
            funcs.append(fun)
        else:
            package.append(item)
    return set(package),set(funcs)

