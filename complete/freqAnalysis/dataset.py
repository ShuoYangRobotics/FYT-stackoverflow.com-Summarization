import os
import json
import sys
sys.path.append('~/Documents/FYT/fyp/')
from pysource import api

questionpath = "../data/questions/"
answerpath = "../data/answers/"
def extractCorpus(start,end):
    qFileList = sorted(os.listdir(questionpath))
    aFileList = sorted(os.listdir(answerpath))
    for i,item in enumerate(qFileList):
        qFileList[i] = questionpath+qFileList[i]
    for i,item in enumerate(aFileList):
        aFileList[i] = answerpath+aFileList[i]

    senList = []
    docList = []
    for i,fileName in enumerate(qFileList[start:end]):
        docList.append([])
        f = open(fileName,'r')
        a = json.load(f)
        for item in a:
            if type(item) == list:
                for myDict in item:
                    if type(myDict) == dict:
                        if myDict.has_key('text'):
                            if myDict['text']!= []:
                                senList.append(myDict['text'][0])
                                docList[i].append(myDict['text'][0])
                    elif type(myDict) == list:
                        for subDict in myDict:
                            if subDict.has_key('text'):
                                if subDict['text']!= []:
                                    senList.append(subDict['text'][0])
                                    docList[i].append(subDict['text'][0])
            elif type(item) == dict:
                if item.has_key('text'):
                    if item['text']!= []:
                        senList.append(item['text'][0])
                        docList[i].append(item['text'][0])
    for i,fileName in enumerate(aFileList[start:end]):
        f = open(fileName,'r')
        a = json.load(f)
        for item in a:
            if type(item) == list:
                for myDict in item:
                    if type(myDict) == dict:
                        if myDict.has_key('text'):
                            if myDict['text']!= []:
                                senList.append(myDict['text'][0])
                                docList[i].append(myDict['text'][0])
                    elif type(myDict) == list:
                        for subDict in myDict:
                            if subDict.has_key('text'):
                                if subDict['text']!= []:
                                    senList.append(subDict['text'][0])
                                    docList[i].append(subDict['text'][0])
            elif type(item) == dict:
                if item.has_key('text'):
                    if item['text']!= []:
                        senList.append(item['text'][0])
                        docList[i].append(item['text'][0])
    return senList,docList

def getTFIDF(senList,docList):
    porter = nltk.PorterStemmer()
    termFreq = defaultdict(int)
    totalCount = 0.0

    invDocFreq = defaultdict(int)       
    totalDoc = float(len(docList))
    print totalDoc
    listDocTokens = []
    for doc in docList:
        docTokens = []
        for sen in doc:
            tokens = nltk.word_tokenize(sen)
            tokens = [porter.stem(t).lower() for t in tokens]
            docTokens+=tokens
        listDocTokens.append(set(docTokens))

    print 'get list of tokens'

    for sen in senList:
        tokens = nltk.word_tokenize(sen)
        tokens = [porter.stem(t).lower() for t in tokens]
        for t in tokens:
            termFreq[t]+=1
            totalCount+=1

    for item in termFreq.keys():
        for docTokens in listDocTokens:
            if item in docTokens:
                invDocFreq[item]+=1
    print 'done'

    tfidf = defaultdict(int)       
    for item in termFreq.keys():
        termFreq[item] = termFreq[item]/totalCount
        invDocFreq[item] = math.log(totalDoc/invDocFreq[item])
        tfidf[item] = termFreq[item]*invDocFreq[item]

    return tfidf

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


if __name__=="__main__":
    import nltk
    import math
    from collections import defaultdict
    deb = None
    sen,doc = extractCorpus(0,99999)
    tfidf = getTFIDF(sen,doc)
