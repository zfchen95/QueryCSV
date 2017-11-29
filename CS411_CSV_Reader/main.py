import csv
import sys
import sqlparse
import numpy as np
import time
import operator
from sqlparse.sql import Identifier, IdentifierList, Parenthesis, Token, TokenList, Where, Comparison
from sqlparse.tokens import Keyword, DML
import re
import copy

logical_opt = ['AND', 'OR', '(', ')']
compare_opt = ['>=', '<=', '<>', '>', '<', '=', 'LIKE']


def get_condition(where):
    loglst = [l for l in where.split() if l in logical_opt]
    newlst = copy.deepcopy(loglst)
    if '(' in newlst and ')' in newlst:
        newlst.remove('(')
        newlst.remove(')')
        where = where.replace("(", "")
        where = where.replace(")", "")
    if not newlst:
        return loglst, [where]
    else:
        if len(newlst) > 1:
            for log in newlst[1:]:
                con = where.replace(log, newlst[0])
        else:
            con = where
        return loglst, [i.strip() for i in con.split(newlst[0])]


def split_condition(s):
    for sep in compare_opt:
        if sep in s:
            lst = []
            for i in s.split(sep):
                # start from NOT
                if i.startswith("NOT"):
                    lst.append('NOT')
                    i = i[4:]
                i = i.strip()
                # string or character
                if i.startswith("'") and i.endswith("'"):
                    lst.append([i[1:-1]])
                # attribute without rename or integers
                elif not '.' in i:
                    lst.append([i])
                else:
                    # float number
                    test = i.replace(".", "")
                    if test.isnumeric():
                        lst.append([i])
                    # attribute with rename
                    else:
                        new_attr = i.split('.')
                        lstitem = []
                        lstitem.append(new_attr[0].strip())
                        lstitem.append(new_attr[1].strip())
                        lst.append(lstitem)
            return lst, sep
            break
    return [], ''


def reverse_not(opt):
    if opt == '<':
        newopt = '>='
    elif opt == '>':
        newopt = '<='
    elif opt == '<=':
        newopt = '>'
    elif opt == '>=':
        newopt = '<'
    elif opt == '=':
        newopt = '<>'
    elif opt == '<>':
        newopt = '='
    else:
        newopt = 'NOT LIKE'
    return newopt


def sql_preprocess(sql):
    sql = sqlparse.format(sql)
    stmt = sqlparse.parse(sql)[0]

    # Select clauses
    attrs = str(stmt.tokens[2])
    attrs = attrs.split(',')
    attribute = []
    for i in range(len(attrs)):
        if not '.' in attrs[i]:
            attribute.append([attrs[i].strip()])
        else:
            array = []
            new_file = attrs[i].split('.')
            array.append(new_file[0].strip())
            array.append(new_file[1].strip())
            attribute.append(array)

    # From clauses
    file = str(stmt.tokens[6])
    file = file.split(',')
    files = []
    for j in range(len(file)):
        file[j] = file[j].strip()
        if not ' ' in file[j]:
            files.append([file[j]])
        else:
            array2 = []
            new_file = file[j].split(' ')
            array2.append(new_file[0].strip())
            array2.append(new_file[1].strip())
            files.append(array2)

    # Where clause conditions, e.q. 'ID = 3'
    if 'WHERE' not in sql:
        conds = []
        keyword = []
    else:
        wherestr = str(stmt.tokens[-1])
        where = str(re.findall('WHERE (.*);', wherestr))[2:-2]
        keyword, condition = get_condition(where)
        n = len(files)
        if n == 1:
            conds = []
            for c in condition:
                value, opt = split_condition(str(c))
                conds.append(value + [opt])
        else:
            conds = []
            for c in condition:
                value, opt = split_condition(str(c))
                if value[0] == 'NOT':
                    value.remove('NOT')
                    opt = reverse_not(opt)
                conds.append(value + [opt])
    return attribute, files, conds, keyword


