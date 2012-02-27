import nltk
import re
from chunker import ConsecutiveNPChunker
from nltk.corpus import conll2000
#train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
#chunk = ConsecutiveNPChunker(train_sents)
class QAPair:
    def __init__(self,id):
        import json
        self._id = id
        f=open('data/questions/question'+str(id)+'.json','rb')
        self._qjson = json.loads(f.read())
        f.close()
        f=open('data/answers/answers'+str(id)+'.json','rb')
        self._ajson = json.loads(f.read())
        f.close()

    def getQBody(self):
        blist = []
        for item in self._qjson:
            try:
                text = item['text']
            except KeyError:
                pass
            for sen in text:
                blist.append(nltk.word_tokenize(sen))
        return blist

    def getABody(self,num):
        blist = []
        for item in self._ajson[num]:
            try:
                text = item['text']
                for sen in text:
                    blist.append(nltk.word_tokenize(sen))
            except KeyError:
                text = item['code']
                blist.append(text)
        return blist

    def parseQ(self):
        rt = []
        wl = self.getQBody()
        for sen in wl:
            tg = nltk.pos_tag(sen)
            rt.append(tg)
        return rt

def chunkProcess(sen):
    tmp=[]
    i=0
    while (i<len(sen)):
        item = sen[i]
        if item[1] == 'O':
            tmp.append(item[0])
            i = i+1
        elif item[1] == 'B-NP':
            end = i
            for j,subitem in enumerate(sen[i+1:]):
                if subitem[1] == "I-NP":
                    end = i + 1 + j
                    continue
                elif subitem[1] == "O":
                    break
            if (end - i)==0:
                tmp.append(item[0])
            else:
                tmp.append(('chunk','NP'))
            i = end+1
    return tmp

def getFeature(sen):
    hasEx = 0
    hasWWord = 0
    hasInter = 0
    wp = re.compile('W\w?\w?')
    for item in sen:
        if item[0] == "?":
            hasEx =  1
        if wp.match(item[1]) != None:
            hasWWord += 1

    posttag = chunkProcess(chunk.tagger.tag(sen)) 


     
test = QAPair(986006)
li = test.parseQ()

