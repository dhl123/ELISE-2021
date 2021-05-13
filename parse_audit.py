import operator
from collections import defaultdict
import pickle
import sys
import numpy as np
import json
import argparse
parser = argparse.ArgumentParser(description='Input')
parser.add_argument('-param_file', action='store', dest='param_file',
                    help='param file file')
parser.add_argument('-input', action='store', dest='input_file_path',
                    help='input file path')
parser.add_argument('-output', action='store',dest='output_file_path',
                    help='output file path')
args = parser.parse_args()
#import json

with open(args.input_file_path, 'rb') as fp:
    data = fp.read()
data=str(data)
from collections import Counter
import re
import time
def translate_time(time_):
    day=time_.split('.')
    return [day[0],day[1]]
conflict_dict={}
def get_dict_allkeys_values(dict_a,values,mins,audit_type,arch,success,types):
        if isinstance(dict_a, dict): 
            for x in range(len(dict_a)):
                temp_key = list(dict_a.keys())[x]
                temp_value = dict_a[temp_key]
                if str(temp_value)=='None':
                    values.append('null')
                elif str(temp_value)=='False':
                    values.append('false')
                elif temp_key=='audit_epoch':
                    if int(translate_time(dict_a[temp_key])[0])<mins[0]:
                        mins[0]=int(translate_time(dict_a[temp_key])[0])
                elif temp_key=='audit_counter':
                    if int(dict_a[temp_key])<mins[1]:
                        mins[1]=int(dict_a[temp_key])
                elif temp_key=='audit_type':
                    if dict_a[temp_key] not in audit_type:
                        audit_type.append(dict_a[temp_key])
                elif temp_key=='type':
                    if dict_a[temp_key] not in types:
                        types.append(dict_a[temp_key])
                elif temp_key=='arch':
                    if dict_a[temp_key] not in arch:
                        arch.append(dict_a[temp_key])
                elif temp_key=='success':
                    if dict_a[temp_key] not in success:
                        success.append(dict_a[temp_key])
                else:
                    if temp_value.isnumeric():
                        if str(temp_key) not in conflict_dict.keys():
                            conflict_dict[str(temp_key)]=[]
                        conflict_dict[str(temp_key)].append(temp_value)
                    if len(str(temp_value))>2:
                        values.append(str(temp_value)+'**'+str(temp_key))
        return values
import sys
def count(data):
    data_=data.split("}{")[:-1]
    if len(data_)>17088238:
        data_[17088237]=data_[17088238]
    if len(data_)>37259958:
        data_[37259957]=data_[37259958]

#    data_[4292665]=data_[4292666]
#    data_[3467833]=data_[3467834]
    data_[0]=data_[0][3:]
    audit_type=[]
    arch=[]
    success=[]
    types=[]
    mins=[sys.maxsize,sys.maxsize]
#    data_[-1]=data_[-1][:-2]
    values=[]
    for i in range(len(data_)):
        json_obj="{"+data_[i]+"}"
        json_obj=json.loads(json_obj)
        get_dict_allkeys_values(json_obj,values,mins,audit_type,arch,success,types)
    return Counter(values),mins,audit_type,arch,success,types

global re_keys
global re_values
values,mins,audit_type,arch,success,types=count(data)
values=sorted(values.items(), key=lambda values:values[1]*len(values[0].split("**")[0]), reverse=True)
values=dict(values)
tmp_dict={}
tmp_keys=list(values.keys())
for i in range(len(tmp_keys)):
    tmp_keys[i]=tmp_keys[i].split('**')[0]
    if tmp_keys[i] not in tmp_dict.keys():
        tmp_dict[tmp_keys[i]]=[i]
    else:
        tmp_dict[tmp_keys[i]].append(i)
tmp_keys=list(values.keys())
tmp_keys2=list(tmp_dict.keys())   #value [1,2,3]
final_dict={}

for i in range(len(tmp_keys2)):
    index=tmp_keys2[i]
    count=0
    for j in tmp_dict[tmp_keys2[i]]:
        index=index+'**'+tmp_keys[j].split("**")[1]
        count=count+values[tmp_keys[j]]*len(tmp_keys[j].split("**")[0])
    final_dict[index]=count
final_dict=sorted(final_dict.items(), key=lambda final_dict:final_dict[1], reverse=True)
#for i in values.keys():
#    key_ids=
minsss=0
for i in range(len(final_dict)):
    if int(final_dict[i][1])<20000:
        break
    else:
        minsss=minsss+1
final_dict=final_dict[:minsss]

