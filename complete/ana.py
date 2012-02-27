import os
import json
import sys
mypysourcepath = '/home/paul/Documents/FYT/fyp/'
sys.path.append(mypysourcepath)
from pysource import api

questionpath = "data/questions/"
answerpath = "data/answers/"
htmlpath = "data/html/"
annotatedpath = "annotated/"

"""
This function returns a list of common english words
the wordlist is obtained from ftp://ftp.cs.cornell.edu/pub/smart/english.stop
    fQ = set(fQ)
    aQ = set(aQ)
    vQ = set(vQ)
    cQ = set(cQ)
"""
def getCommonWord():
    f = open("english.stop",'r')
    li = []
    for line in f:
        li.append(line.split("\n")[0])
    return li

"""
This function returns a list of question id
"""
def getIDList():
    f = open("worth_list.txt",'r')
    li = []
    for line in f:
        li.append(line.split("\n")[0])
    return li

def getDataList():
    qFileList = sorted(os.listdir(questionpath))
    aFileList = sorted(os.listdir(answerpath))
    for i,item in enumerate(qFileList):
        qFileList[i] = questionpath+qFileList[i]
    for i,item in enumerate(aFileList):
        aFileList[i] = answerpath+aFileList[i]
    return qFileList, aFileList

"""
This function can return the question text or answer text 
This input 'type' should define wheather to show question 
or show answer
when type is 1, show question
when type is 0, show answer
"""
def getData(qId, showType):
    if showType == 1:
        search = questionpath+"question"+qId+".json"
    elif showType == 0:
        search = answerpath+"answers"+qId+".json"
    f = open(search,'r')
    a = json.load(f)
    return a

"""
This function get the html code of the give question ID
"""
def getHTML(qId):
    search = htmlpath+"python"+qId+".html"
    f = open(search,'r')
    a = f.read()
    return a

"""
This function takes in a json file, 
output a list of sentences in that json file
"""
def getSentenceList(jsonFile):
    senList = []
    for item in jsonFile:
        if type(item) == list:
            for myDict in item:
                if type(myDict) == dict:
                    if myDict.has_key('text'):
                        if myDict['text']!= []:
                            for thisSen in myDict['text']:
                                senList.append(thisSen)
                    if myDict.has_key('lis'):
                        for li in myDict['lis']:
                            senList.append(li['text'])
                elif type(myDict) == list:
                    for subDict in myDict:
                        if subDict.has_key('text'):
                            if subDict['text']!= []:
                                for thisSen in subDict['text']:
                                    senList.append(thisSen)
                        if subDict.has_key('lis'):
                            for li in subDict['lis']:
                                senList.append(li['text'])
        elif type(item) == dict:
            if item.has_key('text'):
                if item['text']!= []:
                    for thisSen in item['text']:
                        senList.append(thisSen)
            if item.has_key('lis'):
                for li in item['lis']:
                    senList.append(li['text'])
    return senList

"""
This function takes in a list of sentences, 
then parse the sentence to remove common words and stopwords
change each sentence to a list of tokens. 
"""
def parseSenList(senList):
    import re
    common = getCommonWord()
    #porter = nltk.PorterStemmer()
    tokenList = []
    for sen in senList: 
        tokens = nltk.word_tokenize(sen)
        #tokens = [porter.stem(t).lower() for t in tokens if
        tokens = [t.lower() for t in tokens if
        bool(re.match(r"[a-zA-Z]+$",t))==True and t not in common]
        tokenList.append(tokens)
    return tokenList

"""
This function inputs a json file
outputs the code pieces contained in the file
"""
def getCodeList(jsonFile):
    senList = []
    for item in jsonFile:
        if type(item) == list:
            for myDict in item:
                if type(myDict) == dict:
                    if myDict.has_key('code'):
                        if myDict['code']!= []:
                            senList.append(myDict['code'])
                elif type(myDict) == list:
                    for subDict in myDict:
                        if subDict.has_key('code'):
                            if subDict['code']!= []:
                                senList.append(subDict['code'])
        elif type(item) == dict:
            if item.has_key('code'):
                if item['code']!= []:
                    senList.append(item['code'])
    return senList

def parseSource_File(filename):
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