def is_number(s):
    try:
        float(s)  # for int, long and float
    except ValueError:
        try:
            complex(s)  # for complex
        except ValueError:
            return False

    return True


def get_attr_index(filename, attrs):
    """
    Get column index of attributes in select clause;
    :param filename: string
    :param attrs: list of string, attributes we selected
    :return: list of integer, indices of selected attributes
    """
    idx = []
    try:
        myFile = open(filename, 'r')
        reader = csv.reader(myFile)
        attrs_set = next(reader)
        for attr in attrs:
            try:
                idx.append(attrs_set.index(attr))
            except ValueError:
                print('No such attribute:', attr)
        myFile.close()
    except Exception:
        print('No such file:', filename)
    return idx


def get_index(filename, attr):
    """
    find the index of an attribute
    :param filename:
    :param attr:
    :return: integer
    """
    try:
        myFile = open(filename, 'r')
        reader = csv.reader(myFile)
        attrs_set = [attr.lower() for attr in next(reader)]
        myFile.close()
        try:
            return attrs_set.index(attr)
        except ValueError:
            print('No such attribute:', attr)
    except Exception:
        print('No such file:', filename)
    return -1


def get_attribute_name(filename):
    """
    get a list of attribute name
    :param filename:
    :return: list
    """
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    attribute_name = [attr.lower() for attr in next(reader)]
    myFile.close()
    return attribute_name


def get_file_name(fileMap, cond):
    """
    search the fileMap and find the corresponding filename
    :param fileMap: dictionary of filename
    :param cond: condition
    :return: 1D array [filename1, filename2]
    """
    left = cond[0]
    right = cond[1]
    filenames = ['', '']
    if len(left) == 2:
        filenames[0] = fileMap[left[0]]
    else:
        for filename in fileMap.values():
            if left[0] in get_attribute_name(filename):
                filenames[0] = filename
                break
    if len(right) == 2:
        filenames[1] = fileMap[right[0]]
    else:
        for filename in fileMap.values():
            if right[0] in get_attribute_name(filename):
                filenames[1] = filename
                break
    return filenames


def get_file_number(fileMap, cond):
    """
    search the fileMap and get the number of csv in condition
    :param fileMap: dictionary of filename
    :param cond: condition
    :return: int{0, 1, 2}
    """
    left = cond[0]
    right = cond[1]
    res = 0
    if len(left) == 2:
        res += 1
    else:
        for filename in fileMap.values():
            if left[0] in get_attribute_name(filename):
                res += 1
                break
    if len(right) == 2:
        res += 1
    else:
        for filename in fileMap.values():
            if right[0] in get_attribute_name(filename):
                res += 1
                break
    return res


def print_attribute_name(filename):
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    print(next(reader))
    myFile.close()
    return


def get_truth(attr, value, op):
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq,
           '<>': operator.ne,
           'LIKE': like_op,
           'NOT LIKE': not_like_op
           }
    if is_number(attr) and is_number(value):
        return ops[op](float(attr), float(value))
    return ops[op](attr, value)


def decompose_condition(cond):
    """
    return decomposition of single condition
    :param cond:
    :return: target, value, op
    """
    if len(cond[0]) == 1:
        target = cond[0][0]
    else:
        target = cond[0][1].lower()
    if len(cond[1]) == 1:
        value = cond[1][0]
    else:
        value = cond[1][1].lower()
    op = cond[2]
    return target, value, op


def project(attributes, fileMap, file_set, tuples):
    if attributes[0][0] == '*':
        res = []
        for i in range(len(tuples[0])):
            tmp = list()
            tmp.append(tuples[0][i])
            tmp.append(tuples[1][i])
            res.append(tmp)
        return res
    else:
        res = []
        file_idx = [file_set.index(fileMap[attribute[0]]) for attribute in attributes]
        attr_idx = [get_index(fileMap[attribute[0]], attribute[1].lower()) for attribute in attributes]
        for i in range(len(tuples[0])):
            tmp = list()
            for j in range(len(attr_idx)):
                tmp.append(tuples[file_idx[j]][i][attr_idx[j]])
            res.append(tmp)
        return res


