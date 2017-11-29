conditions = [[['A', 'Winner'], ['1'], '='], [['A', 'Winner'], [''], '<>'], [['A', 'Winner'], ['1'], '='],
              [['M', 'imdb_score'], ['6'], '<'], [['M', 'movie_title'], ['A', 'Film'], '='], [['M', 'movie_facebook_likes'], ['10000'], '<']]
keyword = ['AND', 'AND', '(', 'OR', 'OR', ')', 'AND']
# keyword = ['(', 'OR', ')', 'AND', 'AND']
print(conditions)
print(keyword)
if '(' in keyword:
    p_start = keyword.index('(')
    p_end = keyword.index(')')
    if p_start == 0:
        keyword.remove(keyword[p_end])
        keyword.remove(keyword[p_start])
    pre_conditions = list()
    pre_keyword = list()
    pre_keyword.append('')
    for i in range(p_start, p_end):
        pre_conditions.append(conditions[i])
        if keyword[i] is '(' or keyword[i] is ')':
            pass
        else:
            pre_keyword.append(keyword[i])
        conditions[i] = ''
        keyword[i] = ''
print(conditions)
print(keyword)
for cond in conditions:
    if cond == '':
        conditions.remove(cond)
for key in keyword:
    if key == '':
        keyword.remove(key)
print(conditions)
print(keyword)
print(pre_conditions)
print(pre_keyword)

res = list()
for i in range(3):
    res.append([])
print(res)

a = [1, 2, 3, 5]
b = [2, 3, 5, 7]
for i, j in zip(a, b):
    print(i, j)
print(a.index(5) == len(a) - 1)
conditions = [[['A', 'Name'], ['%China%'], 'LIKE'], [['A', 'Film'], ['M', 'movie_title'], '='], [['A', 'Film'], ['%China%'], 'LIKE'], [['M', 'imdb_score'], ['7'], '>']]
keyword = ['OR', 'AND', 'AND', 'OR']
for cond in conditions:
    print(cond)
    if len(cond[0]) == 2 and len(cond[1]) == 2:
        if conditions.index(cond) == 0 or conditions.index(cond) == len(conditions) - 1:
            pass
        elif keyword[conditions.index(cond)-1] != 'OR' and keyword[conditions.index(cond)] != 'OR':
            tmp = cond
            conditions.remove(cond)
            conditions.append(tmp)
print(conditions)
print(keyword)

print('OR' not in keyword[1: 3])