"""
This function preprocess the string that to be parse as code piece
"""
def preProCode(string):
    string = nltk.clean_html(string)
    hasSym = bool(re.match("&gt;&gt;&gt;",string))
    if hasSym:
        t0 = string.split("\n")
        lenT = len(t0)
        for i in range(len(t0)):
            if i>lenT:
                break
            else:
                for j in range(i+1,lenT):
                    if j>=len(t0):
                        break
                    if t0[i] == t0[j]:
                        t0.pop(j) 
                        lenT -= 1
                try:
                    t0[i] = t0[i].replace("&gt;&gt;&gt; ","")
                except IndexError:
                    #print t0
                    pass
        string = t0
    else:
        string = string.split("\n")
    return string

"""
This function can parse the code to know what packages or modules are imported
"""
def cparPack(string):
    package = []
    funcs = []
    try:
        node = api.parse_source(string)
        import_names = list(api.get_import_names(node))
        for item in import_names:
            if len(item.split('.')) >1:
                pac = item.split('.')[0]
                fun = item.split('.')[1]
                package.append(pac)
                funcs.append(fun)
            else:
                package.append(item)
    except SyntaxError:
        if type(string)!=type([]):
            string = string.split("\n")

        for item in string:
            try:
                node = api.parse_source(item)
                #print item
                import_names = list(api.get_import_names(node))
                for item in import_names:
                    if len(item.split('.')) >1:
                        pac = item.split('.')[0]
                        fun = item.split('.')[1]
                        package.append(pac)
                        funcs.append(fun)
                    else:
                        package.append(item)
            except SyntaxError:
                pass
    #except UnicodeEncodeError as e:
        #print string
        #pass
        
    return list(set(package)),list(set(funcs))

"""
This function can parse the code to know what functions are defined and what
variables are declared
input maybe a list 
"""
def cparFuncs(string):
    funcName = []
    varName = []
    argName = []
    className = []
    for item in string:
        if bool(re.match(r"^\s*class\s",item))==True:
            t0 = item.split("class")[1].split("(")[0].split(":")[0].strip() 
            #print "a class----",t0 
            className.append(t0.strip())
        if bool(re.match(r"^\s*def\s",item))==True:
            t0 = item.split("def")[1].split("(")[0].strip() 
            #print "a func def----",t0 
            funcName.append(t0.strip())
        if bool(re.match(r"^.*\(\w+\).*$",item))==True:
            t0 = item.split("(")[1].split(")")[0].strip() 
            #print "args ----",t0 
            argName.append(t0.strip())
        if bool(re.match(r"\w+[.]\w+[(].+[)]",item))==True:
            t0 = item.split("(")[0]
            t1 = t0.split(".")[0]
            t2 = t0.split(".")[1]
            className.append(t1.strip())
            funcName.append(t2.strip())
        if bool(re.match(r"^.*\s*=\s*.*$",item))==True:
            t0 = re.split(r"[+\*]?=", item)[0] 
            #print "assign----",t0 
            t2 = t0.split(",")
            if len(t2)>=3:
                for item in t2:
                    varName.append(item.strip())
            else:
                varName.append(t0)
    return funcName, varName, argName, className




def extractGraph_corpus(start,end):
    qFileList = sorted(os.listdir(questionpath))
    aFileList = sorted(os.listdir(answerpath))
    for i,item in enumerate(qFileList):
        qFileList[i] = questionpath+qFileList[i]
    for i,item in enumerate(aFileList):
        aFileList[i] = answerpath+aFileList[i]

    senList = []
    for i,fileName in enumerate(qFileList[start:end]):
        f = open(fileName,'r')
        a = json.load(f)
        for item in a:
            if type(item) == list:
                for myDict in item:
                    if type(myDict) == dict:
                        if myDict.has_key('code'):
                            if myDict['code']!= []:
                                senList.append(myDict['code'])
                    elif type(myDict) == list:
                        for subDict in myDict:
                            if subDict.has_key('code'):
                                if subDict['code']!= []:
                                    senList.append(subDict['code'])
            elif type(item) == dict:
                if item.has_key('code'):
                    if item['code']!= []:
                        senList.append(item['code'])

    for i,fileName in enumerate(aFileList[start:end]):
        f = open(fileName,'r')
        a = json.load(f)
        for item in a:
            if type(item) == list:
                for myDict in item:
                    if type(myDict) == dict:
                        if myDict.has_key('code'):
                            if myDict['code']!= []:
                                senList.append(myDict['code'])
                    elif type(myDict) == list:
                        for subDict in myDict:
                            if subDict.has_key('code'):
                                if subDict['code']!= []:
                                    senList.append(subDict['code'])
            elif type(item) == dict:
                if item.has_key('code'):
                    if item['code']!= []:
                        senList.append(item['code'])
    pack_count = defaultdict(int)
    for item in senList:
        item = nltk.clean_html(item)
        try:
            packs,funcs = cparPack(item.decode("utf8"))
            for pack in packs:
                pack_count[pack] +=1
        except SyntaxError:
            pass
        except UnicodeEncodeError:
            pass 
    return pack_count



