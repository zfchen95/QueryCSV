import csv
import sys
import io
import time
import numpy as np

def getloc_b_c(fname):
    # fname is a string. ex:"review-5k.csv"
    f = open(fname, "r", encoding='utf8')
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    newod = od[0:len(od) - 1]
    # print("len(newod)",len(newod))
    return (newod)


def getrow(fname, num):
    # fname is a string. loclist is the list from getloc, num is the row number to locate
    f = open(fname, "r", encoding='utf8')
    f.seek(num)
    reader = csv.reader(f)
    res = next(reader)
    f.close()
    return res


def getloc_r_p(fname):
    # fname is a string. ex:"review-5k.csv"
    f = io.open(fname, encoding="utf8", newline="\r\n")
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    f.close()
    newod = od[0:len(od) - 1]

    flag = [0] * len(newod)

    f = open(fname, "r", encoding='utf8')
    reader = csv.reader(f)
    row = next(reader)
    for i in range(len(newod)):
        fcopy = open(fname, "r", encoding='utf8')
        fcopy.seek(newod[i])
        xreader = csv.reader(fcopy)
        tmp = next(xreader)
        fcopy.close()
        if row != tmp:
            flag[i] = 1
            continue
        elif i != len(newod) - 1:
            row = next(reader)
    f.close()
    finalod = []
    for i in range(len(newod)):
        if flag[i] == 0:
            finalod.append(newod[i])
    return finalod


list = getloc_r_p('C:/2017_Fall/CS 411/csv_data/review.csv')
np.save('C:/2017_Fall/CS 411/csv_data/index/reviewloc.npy', list)