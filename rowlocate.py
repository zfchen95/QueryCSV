import csv
import sys
import io
import time


def getloc_b_c(fname):
    #fname is a string. ex:"review-5k.csv"
    f = open(fname, "r")
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    newod = od[0:len(od)-1]
    #print("len(newod)",len(newod))
    return(newod)
    
def getrow(fname, loclist, num):
    #fname is a string. loclist is the list from getloc, num is the row number to locate
    f = open(fname, "r")
    f.seek(loclist[num])
    reader = csv.reader(f)
    res = next(reader)
    f.close()
    return(res)

def getloc_r_p(fname):
    #fname is a string. ex:"review-5k.csv"
    f = io.open(fname, encoding = "utf8", newline="\r\n")
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    f.close()
    newod = od[0:len(od)-1]
    
    flag = [0] * len(newod)
    
    f = open(fname, "r")
    reader = csv.reader(f)
    row = next(reader)
    for i in range(len(newod)):
        fcopy = open(fname, "r")
        fcopy.seek(newod[i])
        xreader = csv.reader(fcopy)
        tmp = next(xreader)
        fcopy.close()
        if row!=tmp:
            flag[i] = 1
            continue
        elif i!=len(newod)-1:
            row = next(reader)
            
    f.close()
        
    finalod = []
    for i in range(len(newod)):
        if flag[i]==0:
            finalod.append(newod[i])
    
    #print("len(finalod)", len(finalod))
    return(finalod)

fname = "business.csv"
f = open(fname, "r")
reader = csv.reader(f)
bcount = 0
for row in reader:
    bcount = bcount+1
    
print("bcount", bcount)
f.close()

#flist = getloc_r_p(fname)
flist = getloc_b_c(fname)

start = time.time()
ans = getrow(fname,flist,5002)
print(ans)
print(time.time()-start)


