import csv
import sys
import sqlparse as sp
import numpy as np


def query():
    return


def project(filename, attr):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    attrs = next(reader)
    idx = []
    for str in attr:
        idx.append(attrs.index(str))
    for row in reader:
        for i in idx:
            print(row[i])
    myFile.close()
    return


def select(filename, str):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    for row in reader:
        if str in row:
            print(row)
    myFile.close()
    return


def rename():
    return


def match():
    return


def intersection():
    return


def loader(filename):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    count = 0
    for row in reader:
        print(row)
        count += 1
    myFile.close()
    return count


def average(filename, attr):
    tmp = sum(filename, attr)
    return tmp/COUNT


def sum(filename, attr):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    attrs = next(reader)
    idx = []
    for str in attr:
        idx.append(attrs.index(str))
    res = np.zeros(len(attr))
    for row in reader:
        for i in range(len(attr)):
            res += float(row[idx[i]])
    myFile.close()
    return res


def minimum(filename, attr):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    attrs = next(reader)
    idx = []
    for str in attr:
        idx.append(attrs.index(str))
    res = np.empty(len(attr))
    res.fill(float('inf'))
    for row in reader:
        for i in range(len(attr)):
            tmp = float(row[idx[i]])
            if tmp < res[i]:
                res[i] = tmp
    myFile.close()
    return res


def maximum(filename, attr):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    attrs = next(reader)
    idx = []
    for str in attr:
        idx.append(attrs.index(str))
    res = np.zeros(len(attr))
    for row in reader:
        for i in range(len(attr)):
            tmp = float(row[idx[i]])
            if tmp > res[i]:
                res[i] = tmp
    myFile.close()
    return res


def count():
    return COUNT


def find(filename, attr, cond):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    attrs = next(reader)
    res = []
    idx = attrs.index(attr)
    for row in reader:
        if float(row[idx]) > cond:
            res.append(row)
    myFile.close()
    return res


filename = 'players_stats_2014_2015.csv'
COUNT = loader(filename)
# print(COUNT)
# project(filename, ['Name', 'Games Played'])
# select(filename, 'James Harden')
sql = 'select * from players_stats_2014_2015.csv where id in (select id from bar)'
print(sp.format(sql, reindent=True, keyword_case='upper'))

print(sum(filename, ['3PM']))
print(maximum(filename, ['FGM', '3PM', 'FTM']))
print(find(filename, '3PA', 600))
print(minimum(filename, ['FG%', '3P%', 'FT%']))
print(average(filename, ['Games Played']))