def select(filename, cond):
    """
    select tuples from single csv file
    :param filename: string
    :param cond: 1D array, [left, right, op]
    :return: 2D array
    """
    myFile = open(filename, 'r', encoding='utf8')
    reader = csv.reader(myFile)
    attrs_set = [attr.lower() for attr in next(reader)]
    target, value, op = decompose_condition(cond)
    try:
        idx = attrs_set.index(target)
    except ValueError:
        print('Cannot find', target, 'in', filename)
    res = []
    if value in attrs_set:
        idx2 = attrs_set.index(value)
        for row in reader:
            if get_truth(row[idx], row[idx2], op):
                res.append(row)
    else:
        for row in reader:
            if get_truth(row[idx], value, op):
                res.append(row)
    myFile.close()
    return res


def or_select(tuples, filename, cond):
    target, value, op = decompose_condition(cond)
    myFile = open(filename, 'r')
    reader = csv.reader(myFile)
    idx = get_index(filename, target)
    for row in reader:
        if get_truth(row[idx], value, op) and row not in tuples:
            tuples.append(row)
    return tuples


def project_after_select(tuples, indices):
    return [[tuples[i][index] for index in indices] for i in range(len(tuples))]


def select_after_select(tuples, filename, cond):
    target, value, op = decompose_condition(cond)
    idx = get_index(filename, target)
    res = []
    for row in tuples:
        if get_truth(row[idx], value, op):
            res.append(row)
    return res


def self_join_selection(filename, cond):
    myFile1 = open(filename, 'r')
    myFile2 = open(filename, 'r')
    reader1 = csv.reader(myFile1)
    reader2 = csv.reader(myFile2)
    attrs_set1 = next(reader1)
    attrs_set2 = next(reader2)
    if len(cond[0]) == 1:
        target = cond[0][0]
    else:
        target = cond[0][1]
    if len(cond[1]) == 1:
        value = cond[1][0]
    else:
        value = cond[1][1]
    op = cond[2]
    idx1 = attrs_set1.index(target)
    idx2 = attrs_set2.index(value)
    res = []
    for row1 in reader1:
        for row2 in reader2:
            if row1[idx1].isnumeric():
                if get_truth(float(row1[idx1]), float(row2[idx2]), op):
                    res.append([row1, row2])
            else:
                if get_truth(row1[idx1], row2[idx2], op):
                    res.append([row1, row2])
    myFile1.close()
    myFile2.close()
    return res


def select_after_self_join(tuples, attributes_name, cond):
    res = []
    target = cond[0][1]
    value = cond[1][1]
    op = cond[2]
    idx1 = attributes_name.index(target)
    idx2 = attributes_name.index(value)
    for tuple in tuples:
        if tuple[0][idx1].isnumeric():
            if get_truth(float(tuple[0][idx1]), float(tuple[1][idx2]), op):
                res.append(tuple)
        else:
            if get_truth(tuple[0][idx1], tuple[1][idx2], op):
                res.append(tuple)
    return res


def select_after_join(tuples, fileMap, file_set, cond):
    target, value, op = decompose_condition(cond)
    if len(cond[0]) == 2 and len(cond[1]) == 2:
        res = []
        filename1 = fileMap[cond[0][0]]
        filename2 = fileMap[cond[1][0]]
        file_idx1 = file_set.index(filename1)
        file_idx2 = file_set.index(filename2)
        attr_idx1 = get_index(filename1, target)
        attr_idx2 = get_index(filename2, value)
        for i in range(len(tuples[0])):
            if get_truth(tuples[file_idx1][i][attr_idx1], tuples[file_idx2][i][attr_idx2], op):
                res.append([tuples[0][i], tuples[1][i]])
        table1 = []
        table2 = []
        for tuple in res:
            table1.append(tuple[0])
            table2.append(tuple[1])
        return table1, table2
    return tuples[0], tuples[1]


