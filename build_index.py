import csv
import numpy as np
import pandas as pd
from BTrees.OOBTree import OOBTree
import pickle
import io
#  Assumption, join on business_id, AND,
#  load data, sort by index
#  time to load file:
#  review500k.csv 7.985
#  business.csv 1.867
#  checkin.csv 1.128
#  photos.csv 0.443
file_path = 'C:/2017_Fall/CS 411/csv_data/'
idx_path = 'C:/2017_Fall/CS 411/csv_data/index/'


def build_index(file_path, filename, idx_path, attr_name, idx_type, multiway):
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
        f = io.open(file_path + filename, encoding="utf8", newline="\r\n")
        od = []
        while 1:
            od.append(f.tell())
            line = f.readline()
            if not line:
                break
        new_od = od[0: -1]
        f.seek(0)
        reader = csv.reader(f)
        attr = next(reader)
        f.close()
        final_od = []
        for i in range(len(new_od)):
            x = new_od[i]
            f = io.open(file_path + filename, encoding="utf8", newline="\r\n")
            f.seek(x)
            reader = csv.reader(f)
            tmp = next(reader)
            if len(tmp) == len(attr):
                final_od.append(x)
                f.close()
        idx_name = filename.replace('.csv', 'loc.npy')
        np.save(idx_path + idx_name, final_od)


build_index(file_path, 'review.csv', idx_path, '', 'Location', False)