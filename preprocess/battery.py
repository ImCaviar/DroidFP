# -*- coding:utf-8 -*-
# 预处理android_battery.csv表
import csv

# 模拟器序号
emulator = [5,10,61,106,107,121,125,127,131,133,134,135,136,137,138,139,140,142,147,150,151,156,158,159,160,161,162]
# bool型数据所在列数，"TRUE"->1;"FALSE"->0
bools = [2]
# 枚举数据所在列数
enums = [5,9,10,12]

# 用字典存储枚举列表
dict_enum = {'str5':[],'str9':[],'str10':[],'str12':[]}

# 处理bool型数据
def deal_bool(var):
    if var == "TRUE":
        return 1
    else:
        return 0

# 处理枚举数据
def deal_enum(var, list):
    if var in list:
        return list.index(var)
    else:
        list.append(var)
        return list.index(var)

with open('df_enhance_battery.csv','r') as f:
    reader = csv.reader(f)
    with open('en_battery.csv','w',newline='') as w:
        writer = csv.writer(w)
        for index,row in enumerate(reader):
            # 处理bool数据
            for i in bools:
                row[i] = deal_bool(row[i])
            # 处理枚举数据
            for i in enums:
                list_name = 'str'+str(i)
                row[i] = deal_enum(row[i],dict_enum[list_name])
            # 插入一列作为label
            e = 0
            if index >= 162:
                e = int((index-162)/100)+1
            if index < 162 and index+1 in emulator:
                row.append(1)
            elif index < 162 and index+1 not in emulator:
                row.append(0)
            elif index >= 162 and e in emulator:
                row.append(1) # 1为模拟器
            else:
                row.append(0) # 0为真实用户
            writer.writerow(row)
