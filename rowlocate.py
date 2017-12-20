import csv
import sys
import io
import time

def getloc(fname):
    #fname is a string. ex:"review-5k.csv"
    f = io.open(fname, encoding = "utf8", newline="\r\n")
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    newod = od[0:len(od)-1]

    f.seek(0)
    reader = csv.reader(f)
    attr = next(reader)
    f.close()
    finalod = []
    for i in range(len(newod)):
        x = newod[i]
        f = io.open(fname, encoding = "utf8", newline="\r\n")
        f.seek(x)
        reader = csv.reader(f)
        tmp = next(reader)
        if len(tmp)==len(attr):
            finalod.append(x)
            f.close()
    return(finalod)
    
def getrow(fname, loclist, num):
    #fname is a string. loclist is the list from getloc, num is the row number to locate
    f = io.open(fname, encoding = "utf8", newline="\r\n")
    f.seek(loclist[num])
    reader = csv.reader(f)
    res = next(reader)
    f.close()
    return(res)

ff = "review-5k.csv"
flist = getloc(ff)
ans = getrow(ff,flist,5002)
print(ans)