#final_dict=final_dict[:170]  #40
#final_dict=dict(final_dict)
#print(final_dict)
#final_dict=sorted(final_dict.items(), key=lambda final_dict:int(final_dict[1])/len(final_dict[0].split("**")[0]), reverse=True)
print(final_dict)
re_values=[]
re_keys={}
for name in conflict_dict.keys():
    re_keys[name]=[]
for (i,c) in final_dict:
    tmpp=i.split("**")
    re_values.append(tmpp[0])
   # re_keys.append(tmpp[1:])
    for j in tmpp[1:]:
        conflict_value=[]
        if str(j) in conflict_dict.keys():
            conflict_value=conflict_dict[str(j)]
        if j not in re_keys.keys():
            re_keys[j]=[]
            while str(len(re_keys[j])) in conflict_value:
                re_keys[j].append('**-1**')
            re_keys[j].append(tmpp[0])
        else:
            while str(len(re_keys[j])) in conflict_value:
                re_keys[j].append('**-1**')
            re_keys[j].append(tmpp[0])
#values=final_dict[]
#values=dict(values)
print(re_keys)
print(re_values)

import pickle
key_template=[]
with open('hpack_key_audit.pickle','rb') as f:
    key_template=pickle.load(f)

key_template_dict={c:i for (i,c) in enumerate(key_template)}
#print(intervel)
#exit()
def process_pid(json_obj_key,char2id_dict,id2char_dict,data_processed):

    if json_obj_key not in char2id_dict:
        for tmpchar in json_obj_key:
            if tmpchar not in char2id_dict:
                end=len(char2id_dict)+4
                char2id_dict[tmpchar]=end
                id2char_dict[end]=tmpchar
                data_processed.append(end)
            else:
                data_processed.append(char2id_dict[tmpchar])
    else:
        data_processed.append(char2id_dict[json_obj_key])
    data_processed.append(1)


def handle_block(data_,char2id_dict,id2char_dict,mins,audit_type,arch,success,types):
    data_processed=[]
    flag=0
    for i in range(len(data_)):
        json_obj=data_[i]
        json_obj=json.loads(json_obj)
        pid_key_list=['uid','gid','arch','host','pid','ppid']
        tmplist=list(json_obj.keys())
        tmplist.sort()
        if flag==0:
            flag=1
            common_key=[val for val in tmplist if val in pid_key_list]
            data_processed.append(3)
            for com_key in common_key:
                temp_value=json_obj[com_key]
                if temp_value in re_values:
                    temp_value=str(re_keys[com_key].index(temp_value))
#                if com_key=='auid':
#                    print(temp_value)
                process_pid(temp_value,char2id_dict,id2char_dict,data_processed)
            data_processed.append(3)
        for k in str(key_template_dict[','.join(tmplist)]):
            if k not in char2id_dict:
                end=len(char2id_dict)+4
                char2id_dict[k]=end
                id2char_dict[end]=k
                data_processed.append(end)
            else:
                data_processed.append(char2id_dict[k])
        data_processed.append(0)
        temp_key=[val for val in tmplist if val not in common_key]
        for x in temp_key:
            temp_value = str(json_obj[x])
            if x=='audit_counter':
                temp_value=str(int(temp_value)-mins[1])
            if x=='audit_epoch':
                tmp_time,tmp_order=translate_time(temp_value)
                tmp_time=str(int(tmp_time)-mins[0])
                temp_value=tmp_time+' '+tmp_order
            if x=='success':
                temp_value=str(success.index(temp_value))
            if x=='arch':
                temp_value=str(arch.index(temp_value))
            if x=='audit_type':
               # print(temp_value)
                temp_value=str(audit_type.index(temp_value))
                #print(temp_value)
            if x=='type':
                temp_value=str(types.index(temp_value))
            if temp_value in re_values and x not in ['audit_counter','audit_epoch','success','arch','audit_type','type']:
                temp_value=str(re_keys[x].index(temp_value))
            if temp_value not in char2id_dict:
                for tmpchar in temp_value:
                    if tmpchar not in char2id_dict:
                        end=len(char2id_dict)+4
                        char2id_dict[tmpchar]=end
                        id2char_dict[end]=tmpchar
                        data_processed.append(end)
                    else:
                        data_processed.append(char2id_dict[tmpchar])
            else:
                data_processed.append(char2id_dict[temp_value])
            data_processed.append(1)
        data_processed.append(2) 
    data_processed.append(3)   
    return data_processed
