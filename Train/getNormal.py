# Same directory hack
import sys
sys.path.append('.')
sys.path.append('..')

import numpy
import csv
import nltk
import stackexchange
from BeautifulSoup import BeautifulSoup
from soupselect import select
from funcs import *

class myParser:
    """""""""""""""""""""""""""""""""""""""
             FUNCTIONS DEFINITION
    """""""""""""""""""""""""""""""""""""""
    def senParse(self,metaSen,senID):
        parseSen={}
        parseSen['senID'] = senID
        #handle the case where metaSen contains a single link or image
        try:
            if metaSen.text == '':
                children = metaSen.findChildren()
                if len(children) == 1:
                    parseSen['tag'] = children[0].name
                    if children[0].name == 'img':
                        for attr in children[0].attrs:
                            if attr[0] == 'src':
                                parseSen['src'] = attr[1]
                    elif children[0].name == 'a': 
                        for attr in children[0].attrs:
                            if attr[0] == 'href':
                                parseSen['href'] = attr[1]
                else:
                    '''
                        Here assume only one element in one such a <p>
                        will it cause potential problems? Maybe, we will see
                        Just note down this concern here TODO
                    '''
                    pass
                return parseSen
            else:
                tmtxt = ''
                tmp = metaSen.contents
                for item in tmp:
                    try:
                        s = item.text
                    except AttributeError:
                        s = item
                    tmtxt += s

                tt = nltk.sent_tokenize(tmtxt)
                tt = myTrim(tt)
                parseSen['text'] = tt
                parseSen['tag'] = metaSen.name

                return parseSen
        except AttributeError:
            parseSen['text'] = metaSen
            parseSen['tag'] = 'none'
            return parseSen



    def codeParse(self,metaCode,senID):
        parseCode = {}
        parseCode['code'] = metaCode.prettify()
        parseCode['senID'] = senID
        return parseCode

    def blockParse(self,text):
        parseSens = []
        senId = 0
        metaAll = BeautifulSoup(text)

        for item in metaAll.contents:
            try:
                myType = item.name
            except AttributeError:
                myType = 'str'

            if myType == "p" or myType == "h2":
                parseSens.append(self.senParse(item,senId))
                senId += 1
            elif myType == "pre":
                parseSens.append(self.codeParse(item,senId))
                senId += 1
            elif myType == "ul":
                parseUl = {}
                lis= myTrim(item.contents)
                parseUl['tag'] = myType
                parseUl['num'] = len(lis)
                parseUl['lis'] = []
                for li in lis:
                    parseUl['lis'].append(self.senParse(li.contents[0],senId))
                    senId += 1
                parseSens.append(parseUl)
            else:
                pass
        return parseSens

    def getPage(self,id):
        self.aList = []
        getQuestion = True
        self.id=id
        try:
            question = self.site.question(id)
        except ValueError:
            getQuestion = False

        if getQuestion:
            self.qTree = self.blockParse("<h2>"+question.title+"</h2>"+"<br />"+question.body)
        else:
            print "no question associated with this id - ",
            print id

    def dump(self):
        import json
        a = json.dumps(self.qTree)
        f=open('data/questions/question'+str(self.id)+'.json','wb')
        f.write(a)
        f.close()

    def getFile(self):
        import time
        id_list = []
        tmpCSV = csv.reader(open("python.csv",'rb'))
        for row in tmpCSV:
            id_list.append(row[0])
        for item in id_list[78:]:
            self.getPage(item)
            self.dump()
            print "successfully fetched page with id %d"%int(item)
            time.sleep(0.5)

    """""""""""""""""""""""""""""""""""""""
         MAIN ENTRY POINT DEFINITION
    """""""""""""""""""""""""""""""""""""""
    def __init__(self):
        self.site = stackexchange.Site(stackexchange.StackOverflow)
        self.site.be_inclusive()
        self.body=""
        self.raw=""
        self.qTree = None
        self.aList = []
        self.id=0
        self.prob=[]

