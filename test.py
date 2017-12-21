import csv
import query_parser as parse
import operator
import re
import numpy as np
import time
import io
import sys
from btree_search import get_rows
from os.path import exists
file_path = 'C:/Users/Lenovo/Desktop/QueryCSV-master/'
idx_path = 'C:/Users/Lenovo/Desktop/QueryCSV-master/index/'

def getrow(fname, loclist, num):
    #fname is a string. loclist is the list from getloc, num is the row number to locate
    f = open(fname, "r")
    f.seek(loclist[num])
    reader = csv.reader(f)
    res = next(reader)
    f.close()
    return(res)

def getloc_r_p(fname):
    #fname is a string. ex:"review-5k.csv"
    f = io.open(fname, encoding = "utf8", newline="\r\n")
    od = []

    while 1:
        od.append(f.tell())
        line = f.readline()
        if not line:
            break

    f.close()
    newod = od[0:len(od)-1]
    
    flag = [0] * len(newod)
    
    f = open(fname, "r")
    reader = csv.reader(f)
    row = next(reader)
    for i in range(len(newod)):
        fcopy = open(fname, "r")
        fcopy.seek(newod[i])
        xreader = csv.reader(fcopy)
        tmp = next(xreader)
        fcopy.close()
        if row!=tmp:
            flag[i] = 1
            continue
        elif i!=len(newod)-1:
            row = next(reader)
            
    f.close()
        
    finalod = []
    for i in range(len(newod)):
        if flag[i]==0:
            finalod.append(newod[i])
    
    #print("len(finalod)", len(finalod))
    return(finalod)


def get_index(filename, attr):
    """
    find the index of one attribute
    :param filename:
    :param attr:
    :return: integer
    """
    try:
        tag_name = np.load(filename)
        tag_name = [tag.lower() for tag in tag_name]
        try:
            return tag_name.index(attr.lower())
        except ValueError:
            print('No such attribute:', attr)
    except Exception:
        print('No such file:', filename)
    return -1




def projection(before_pro, file, attributes):
	table_num = len(file) #how many files
	pro_size = len(before_pro[0])  #size of found index from one file

####################################################################
	attri_dict = {} #to merge all attri by filename

	for name_attri in attributes:
		#print(name_attri)
		if name_attri[0] not in attri_dict:
			attri_dict[name_attri[0]] = list()
		attri_dict[name_attri[0]].append(name_attri[1])
		#print(attri_dict[name_attri[0]])
####################################################################
	file_dict_attri_idx_lst = {}

	for i in range(table_num):
		filename = file[i][0]
		attri_lst = attri_dict[filename]
		fname = idx_path + filename.replace(".csv", "tag.npy")
		#print(fname)
		for entry in attri_lst:
			#print(entry)
			attri_idx = get_index(fname, entry)
			if filename not in file_dict_attri_idx_lst:
				#print(attri_idx)
				file_dict_attri_idx_lst[filename] = list()
			file_dict_attri_idx_lst[filename].append(attri_idx)
	print(file_dict_attri_idx_lst)
	#a dict of k = file.csv, v = list of attribute idx
####################################################################
	output_list = list()

	for i in range(pro_size):
		temp = list()
		for j in range(table_num):
			this_row = list() #store one row
			row_number = before_pro[j][i]
			filename = file[j][0]
			locallist = file[j][1]
			print('row:',row_number)
			print('size',len(locallist))
			print('filename:', filename)
			this_row = getrow(filename, locallist, row_number+1)
			#invoke get_index() to get attribute index
			idx_lst = file_dict_attri_idx_lst[filename]
			#print(idx_lst)
			#print('5555555555:',this_row[5])
			for entry in idx_lst:
				#print(entry)
				
				temp.append(this_row[entry])
		output_list.append(temp)

	return output_list