def select_another_table(tuples, file_set, filename, cond):
    file_idx = file_set.index(filename)
    if len(tuples[file_idx]) == 0:
        pass
    else:
        target, value, op = decompose_condition(cond)
        myFile = open(filename, 'r')
        reader = csv.reader(myFile)
        attrs_set = [attr.lower() for attr in next(reader)]
        try:
            idx = attrs_set.index(target)
        except ValueError:
            print('Cannot find', target, 'in', filename)

    return tuples


def select_join(filenames, cond):
    myFile1 = open(filenames[0], 'r', encoding="utf8")
    myFile2 = open(filenames[1], 'r', encoding="utf8")
    reader1 = csv.reader(myFile1)
    reader2 = csv.reader(myFile2)
    attrs_set1 = [attr.lower() for attr in next(reader1)]
    attrs_set2 = [attr.lower() for attr in next(reader2)]
    target, value, op = decompose_condition(cond)
    idx1 = attrs_set1.index(target)
    idx2 = attrs_set2.index(value)
    res = []
    dict = {}
    count = 0;
    if op == '=':
        for row1 in reader1:
            if row1[idx1] != '':
                dict[row1[idx1]] = row1
        myFile1.close()
        for row2 in reader2:
            if row2[idx2] in dict:
                res.append([dict[row2[idx2]], row2])
        myFile2.close()
    else:
        for row1 in reader1:
            try:
                for row2 in reader2:
                    count += 1
                    try:
                        if row1[idx1].isnumeric() and row2[idx2].isnumeric():
                            if get_truth(float(row1[idx1]), float(row2[idx2]), op):
                                res.append([row1, row2])
                        else:
                            if get_truth(row1[idx1], row2[idx2], op):
                                res.append([row1, row2])
                    except Exception:
                        print('Unknown error in comparing two values in select join')
            except Exception:
                print('Unknown error in reading', filenames[1], ' in select join')
            myFile2.close()
            myFile2 = open(filenames[1], 'r', encoding="utf8")
            reader2 = csv.reader(myFile2)
        myFile1.close()
        myFile2.close()
    table1 = []
    table2 = []
    for tuple in res:
        table1.append(tuple[0])
        table2.append(tuple[1])
    return table1, table2


def join_after_join(tuples, fileMap, file_set, cond):
    # target query 'SELECT * FROM movies.csv M, oscars.csv A WHERE imdb_score < 7 AND M.movie_title = A.film;'
    target, value, op = decompose_condition(cond)
    filenames = get_file_name(fileMap, cond)
    idx1 = get_attribute_name(filenames[0]).index(target)
    idx2 = get_attribute_name(filenames[1]).index(value)
    file_idx1 = file_set.index(filenames[0])
    file_idx2 = file_set.index(filenames[1])
    res =[]
    if len(tuples[file_idx1]) == 0 and len(tuples[file_idx2]) == 0:
        pass
    elif len(tuples[file_idx2]) != len(tuples[file_idx1]):
        my_file = open(filenames[1], 'r', encoding="utf8")
        reader = csv.reader(my_file)
        if op == '=':
            dict = {}
            for tuple1 in tuples[file_idx1]:
                if tuple1[idx1] != '':
                    dict[tuple1[idx1]] = tuple1
            # for row in reader:
            #     if row[idx2] in dict:
            #         res.append([dict[row[idx2]], row])
            for tuple2 in tuples[file_idx2]:
                if tuple2[idx2] in dict:
                    res.append([dict[tuple2[idx2]], tuple2])
        else:
            for row in reader:
                if row[idx2] == '':
                    pass
                else:
                    for tuple1 in tuples[file_idx1]:
                        if get_truth(tuple1[idx1], row[idx2], op):
                            res.append([tuple1, row])
        my_file.close()
    else:
        tuple1 = tuples[file_idx1]
        tuple2 = tuples[file_idx2]
        for i in range(len(tuples[file_idx1])):
            if get_truth(tuple1[i][idx1], tuple2[i][idx2], op):
                res.append([tuple1[i], tuple2[i]])
    table1 = []
    table2 = []
    for tuple in res:
        table1.append(tuple[0])
        table2.append(tuple[1])
    return table1, table2


