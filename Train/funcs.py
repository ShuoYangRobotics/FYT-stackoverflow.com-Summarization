import sys
import os
sys.path.append('.')
sys.path.append('..')
import nltk
import math
import re
from BeautifulSoup import BeautifulSoup
from soupselect import select

def myTrim(tt):
    for a in tt:
        if len(a)<2:
            tt.remove(a)
    return tt

class termAna:
    def termFreq(self,word,text):
        tokens = nltk.word_tokenize(text)
        freq = 0
        for token in tokens:
            if word==token:
                freq+=1 

        return (freq,len(tokens))

    def termAppear(self,word,text):
        tokens=[]
        sens = self.sent_tokenizer.tokenize(text)
        for sen in sens:
            tokens+=sen.split(" ")
        for token in tokens:
            try: 
                word = word.encode('utf8')
            except UnicodeDecodeError:
                pass
            if word.lower()==token.lower():
                return True
        return False

    def invrdocFreq(self,word):
        from time import time as time
        t0=time()

        num_appear=1.0
        for text in self.corpus:
            if self.termAppear(word,text):
                num_appear += 1
        idf = math.log(self.corpus_size/num_appear) 

        t1=time()-t0
        print "Time spent on querying the idf of '%s':%f"%(word,t1)
        return idf
    
    def gettfidf(self,word,text):
        a = self.termFreq(word,text)[0]
        b = self.invrdocFreq(word)
        print (a,b) 
        return a*b

    def __init__(self):
        self.sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
        self.corpus_path='data/corpus/'
        self.corpus_size=0
        self.corpus=[]

        listing = os.listdir(self.corpus_path)
        self.corpus_size = len(listing)
        for doc in listing:
            f=open(self.corpus_path+doc,'rb')
            self.corpus.append(f.read())
            f.close()
        
#exclusively for Python!    
class codeAna:
    def __init__(self):
        self.html_path='data/html/'
        self.code=[]
        '''
        listing = os.listdir(self.html_path)
        for doc in listing:
            f=open(self.html_path+doc,'rb')
            soup=BeautifulSoup(f.read())
            self.code+=select(soup,"code")
            f.close()
        '''
    def funcdefGet(self,codeText):
        parseList = {}
        parseList['funcName'] = [] 
        parseList['funcIn'] = []

        codeText = codeText.replace("&gt;&gt;&gt;","\n")
        matches=re.findall('def\s.+:',codeText)
        for match in matches:
            pieces = match.split('(')
            parseList['funcName'].append(pieces[0].split()[1])
            parseList['funcIn'].append(pieces[1].split(')')[0].replace(' ',
            '').split(','))
            
        matches=re.findall('return.*\n?',codeText)
        parseList['funcOut'] = [match.split("return ")[1] for match in matches]
        return parseList

    def moduleGet(self, codeText):
        parseList = {}
        parseList['moduleName'] = [] 

        codeText = codeText.replace("&gt;&gt;&gt;",">>>")
        matches = re.findall('import\s.+\n?\s?',codeText)
        for match in matches:
            module = match.split(" ")[1].split('\n')[0]
            parseList['moduleName'].append(module)
        return parseList