ff1 = "review.csv"
flist1 = np.load('C:/Users/Lenovo/Desktop/QueryCSV-master/index/reviewloc.npy')
ff2 = "business.csv"
flist2 = np.load('C:/Users/Lenovo/Desktop/QueryCSV-master/index/businessloc.npy')
ff3 = "photos.csv"
flist3 = np.load('C:/Users/Lenovo/Desktop/QueryCSV-master/index/photosloc.npy')
before_pro = [[69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 69770, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 8349, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 42435, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 44326, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 28590, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 81398, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 73142, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 86276, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113735, 113713, 113713, 113713, 113713, 113713, 113713, 113713, 113713, 113713, 113713, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 97695, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 121591, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346, 86346], [948898, 948901, 948903, 948908, 948911, 948917, 995556, 995557, 995558, 995567, 995568, 995569, 995582, 995594, 995596, 995598, 995599, 995600, 995601, 995602, 995612, 682620, 682622, 682625, 682626, 682628, 692422, 692425, 692429, 692433, 692434, 692439, 692442, 692448, 692451, 692452, 692453, 692454, 692457, 692458, 692460, 692468, 692472, 692476, 692477, 692482, 692497, 692500, 692505, 198460, 198462, 198464, 199004, 199005, 199007, 199008, 199009, 199013, 199017, 199019, 199020, 199022, 199024, 199025, 199026, 199027, 199028, 199029, 199031, 199034, 199035, 199036, 199037, 199040, 199043, 199044, 199045, 199048, 199050, 199051, 199056, 199057, 199058, 199059, 199060, 199061, 199068, 199069, 199070, 199073, 199074, 199079, 199081, 199082, 199085, 199087, 199088, 199089, 199091, 199092, 245907, 245914, 245915, 245916, 245917, 245922, 245923, 245925, 245926, 245927, 245928, 245929, 245930, 245931, 245938, 245940, 245943, 245947, 245951, 198460, 198462, 198464, 199004, 199005, 199007, 199008, 199009, 199013, 199017, 199019, 199020, 199022, 199024, 199025, 199026, 199027, 199028, 199029, 199031, 199034, 199035, 199036, 199037, 199040, 199043, 199044, 199045, 199048, 199050, 199051, 199056, 199057, 199058, 199059, 199060, 199061, 199068, 199069, 199070, 199073, 199074, 199079, 199081, 199082, 199085, 199087, 199088, 199089, 199091, 199092, 245907, 245914, 245915, 245916, 245917, 245922, 245923, 245925, 245926, 245927, 245928, 245929, 245930, 245931, 245938, 245940, 245943, 245947, 245951, 318088, 318091, 318094, 318095, 318097, 318099, 318102, 318103, 318104, 318105, 318106, 318107, 318108, 318109, 318110, 318112, 318113, 318115, 318121, 318124, 318133, 318134, 318135, 318139, 318141, 318142, 318143, 318144, 318147, 318150, 318151, 318153, 318155, 318156, 318159, 318160, 318161, 318163, 318164, 318165, 318171, 360896, 360898, 360900, 360901, 360902, 360903, 360904, 360907, 360911, 360913, 360914, 360915, 360916, 360917, 360920, 360922, 360927, 360933, 360938, 360939, 360945, 360947, 360949, 360950, 360953, 360957, 360958, 360959, 360960, 360961, 360962, 360965, 360969, 360971, 360974, 925428, 925437, 925446, 925454, 925459, 925463, 925477, 925490, 925494, 925495, 925503, 925508, 925428, 925437, 925446, 925454, 925459, 925463, 925477, 925490, 925494, 925495, 925503, 925508, 925428, 925437, 925446, 925454, 925459, 925463, 925477, 925490, 925494, 925495, 925503, 925508, 925428, 925437, 925446, 925454, 925459, 925463, 925477, 925490, 925494, 925495, 925503, 925508, 319203, 319240, 337958, 337961, 337969, 337975, 319203, 319240, 337958, 337961, 337969, 337975, 319203, 319240, 337958, 337961, 337969, 337975, 319203, 319240, 337958, 337961, 337969, 337975, 440466, 440469, 440472, 440476, 440477, 440480, 440481, 440482, 440484, 440486, 440490, 440493, 440466, 440469, 440472, 440476, 440477, 440480, 440481, 440482, 440484, 440486, 440490, 440493, 40774, 40775, 40776, 40789, 40790, 40791, 40796, 40798, 40800, 40803, 40805, 40810, 40817, 40818, 40820, 40821, 40822, 40823, 40828, 40831, 40832, 40837, 40839, 40841, 40844, 40847, 40848, 230333, 751898, 751900, 751902, 751906, 751908, 751909, 751914, 751915, 751922, 751930, 751935, 751937, 751939, 751940, 751941, 751942, 751946, 751947, 751948, 751953, 751955, 751957, 768160, 768163, 768167, 768171, 768176, 768178, 768181, 768190, 768195, 768203, 336030, 336032, 336036, 336037, 336042, 336044, 336052, 336054, 336056, 336060, 264531, 264533, 264534, 264535, 264538, 264539, 264531, 264533, 264534, 264535, 264538, 264539, 264531, 264533, 264534, 264535, 264538, 264539, 264531, 264533, 264534, 264535, 264538, 264539, 180359, 180360, 180362, 180363, 180365, 180367, 180371, 180375, 180377, 180379, 180382, 180384, 180386, 180387, 180388, 180390, 180391, 180393, 180394, 180396, 180397, 180399, 180404, 180405, 180407, 180412, 180414, 180415, 180417, 180418, 180422, 180423, 180424, 180431, 180432, 180434, 180440, 180442, 180443, 180444, 180445, 180448, 180455, 180456, 180458, 180462, 180463, 180465, 180466, 180467, 180468, 180469, 180471, 180472, 180475, 180476, 180479, 180483, 180484, 180488, 180489, 180490, 180491, 236562, 236565, 236568, 236569, 236575, 236577, 236578, 236580, 180359, 180360, 180362, 180363, 180365, 180367, 180371, 180375, 180377, 180379, 180382, 180384, 180386, 180387, 180388, 180390, 180391, 180393, 180394, 180396, 180397, 180399, 180404, 180405, 180407, 180412, 180414, 180415, 180417, 180418, 180422, 180423, 180424, 180431, 180432, 180434, 180440, 180442, 180443, 180444, 180445, 180448, 180455, 180456, 180458, 180462, 180463, 180465, 180466, 180467, 180468, 180469, 180471, 180472, 180475, 180476, 180479, 180483, 180484, 180488, 180489, 180490, 180491, 236562, 236565, 236568, 236569, 236575, 236577, 236578, 236580, 72328, 72331, 72332, 72328, 72331, 72332, 72328, 72331, 72332, 72328, 72331, 72332, 72328, 72331, 72332, 72328, 72331, 72332, 72328, 72331, 72332], [3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3331, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3349, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3370, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 3373, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 14184, 30178, 30178, 30178, 30178, 30178, 30178, 30178, 30178, 30178, 30178, 30178, 30178, 30180, 30180, 30180, 30180, 30180, 30180, 30180, 30180, 30180, 30180, 30180, 30180, 30181, 30181, 30181, 30181, 30181, 30181, 30181, 30181, 30181, 30181, 30181, 30181, 30182, 30182, 30182, 30182, 30182, 30182, 30182, 30182, 30182, 30182, 30182, 30182, 30477, 30477, 30477, 30477, 30477, 30477, 30479, 30479, 30479, 30479, 30479, 30479, 30481, 30481, 30481, 30481, 30481, 30481, 30483, 30483, 30483, 30483, 30483, 30483, 43093, 43093, 43093, 43093, 43093, 43093, 43093, 43093, 43093, 43093, 43093, 43093, 43094, 43094, 43094, 43094, 43094, 43094, 43094, 43094, 43094, 43094, 43094, 43094, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 82998, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 96638, 125234, 125234, 125234, 125234, 125234, 125234, 125234, 125234, 125234, 125234, 139201, 139201, 139201, 139201, 139201, 139201, 139202, 139202, 139202, 139202, 139202, 139202, 139203, 139203, 139203, 139203, 139203, 139203, 139205, 139205, 139205, 139205, 139205, 139205, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156848, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 156850, 192657, 192657, 192657, 192658, 192658, 192658, 192659, 192659, 192659, 192660, 192660, 192660, 192661, 192661, 192661, 192662, 192662, 192662, 192663, 192663, 192663]]
file = [[ff2,flist2],[ff1,flist1],[ff3,flist3]]
attributes = [['review.csv','review_id'],['review.csv','stars'],['review.csv','useful'],['business.csv','business_id'],['business.csv','state'], ['photos.csv','label']]

print(projection(before_pro, file, attributes))