def like_op(before_se, query):
    #before_se is a list of list from previous stage, query is LIKE clause which is a pattern, string after LIKE
    keyword = re.compile(r'[a-z A-Z 0-9]+')
    keyword = keyword.findall(query)
    keyword = keyword[0] #now we have the STRING we are going to match

    pattern1 = re.compile(r'^%{}%$'.format(keyword))	#1 %str%
    pattern2 = re.compile(r'^%{}$'.format(keyword))   #2 %str
    pattern3 = re.compile(r'^{}%$'.format(keyword))   #3 str%
    pattern4 = re.compile(r'^{}$'.format(keyword))    #4 str
    pattern5 = re.compile(r'^_{}_$'.format(keyword))  #5 _str_
    pattern6 = re.compile(r'^_{}$'.format(keyword))   #6 _str
    pattern7 = re.compile(r'^{}_$'.format(keyword))   #7 str_
    pattern8 = re.compile(r'^%{}_$'.format(keyword))  #8 %str_
    pattern9 = re.compile(r'^_{}%$'.format(keyword))  #9 _str%

    q_pattern = None

    if(re.match(pattern1, query) != None):
        q_pattern = re.compile(r'^.*{}.*$'.format(keyword))
        #print(1)
    elif(re.match(pattern2, query) != None):
        q_pattern = re.compile(r'^.*{}$'.format(keyword))
        #print(2)
    elif(re.match(pattern3, query) != None):
        q_pattern = re.compile(r'^{}.*$'.format(keyword))
        #print(3)
    elif(re.match(pattern4, query) != None):
        q_pattern = re.compile(r'^{}$'.format(keyword))
        #print(4)
    elif(re.match(pattern5, query) != None):
        q_pattern = re.compile(r'^.{}.$'.format(keyword))
        #print(5)
    elif(re.match(pattern6, query) != None):
        q_pattern = re.compile(r'^.{}$'.format(keyword))
        #print(6)
    elif(re.match(pattern7, query) != None):
        q_pattern = re.compile(r'^{}.$'.format(keyword))
        #print(7)
    elif(re.match(pattern8, query) != None):
        q_pattern = re.compile(r'^.*{}.$'.format(keyword))
        #print('8')
    elif(re.match(pattern9, query) != None):
        q_pattern = re.compile(r'^.{}.*$'.format(keyword))
        #print('9')
    #print(q_pattern)
    if(re.match(q_pattern, before_se) != None):
        return 1
    return 0


def not_like_op(before_se, query):
    return not like_op(before_se, query)


def reorder_condition(fileMap, conds, keyword):
    if ('AND' in keyword and 'OR' not in keyword) or ('OR' in keyword and 'AND' not in keyword):
        table_need = [get_file_number(fileMap, cond) for cond in conds]
        for i in range(len(conds)):
            if table_need[i] == 2 and conds[i][2] != '=':
                table_need[i] += 1
        new_conds =[]
        for i in range(len(table_need)):
            if table_need[i] == 1:
                new_conds.append(conds[i])
                table_need[i] = -1
        for i in range(len(table_need)):
            if table_need[i] == 2:
                new_conds.append(conds[i])
                table_need[i] = -1
        for i in range(len(table_need)):
            if table_need[i] == 3:
                new_conds.append(conds[i])
                table_need[i] = -1
        return new_conds
    else:
        return conds


