# Same directory hack
import sys
sys.path.append('.')

import numpy
import csv
import stackexchange
from BeautifulSoup import BeautifulSoup
from soupselect import select

site = stackexchange.Site(stackexchange.StackOverflow)
site.be_inclusive()

id_list = []
tmpCSV = csv.reader(open("polls.csv",'rb'))
for row in tmpCSV:
    id_list.append(row[0])
id = id_list[numpy.random.randint(1, len(id_list))]

getQuestion = True
try:
    question = site.question(id)
except ValueError:
    getQuestion = False

if getQuestion:
    body=""
    body+="<h3>Question (ID-"+str(id)+"):</h3>"
    body+=question.body
    body+="<br />"
    body+="<h3>Answers (Total-"+str(len(question.answers))+"):</h3>"
    for i, answer in enumerate(question.answers):
        num="<b>"+str(i)+"</b>"
        body+= num
        body+=answer.body
        body+="<br />"

    body = body.encode('utf8')
    f=open('polls'+str(id)+'.html','wb')
    f.write(body)
    f.close()
else:
    print "no question associated with this id(%d)"%id