def handle_normal(json_obj,char2id_dict,id2char_dict,mins,audit_type,arch,success,types):
    data_processed=[]
    tmplist=list(json_obj.keys())
    tmplist.sort()
    #print(tmplist)
    for k in str(key_template_dict[','.join(tmplist)]):
        if k not in char2id_dict:
            end=len(char2id_dict)+4
            char2id_dict[k]=end
            id2char_dict[end]=k
            data_processed.append(end)
        else:
            data_processed.append(char2id_dict[k])
    data_processed.append(0)
    for x in range(len(tmplist)):
        temp_key = tmplist[x]
        temp_value = str(json_obj[temp_key])
        if temp_key=='audit_counter':
            temp_value=str(int(temp_value)-mins[1])
        if temp_key=='audit_epoch':
            tmp_time,tmp_order=translate_time(temp_value)
            tmp_time=str(int(tmp_time)-mins[0])
            temp_value=tmp_time+' '+tmp_order
        if temp_key=='success':
            temp_value=str(success.index(temp_value))
        if temp_key=='arch':
            temp_value=str(arch.index(temp_value))
        if temp_key=='audit_type':
           # print("HHHHHHHHHHHHHHHHHHHHH")
            temp_value=str(audit_type.index(temp_value))
        if temp_key=='type':
            temp_value=str(types.index(temp_value))
        if temp_value in re_values and temp_key not in ['audit_counter','audit_epoch','success','arch','audit_type','type']:
            temp_value=str(re_keys[temp_key].index(temp_value))        
        if temp_value not in char2id_dict:
            for tmpchar in temp_value:
                if tmpchar not in char2id_dict:
                    end=len(char2id_dict)+4
                    char2id_dict[tmpchar]=end
                    id2char_dict[end]=tmpchar
                    data_processed.append(end)
                else:
                    data_processed.append(char2id_dict[tmpchar])
        else:
            data_processed.append(char2id_dict[temp_value])
        data_processed.append(1)
    data_processed.append(2)
    return data_processed

def exec(data):
    data_=data.split("}{")[:-1]#[1200000:]
    if len(data_)>17088238:
        data_[17088237]=data_[17088238]
    if len(data_)>37259958:
        data_[37259957]=data_[37259958]

 #   data_[4292665]=data_[4292666]

 #   data_[3467833]=data_[3467834]
    data_[0]=data_[0][3:]
 #   data_[-1]=data_[-1][:-2] #testdataset -4  original -2
    pid_=defaultdict(list)
    for i in range(len(data_)):
        data_[i]="{"+data_[i]+"}"
        json_obj=data_[i]
        json_obj=json.loads(json_obj)
        if 'pid' in json_obj.keys():
            pid_[json_obj['pid']].append(data_[i])
    return pid_


def addsdict(data):
    data_=data.split("}{")[:-1]#[1200000:]
  #  data_[4292665]=data_[4292666]
#i
    if len(data_)>17088238:
        data_[17088237]=data_[17088238]
    if len(data_)>37259958:
        data_[37259957]=data_[37259958]

 #   data_[3467833]=data_[3467834]
    data_[0]=data_[0][3:]
  #  data_[-1]=data_[-1][:-2]
    data_processed=[]
    char2id_dict={}
    id2char_dict={}
    pid_=exec(data)
#    data_processed=[]
    for i in range(len(data_)):
        json_obj="{"+data_[i]+"}"
       # print(json_obj)
        json_obj=json.loads(json_obj)
       # print(json_obj)
        if 'pid' in json_obj.keys():
            #print(pid_[json_obj['pid']])
            if pid_[json_obj['pid']] != -1:
                data_processed.append(handle_block(pid_[json_obj['pid']],char2id_dict,id2char_dict,mins,audit_type,arch,success,types))
                pid_[json_obj['pid']]=-1
        else:
            data_processed.append(handle_normal(json_obj,char2id_dict,id2char_dict,mins,audit_type,arch,success,types))       

    return char2id_dict,id2char_dict,data_processed 

char2id_dict,id2char_dict,data_processed=addsdict(data)
params = {'char2id_dict':char2id_dict, 'id2char_dict':id2char_dict,'key_template_dict':key_template_dict,'mins':mins,'audit_type':audit_type,'arch':arch,'success':success,'types':types,'re_values_dict':[re_keys,re_values]}
#exit()

with open(args.param_file, 'w') as f:
    json.dump(params, f, indent=4)
out = [c for item in data_processed for c in item]
integer_encoded = np.array(out)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
np.save(args.output_file_path, integer_encoded)