def reorder_condition_by_key(conds, keyword):
    if '(' in keyword:
        new_condition = conds
        new_keyword = keyword
        if keyword[0] == '(':
            new_keyword.remove('(')
            new_keyword.remove(')')
        start = new_keyword.index('(')
        end = new_keyword.index(')')
        for i in range(0, start):
            tmp = conds[i]
            new_condition.remove(conds[i])
            new_condition.append(tmp)
        for i in range(0, start):
            tmp = keyword[i]
            conds.remove(keyword[i])
        return new_condition, new_keyword
    else:
        return conds, keyword


def checkrow(tf, op):
    if len(tf)==1:
        return(eval(tf[0]))
    n = 0
    ss = ''
    for st in range(len(tf)):
        while (n<len(op)):
            if op[n] in ['(', 'NOT']:
                ss = ss+op[n]+' '
                n += 1
            else:
                break
        ss = ss+tf[st]+' '
        if n<len(op):
            if op[n] in [')']:
                ss = ss+op[n]+' '
                n += 1
        if st<(len(tf)-1):
            ss = ss+op[n]+' '
            n+=1
    return(eval(ss.lower()))


def query_one_table(attribute, file, conds, keyword):
    myFile = open(file[0][0], 'r', encoding = "utf8")
    reader = csv.reader(myFile)
    attrs_set = next(reader)
    tmp = []
    for row in reader:
        checkcon = [False]*len(conds)
        for j in range(len(conds)):
            cond = conds[j]
            if len(cond)==3:
                if cond[0][0] in attrs_set:
                    valuel = row[attrs_set.index(cond[0][0])]
                else:
                    valuel = cond[0][0]
                #get value for right
                if cond[1][0] in attrs_set:
                    valuer = row[attrs_set.index(cond[1][0])]
                else:
                    valuer = cond[1][0]
                if cond[2]=='LIKE':
                    checkcon[j] = str(like_op(valuel, valuer))
                else:
                    checkcon[j] = str(int(get_truth(valuel, valuer, cond[2])))
            else:
                if cond[1][0] in attrs_set:
                    valuel = row[attrs_set.index(cond[1][0])]
                else:
                    valuel = cond[1][0]
                #get value for right
                if cond[2][0] in attrs_set:
                    valuer = row[attrs_set.index(cond[2][0])]
                else:
                    valuer = cond[2][0]
                #print(valuel, valuer)
                if cond[3]=='LIKE':
                    checkcon[j] = str(int(not like_op(valuel, valuer)))
                else:
                    checkcon[j] = str(int(not get_truth(valuel, valuer, cond[3])))
        thisrow = checkrow(checkcon, keyword)
        #print(checkcon)
        #print(keyword)
        if thisrow:
            tmp.append(row)
            #i += 1
            #if i==10:
            #    break

    if attribute[0][0]=='*':
        print(attrs_set)
    else:
        # print(attribute)
        ntmp = []
        for row in tmp:
            rowtmp = []
            for att in attribute:
                rowtmp.append(row[attrs_set.index(att[0])])
            ntmp.append(rowtmp)
        tmp = ntmp
    #for row in tmp:
    #    print(row)
    #print(len(tmp))
    return tmp