def extractTFIDF_corpus(start,end):
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
                                for thisSen in myDict['text']:
                                    senList.append(thisSen)
                                    docList[i].append(thisSen)
                        if myDict.has_key('lis'):
                            for li in myDict['lis']:
                                senList.append(li['text'])
                                docList[i].append(li['text'])
                    elif type(myDict) == list:
                        for subDict in myDict:
                            if subDict.has_key('text'):
                                if subDict['text']!= []:
                                    for thisSen in subDict['text']:
                                        senList.append(thisSen)
                                        docList[i].append(thisSen)
                            if subDict.has_key('lis'):
                                for li in subDict['lis']:
                                    senList.append(li['text'])
                                    docList[i].append(li['text'])
            elif type(item) == dict:
                if item.has_key('text'):
                    if item['text']!= []:
                        for thisSen in item['text']:
                            senList.append(thisSen)
                            docList[i].append(thisSen)
                if item.has_key('lis'):
                    for li in item['lis']:
                        senList.append(li['text'])
                        docList[i].append(li['text'])
            
    for i,fileName in enumerate(aFileList[start:end]):
        f = open(fileName,'r')
        a = json.load(f)
        for item in a:
            if type(item) == list:
                for myDict in item:
                    if type(myDict) == dict:
                        if myDict.has_key('text'):
                            if myDict['text']!= []:
                                for thisSen in myDict['text']:
                                    senList.append(thisSen)
                                    docList[i].append(thisSen)
                        if myDict.has_key('lis'):
                            for li in myDict['lis']:
                                senList.append(li['text'])
                                docList[i].append(li['text'])
                    elif type(myDict) == list:
                        for subDict in myDict:
                            if subDict.has_key('text'):
                                if subDict['text']!= []:
                                    for thisSen in subDict['text']:
                                        senList.append(thisSen)
                                        docList[i].append(thisSen)
                            if subDict.has_key('lis'):
                                for li in subDict['lis']:
                                    senList.append(li['text'])
                                    docList[i].append(li['text'])
            elif type(item) == dict:
                if item.has_key('text'):
                    if item['text']!= []:
                        for thisSen in item['text']:
                            senList.append(thisSen)
                            docList[i].append(thisSen)
                if item.has_key('lis'):
                    for li in item['lis']:
                        senList.append(li['text'])
                        docList[i].append(li['text'])
    return senList,docList

def getTFIDF(senList,docList):
    pattern = re.compile("[a-zA-Z]*")
    porter = nltk.PorterStemmer()
    termFreq = defaultdict(int)
    totalCount = 0.0

    common = getCommonWord()


    invDocFreq = defaultdict(int)       
    totalDoc = float(len(docList))
    print totalDoc
    listDocTokens = []
    for doc in docList:
        docTokens = []
        for sen in doc:
            tokens = nltk.word_tokenize(sen)
            tokens = [porter.stem(t).lower() for t in tokens if
            bool(re.match(r"[a-zA-Z]+$",t))==True and t not in common]
            docTokens+=tokens
        listDocTokens.append(set(docTokens))

    print 'get list of tokens'

    for sen in senList:
        tokens = nltk.word_tokenize(sen)
        tokens = [porter.stem(t).lower() for t in tokens if
        bool(re.match(r"[a-zA-Z]+$",t))==True and t not in common]
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

"""
this function utilizes the above functions to get a dictionary of 
modules that imported in the code pieces.
packs, a dictionary will be the output
"""
def getFrequentPacks():
    packs = extractGraph_corpus(0,9999)
    fdist = nltk.FreqDist(packs)
    sum = 0.0
    l=[]
    for item in fdist.values()[0:100]:
            sum+=item
    for item in fdist.values()[0:100]:
        l.append(item/sum)
    pylab.plot(range(0,100),l)
    pylab.xticks(numpy.arange(0,100),fdist.keys()[0:100],rotation='vertical')
    pylab.show()
    return packs

"""
this function returns a list of tf-idf
"""
def obtainTFIDF():
    sen,doc = extractTFIDF_corpus(0,99999)
    tfidf = getTFIDF(sen,doc)
    return tfidf

