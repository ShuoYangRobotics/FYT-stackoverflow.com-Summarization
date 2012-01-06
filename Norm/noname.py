import sys
import os
import nltk
import math
import csv
import json
from funcs import *

sys.path.append('.')
sys.path.append('..')

def codeCount(ajson,id):
    def myTrim(tt):
        for a in tt:
            if len(a)<2:
                tt.remove(a)
        return tt
    code_list=[]
    line_sum=0
    for item in ajson:
        for li in item:
            try:
                li['code'] = li['code'].replace("&gt;",">")
                tmp = nltk.clean_html(li['code'])
                tmp = tmp.split("\n")
                tmp = myTrim(tmp)
                line_sum += len(tmp)
                code_list.append(tmp)
            except KeyError:
                pass
    print "doc %d code count:"%id
    print "%d answers"%len(ajson)
    print "%d pieces of code"%len(code_list)
    print "total %d lines of code"%line_sum
    return {'num':len(code_list), 'count':line_sum}

f=open('data/questions/question'+str(25665)+'.json','rb')
qjson1 = json.loads(f.read())
f.close()

f=open('data/questions/question'+str(56011)+'.json','rb')
qjson2 = json.loads(f.read())
f.close()

def quesAna(qjson):
    pass 


def getWorth():
    id_list= []
    tmpCSV = csv.reader(open("python.csv",'rb'))
    for row in tmpCSV:
        id_list.append(row[0])

    worth_list=[]
    for item in id_list:
        f=open('data/answers/answers'+item+'.json','rb')
        ajson = json.loads(f.read())
        f.close()
        tmp = codeCount(ajson,int(item))
        if (tmp['count']>0 and 
            tmp['num']>0 and 
            tmp['count']/float(tmp['num'])>4):
            print "doc %d is worth to read"%int(item)
            worth_list.append(int(item))

    return worth_list
