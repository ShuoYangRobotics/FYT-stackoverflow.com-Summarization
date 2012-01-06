import csv
annolist =[]
todo = open("list.txt",'rb')
for row in todo:
    annolist.append(row)
todo.close()
yy=2442
total = len(annolist)
for i,item in enumerate(annolist[yy:]):
    tmp = item.split('\n')[0].split("<#>")
    print "=========================="
    print "(%d/%d)"%(i+yy+1,total)
    print "=========================="
    print tmp[0]
    decision = 0
    while True:
        var = raw_input("enter(y/n): ")
        if var == "y" or var == "Y":
            decision = 2
            break
        elif var == "n" or var == "N":
            decision = 1
            break
        elif var == "exit":
            pass

    if decision == 2:
        tmp[1] = 'Q'
    elif decision == 1:
        tmp[1] = 'NQ'
    item = tmp[0]+"<#>"+tmp[1]+"\n"
    out = open("annotated.txt",'a')
    out.write(item)
    out.close()




