import sqlparse
import copy
import re
import time

logical_opt = ['AND', 'OR', '(', ')']
compare_opt = ['>=', '<=', '<>', '>', '<', '=', 'LIKE']


def get_condition(where):
    loglst = [l for l in where.split(' ') if l in logical_opt]
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
                where = where.replace(log, newlst[0])
        return loglst, [i.strip() for i in where.split(newlst[0])]


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


# Help function to order the parenthese function
def sort_order(lst, leftside, inside, rightside, num):
    order = []
    if not leftside:
        for n in range(len(lst)):
            index = lst.index(lst[n])
            order.append(index)
    else:
        for i in leftside:
            order.append(i + num)
        for j in range(len(inside)):
            order.append(j)
        for k in rightside:
            order.append(k)
    newlist = []
    for m in range(len(order)):
        index = order.index(m)
        newlist.append(lst[index])
    return newlist


def parentheses(keyword, conds):
    left = keyword.index('(')
    right = keyword.index(')')
    keyword.remove('(')
    keyword.remove(')')
    num_inside = right - left - 1
    inside = []
    leftside = []
    rightside = []
    for i in range(0, left):
        leftside.append(i)
    for j in range(left, right - 1):
        inside.append(j)
    for z in range(right - 1, len(keyword)):
        rightside.append(z)

    newkey = sort_order(keyword, leftside, inside, rightside, num_inside)

    inside2 = [i for i in inside] + [i + 1 for i in inside]
    leftside2 = leftside
    rightside2 = [j + 1 for j in rightside]
    newcond = sort_order(conds, leftside2, inside2, rightside2, num_inside + 1)

    return newkey, newcond


def sql_preprocess(query):
    if 'DISTINCT' in query:
        dist = True
        sql = query.replace('DISTINCT', '')
    else:
        dist = False
        sql = query

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
    if '(' in keyword and ')' in keyword:
        keyword, conds = parentheses(keyword, conds)
    return attribute, files, conds, keyword, dist