def query_two_table(attribute, file, conds, keyword):
    fileMap = {}
    for filename in file:
        if len(filename) == 2:
            fileMap[filename[1]] = filename[0]
        else:
            fileMap[filename[0]] = filename[0]
    file_set = []
    for filename in fileMap.values():
        if filename not in file_set:
            file_set.append(filename)
    counter = 0
    tmp = []
    for i in file_set:
        tmp.append([])
    conds = reorder_condition(fileMap, conds, keyword)
    for cond in conds:

        if len(cond[0]) == 2 and len(cond[1]) == 2 and cond[0][0] != cond[1][0]:
            # self join or inner join
            filename1 = fileMap[cond[0][0]]
            filename2 = fileMap[cond[1][0]]
            file_idx1 = file_set.index(filename1)
            file_idx2 = file_set.index(filename2)
            if counter > 0:
                if keyword[counter - 1] == 'AND':
                    if fileMap[cond[0][0]] == fileMap[cond[1][0]]:
                        attribute_name = get_attribute_name(filename1)
                        tmp = select_after_self_join(tmp, attribute_name, cond)
                    else:
                        #  join after selection
                        table1, table2 = join_after_join(tmp, fileMap, file_set, cond)
                        tmp[file_idx1] = table1
                        tmp[file_idx2] = table2
                elif keyword[counter - 1] == 'OR':
                    table1, table2 = select_join([fileMap[cond[0][0]], fileMap[cond[1][0]]], cond)
                    tmp[file_idx1] += table1
                    tmp[file_idx2] += table2
            else:
                if fileMap[cond[0][0]] == fileMap[cond[1][0]]:
                    tmp = self_join_selection(fileMap[cond[0][0]], cond)
                else:
                    tmp[file_idx1], tmp[file_idx2] = select_join([fileMap[cond[0][0]], fileMap[cond[1][0]]], cond)
        elif len(cond[0]) == 2:
            # the first item is from a renamed table
            filename = fileMap[cond[0][0]]
            file_idx = file_set.index(filename)
            if counter > 0:
                if keyword[counter - 1] == 'AND':
                    if len(tmp[file_idx]) == 0:
                        tmp[file_idx] = select(filename, cond)
                    elif len(tmp[0]) == len(tmp[1]) and len(cond[1]) == 2:
                        #  join after selection
                        table1, table2 = select_after_join(tmp, fileMap, file_set, cond)
                        tmp[file_idx1] = table1
                        tmp[file_idx2] = table2
                    else:
                        tmp[file_idx] = select_after_select(tmp[file_idx], filename, cond)
                elif keyword[counter - 1] == 'OR':
                    tmp[file_idx] = or_select(tmp[file_idx], filename, cond)
            else:
                tmp[file_idx] = select(filename, cond)
        elif len(cond[1]) == 2:
            # the second item is from a renamed table
            pass
            # implement it
        else:
            pass
        counter += 1
    res = project(attribute, fileMap, file_set, tmp)
    return res


def query_three_table(attribute, file, conds, keyword):
    pass


def query(input):
    query_list = sqlparse.split(input)
    for sql in query_list:
        attribute, file, conds, keyword = sql_preprocess(sql)
        print('SELECT:', attribute)
        print('FROM:', file)
        print('WHERE CONDS:', conds)
        print('WHERE KEY:', keyword)
        start = time.time()
        if len(file) == 1:
            res = query_one_table(attribute, file, conds, keyword)
        elif len(file) == 2:
            res = query_two_table(attribute, file, conds, keyword)
        elif len(file) == 3:
            res = query_two_table(attribute, file, conds, keyword)
        end = time.time()
        for tuple in res:
            print(tuple)
        print("running time", end - start)



