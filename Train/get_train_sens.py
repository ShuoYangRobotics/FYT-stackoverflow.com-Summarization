import nltk
import os
import csv
class Q:
    def __init__(self,fileName):
        self.path = './data/questions/'
        import json
        self._id = id
        f=open(self.path+fileName,'rb')
        self._qjson = json.loads(f.read())
        f.close()

    def getQBody(self):
        blist = []
        try:
            for item in self._qjson:
                try:
                    text = item['text']
                except KeyError:
                    pass
                for sen in text:
                    blist.append(sen)
        except TypeError:
            pass
        return blist

dirlist = os.listdir('./data/questions/')     
outlist = open('list.txt','wb')
for item in dirlist:
    test = Q(item)
    tmplist = test.getQBody()
    for i,sen in enumerate(tmplist):
        if len(sen)<10:
            continue
        if sen.strip() == tmplist[i-1].strip():
            continue
        if sen.strip() == tmplist[i-2].strip():
            continue
        try:
            outlist.write(sen+'<#>I\n')
        except UnicodeEncodeError:
            outlist.write(sen.encode('utf8')+'<#>I\n')



