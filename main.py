import csv
import sqlparse


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


filename = 'players_stats_2014_2015.csv'
COUNT = loader(filename)
# print(COUNT)
# project(filename, ['Name', 'Games Played'])
# select(filename, 'James Harden')
sql = 'select * from players_stats_2014_2015.csv where id in (select id from bar)'
print(sqlparse.format(sql, reindent=True, keyword_case='upper'))
res = sqlparse.parse(sql)
for str in res:
    print(str)