# sample query
# one table
sample_query1 = 'SELECT movie_title, title_year FROM movies.csv WHERE title_year=1999 OR title_year = 2009;'
sample_query2 = "SELECT movie_title, imdb_score FROM movies.csv WHERE movie_title LIKE '%Godfather%' OR movie_title LIKE '%Star Wars%';"
sample_query7 = "SELECT movie_title, title_year, imdb_score FROM movies.csv WHERE imdb_score > 8.5 AND movie_title LIKE '%Harry Potter%' AND title_year = 2009;"
sample_query8 = "SELECT * FROM oscars.csv WHERE Ceremony = 80;"
sample_query9 = "SELECT movie_title, country FROM movies.csv WHERE country <> 'English' and country <> '';"
sample_query10 = "SELECT movie_title, imdb_score FROM movies.csv WHERE NOT imdb_score < 9;"
sample_query13 = "SELECT movie_title, duration FROM movies.csv WHERE duration > 150;"
sample_query14 = "SELECT movie_title, budget, gross FROM movies.csv WHERE gross > 448130640;"
sample_query20 = "SELECT Year, Film FROM oscars.csv WHERE Name LIKE '%Star Wars%' or Film LIKE '%Star Wars%';"
sample_query21 = "SELECT Year, Film FROM oscars.csv WHERE Name LIKE '%Godfather%';"
# two table
sample_query3 = 'SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.film AND M.imdb_score < 7;'
sample_query4 = 'SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.imdb_score > 8.5 AND M.movie_title = A.film;'
sample_query6 = "SELECT * FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.Film AND M.movie_title LIKE '%Godfather%';"
sample_query11 = "SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.film AND M.imdb_score > 7 AND A.Award = 'Actor';"
sample_query12 = "SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.film AND M.imdb_score > 8 AND M.title_year > 2000;"
sample_query15 = "SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.film AND M.imdb_score > 8 AND M.title_year > 1970 AND A.Award = 'Actor';"
sample_query16 = 'SELECT M.movie_title, A.Name, M.actor_1_name, M.actor_2_name FROM movies.csv M, oscars.csv A WHERE M.actor_1_name = A.Name OR M.actor_2_name = A.Name;'
sample_query17 = 'SELECT M.movie_title, A.Film, A.Name, M.actor_1_name FROM movies.csv M, oscars.csv A WHERE M.actor_1_name = A.Name AND M.movie_title = A.Film;'
sample_query18 = "SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.film AND ( M.imdb_score > 7 AND M.imdb_score < 8 );"
sample_query19 = "SELECT M.title_year, M.movie_title, A.award, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.movie_title = A.film AND ( M.movie_title LIKE '%Star War%' OR M.movie_title LIKE '%Godfather%' );"
sample_query22 = "SELECT M.title_year, M.movie_title, A.Film, M.imdb_score FROM movies.csv M, oscars.csv A WHERE M.imdb_score > 7 AND M.imdb_score < 8 AND M.movie_title = A.film;"
sample_query23 = "SELECT M.movie_title, A.Film, M.gross, M.budget FROM movies.csv M, oscars.csv A WHERE M.imdb_score > 7 AND M.gross > M.budget AND M.movie_title = A.film;"
sample_query24 = "SELECT M.movie_title, A.award, M.gross, M.budget FROM movies.csv M, oscars.csv A WHERE M.imdb_score > 7 AND M.movie_title = A.film AND M.gross > M.budget;"
sample_query25 = "SELECT M.movie_title, A.Film, M.gross, M.budget FROM movies.csv M, oscars.csv A WHERE M.imdb_score > 7 AND M.movie_title = A.film;"
# three table
sample_query5 = 'SELECT N.movie_title FROM movies.csv M, movies.csv N, oscars.csv A WHERE M.director_name = N.director_name AND M.movie_title > N.movie_title AND M.movie_title = A.film;'

query1 = "SELECT movie_title, title_year, imdb_score FROM movies.csv WHERE movie_title LIKE '%Kevin%' AND imdb_score > 7; "
query3 = "SELECT M.title_year, M.movie_title, A.Award, M.imdb_score, M.movie_facebook_likes FROM movies.csv M oscars.csv A WHERE M.imdb_score < 6 OR M.movie_facebook_likes < 10000 AND A.Winner = 1 AND M.movie_title = A.Film;"
query4 = "SELECT A1.Year, A1.Film, A1.Award, A1.Name, A2.Award, A2.Name FROM oscars.csv A1, oscars2.csv A2 WHERE A1.Film <> '' AND A1.Winner = 1 AND A2.Winner=1 AND A1.Year > 2010 AND A1.Award > A2.Award AND A1.Film = A2.Film;"
query5 = "SELECT M.movie_title, M.title_year, M.imdb_score, A1.Name, A1.Award, A2.Name, A2.Award FROM movies.csv M, oscars.csv A1, oscars.csv A2 ON (M.movie_title = A1.Film AND M.movie_title = A2.Film) WHERE A1.Award = 'Actor' AND A2.Award = 'Actress'"

query(query4)

