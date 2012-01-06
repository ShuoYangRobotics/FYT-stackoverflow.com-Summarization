import os
import nltk
import re
from chunker import ConsecutiveNPChunker
from nltk.corpus import conll2000
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
chunk = ConsecutiveNPChunker(train_sents)

def main():
    pass


def processTrainData():
    f = open('annotated.txt','rb')
    li = f.read()
    f.close()
    li = li.split('\n')
    q = []
    nq = []
    for line in li:
        body = line.split('<#>')[0]
        body = nltk.word_tokenize(body)
        if len(body)<4:
            continue

        try:
            flag = line.split('<#>')[1]
        except IndexError:
            print line

        if flag == 'Q':
            q.append(body)
        elif flag == 'NQ':
            nq.append(body)
        else:
            pass
    return q,nq


def chunkProcess(sen):
    tmp=[]
    i=0
    while (i<len(sen)):
        item = sen[i]
        print item
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
    tg = nltk.pos_tag(sen)
    posttag = chunkProcess(chunk.tagger.tag(tg)) 
    print sen
    print tg
    print posttag

    hasEx = 0
    hasWWord = 0
    hasInter = 0
    wp = re.compile('W\w?\w?')
    for item in tg:
        if item[0] == "?":
            hasEx =  1
        if wp.match(item[1]) != None:
            hasWWord += 1
