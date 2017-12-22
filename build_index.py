import csv
import numpy as np
import pandas as pd
from BTrees.OOBTree import OOBTree
import pickle
import io
import sys


sys.setrecursionlimit(1000000)


def build_index(file_path, filename, idx_path, attr_name, idx_type, multiway):
    """
    build index
    :param file_path: e.g. 'C:/2017_Fall/CS 411/csv_data/'
    :param filename: e.g. 'review.csv'
    :param idx_path: e.g. file_path + 'index/'
    :param attr_name: e.g. 'stars'
    :param idx_type: e.g. 'Hash', 'BTree', 'Location', 'Tag'
    :param multiway: True or False, True for join attribute, e.g. 'business_id'
    :return:
    """
    if idx_type == 'Hash':
        idx_name = filename.replace('.csv', attr_name + '.npy')
        id_name = filename.replace('.csv', attr_name+'idx.npy')
        idx_dict = {}
        id_dict = {}
        with open(file_path + filename, 'r', encoding='utf8') as myfile:
            reader = csv.reader(myfile)
            attributes = next(reader)
            attr_idx = attributes.index(attr_name)
            count = 0
            for row in reader:
                cur = row[attr_idx]
                if cur not in idx_dict:
                    idx_dict[cur] = list()
                idx_dict[cur].append(count)
                id_dict[count] = cur
                count += 1
        myfile.close()
        if multiway:
            np.save(idx_path + id_name, id_dict)
        np.save(idx_path + idx_name, idx_dict)
    elif idx_type == 'BTree':
        idx_dict = {}
        idx_name = filename.replace('.csv', attr_name + '.pkl')
        for chunck_df in pd.read_csv(file_path + filename, chunksize=10000, encoding="utf8"):
            dic = chunck_df.to_dict()
            idx_dict = dict(list(idx_dict.items()) + list(dic[attr_name].items()))
        idx_list = {}
        for k, v in idx_dict.items():
            if v not in idx_list:
                idx_list[v] = [k]
            else:
                idx_list[v].append(k)
        BT = OOBTree()
        BT.update(idx_list)
        with open(idx_path + idx_name, 'wb') as f:
            pickle.dump(BT, f, pickle.HIGHEST_PROTOCOL)
    elif idx_type == 'Location':
        if filename == 'review.csv' or filename == 'photos.csv':
            new_od = getloc_r_p(file_path + filename)
        elif filename == 'business.csv' or filename == 'checkin.csv':
            new_od = getloc_b_c(file_path + filename)
        else:
            new_od = getloc_r_p(file_path + filename)
        idx_name = filename.replace('.csv', 'loc.npy')
        np.save(idx_path + idx_name, new_od)
    elif idx_type == 'Tag':
        myfile = open(file_path + filename, 'r', encoding='utf8')
        reader = csv.reader(myfile)
        tag = next(reader)
        myfile.close()
        idx_name = filename.replace('.csv', 'tag.npy')
        np.save(idx_path + idx_name, tag)

def getloc_b_c(fname):
    f = open(fname, "r", encoding='utf8')
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    newod = od[0:len(od) - 1]
    return newod


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

