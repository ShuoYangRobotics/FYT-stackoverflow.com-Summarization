# Same directory hack
import sys
import os
import nltk
import math
from threading import *
from ctypes import *

sys.path.append('.')
sys.path.append('..')

class Analysis:
    def termFreq(self,word,text):
        tokens=[]
        sens = self.sent_tokenizer.tokenize(text)
        for sen in sens:
            tokens+=sen.split(" ")
        freq = 0
        for token in tokens:
            if word.lower()==token.lower():
                freq+=1 

        return (freq,len(tokens))

    class MyThread(Thread):
        def __init__(self,word,sublist,parent,count):
            Thread.__init__(self)
            self.word=word
            self.sublist=sublist
            self.parent=parent
            self.count=count
    
        def run(self):
            for doc in self.sublist:
                f=open(self.parent.corpus_path+doc,'rb')
                text = f.read()
                f.close()
                if self.parent.termFreq(self.word,text)[0] != 0:
                    self.count[0] +=1 


    def invrdocFreq(self,word):
        from time import time as time
        from time import sleep
        t0=time()

        listing = os.listdir(self.corpus_path)
        self.corpus_size = len(listing)
        sub_size = 10
        thrst=[]
        
        for i in range (self.corpus_size/sub_size):
            left = i*sub_size
            right = (i+1)*sub_size-1
            if right > self.corpus_size-1:
                right = self.corpus_size-1
            if left < 0:
                left = 0
            if (left>=right):
                break

            thrst.append(c_int(0))
            a = self.MyThread(word,
            listing[left:right+1],
            self,
            pointer(thrst[-1]))
            a.start()

        total = 1.0
        for item in thrst:
            total +=item.value
        print total


        idf = math.log(self.corpus_size/total) 
        t1=time()-t0
        print "Time spent on querying the idf of '%s':%f"%(word,t1)
        return idf



    def __init__(self):
        self.sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
        self.corpus_path='data/corpus/'
        self.corpus_size=0
        
    
