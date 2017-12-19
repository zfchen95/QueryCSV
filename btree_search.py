# coding: utf-8

# In[120]:


import copy
import pickle


# In[122]:


def is_number(s):
    try:
        float(s)  # for int, long and float
    except ValueError:
        try:
            complex(s)  # for complex
        except ValueError:
            return False
    return True



def row_operation(tree, num, op):
    if op == '>':
        row = list(tree.values(min=num, excludemin=True))
    elif op == '>=':
        row = list(tree.values(min=num, excludemax=False))
    elif op == '<':
        row = list(tree.values(max=num, excludemax=True))
    elif op == '<=':
        row = list(tree.values(max=num, excludemax=False))
    elif op == '=':
        row = list(tree[num])
    elif op == '<>':
        row = list(tree.values(max=num, excludemax=True)) + list(tree.values(min=num, excludemax=True))
    output = [j for i in row for j in i]
    return output


# In[126]:


def get_rows(filename, compare_value, op):
    if is_number(compare_value):
        compare_value = float(compare_value)
    with open(filename, 'rb') as f:
        Btree = pickle.load(f)
    return row_operation(Btree, compare_value, op)