def plotTFIDF(tfidf):
    fdist = nltk.FreqDist(tfidf)
    sum = 0.0
    l=[]
    for item in fdist.values()[0:100]:
            sum+=item
    for item in fdist.values()[0:100]:
        l.append(item/sum)
    pylab.plot(range(0,100),l)
    pylab.xticks(numpy.arange(0,100),fdist.keys()[0:100],rotation='vertical')
    pylab.show()

"""
This function replace a string with a HTML tag,
it is used to annotate the HTML code
"""
def annotate(word):
    t1 = u"<span style=\"background-color:yellow;\">"+word+u"</span>"
    return t1

"""
This function annote the html file with identified function keywords and so on.
"""
def htmlAnnotate(html, keyList):
    common = getCommonWord()
    soup = BS(''.join(html))
    for j,item in enumerate(soup.contents):
        try:
            count = 0
            sen = nltk.clean_html(str(item))
            if item.name == "pre":
                continue
            if not isinstance(item, NavigableString):
                children = item.findChildren()
                for child in children:
                    if child.name == "code" or child.name == "a":
                        print nltk.clean_html(str(child))
                        keyList.append(nltk.clean_html(str(child).decode('utf8')))

            tokens = nltk.word_tokenize(sen)
            for i,token in enumerate(tokens):
                if token == "?":
                    continue
                for item2 in keyList:
                    try:
                        token = token.split("(")[1]
                    except IndexError:
                        token = token.split(")")[0]
                    try:
                        if bool(re.match(item2,token.strip())):
                            if token != "." and token not in common:
                                tokens[i] = annotate(token)
                                count += 1
                    except:
                        pass
            try: 
                newSen = ''
                for token in tokens:
                        newSen += token
                        newSen += " "
                soup.contents[j].setString(newSen)
                soup.contents[j]['id'] = count
                soup.contents[j]['class'] = "sentence"
            except UnicodeDecodeError:
                pass
        except AttributeError:
            pass
    return soup

"""
This function get an ID and annotates the corresponding document
"""
def annotateID(testID):
    myDataQ = getData(testID,1)
    myDataA = getData(testID,0)
    myCodeListQ = getCodeList(myDataQ)
    myCodeListA = getCodeList(myDataA)
    myHtml = getHTML(testID)

    
    t1 = []
    packQ = []
    funcQ = []
    for item in myCodeListQ:
        try:
            p,f = cparPack(nltk.clean_html(item))
            packQ += p 
            funcQ += f
        except SyntaxError:
            pass
        t1 += preProCode(item)
    fQ,aQ,vQ,cQ = cparFuncs(t1) 
    packQ,funcQ = cparPack(t1)
    fQ = list(set(fQ))
    aQ = list(set(aQ))
    vQ = list(set(vQ))
    cQ = list(set(cQ))

    combQ = []
    for cItem in cQ:
        for fItem in fQ:
            combQ.append(cItem+"."+fItem) 

    t2 = []
    packA = []
    funcA = []
    for item in myCodeListA:
        try:
            p,f = cparPack(nltk.clean_html(item))
            packA += p 
            funcA += f
        except SyntaxError:
            pass
        t2 += preProCode(item)
    fA,aA,vA,cA = cparFuncs(t2) 
    fA = list(set(fA))
    aA = list(set(aA))
    vA = list(set(vA))
    cA = list(set(cA))

    combA = []
    for cItem in cA:
        for fItem in fA:
            combA.append(cItem+"."+fItem) 

    keyList = \
    list(set(fQ+fA+aQ+aA+vQ+vA+cQ+cA+combQ+combA+packQ+packA+funcQ+funcA))
    mySoup = htmlAnnotate(myHtml, keyList)
    f = open(annotatedpath+"annotated"+testID+".html",'w')

    try:
        mySoup =HTMLParser.HTMLParser().unescape(str(mySoup).decode("utf8")) 
    except UnicodeEncodeError:
        pass

    b = "<style>.sentence:hover{background-color:red;}</style>"
    a = PQ("<html><head>"+b+"</head><body>"+str(mySoup.encode("utf8"))+"</body></html>") 
    f.write(str(a))
    f.close()
    return mySoup,keyList,myHtml

if __name__=="__main__":
    import HTMLParser
    import nltk
    import math
    import re
    import pylab
    import numpy
    import string as StrLib
    from BeautifulSoup import BeautifulSoup as BS
    from pyquery import PyQuery as PQ
    from collections import defaultdict
    from BeautifulSoup import NavigableString
    idList = getIDList()
    qFileList, aFileList = getDataList()

    #total = float(len(idList))
    #for i,item in enumerate(idList):
    #    annotateID(item)
    #    print "%4.3f completed."%(i/total*100)
