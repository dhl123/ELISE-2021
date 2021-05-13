import sys
import numpy as np
import json
import argparse
parser = argparse.ArgumentParser(description='Input')
parser.add_argument('-input', action='store', dest='input_file_path',help='input file')
args = parser.parse_args()

with open(args.input_file_path, 'rb') as fp:
    data = fp.read()
#print(data)
data=str(data)

import pickle
def count(data):
    data_=data.split("}{")[:-1]
 #   print(len(data_))
#    data_[17088237]=data_[17088238]  

#    data_[37259957]=data_[37259958] 
#    data_[3467833]=data_[3467834]
#  exit()
    data_[0]=data_[0][3:]
    key_list=[]
    for i in range(len(data_)):
        data_[i]="{"+data_[i]+"}"
        json_obj=data_[i]
        json_obj=json.loads(json_obj)
        tmplist=list(json_obj.keys())
        tmplist.sort()
        key_list.append(','.join(tmplist))
    return key_list
key_list=count(data)
#print(len(key_list))
key_final=[]
for i in key_list:
    if i not in key_final:
        key_final.append(i)
#key_final=enumerate(key_final)
print(key_final)
with open('hpack_key_audit.pickle','wb') as f:
    pickle.dump(key_final,f)

