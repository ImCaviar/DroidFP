# -*- coding:utf-8 -*-
# 预处理android_thermal.csv表
import csv
import math
import re

# 模拟器序号
emulator = [5,11,62,107,108,122,126,128,132,134,135,136,137,138,139,140,141,143,148,151,152,157,159,160,161,162,163]

# 筛选有效的温度，定义20000-75000之间的温度为正常值，即20-75℃
def filter_thermal(temp):
    new_line = []
    for t in temp:
        num = re.findall(r'\d+',t)
        if t == '':
            continue
        elif int(num[0]) >= 20000 and int(num[0]) <= 75000:
            new_line.append(int(num[0]))
    return new_line

# 计算有效温度值中的最大值、最小值、均值、方差
def mm_thermal(temp):
    mmax = 0
    mmin = 75000
    average = float(0)
    varia = float(0)
    for t in temp:
        num = int(t)
        average += num
        if num > mmax:
            mmax = num
        if num < mmin:
            mmin = num
    if len(temp) == 0:
        average = 0
        varia = 0
    else:
        average = average/float(len(temp))
        for t in temp:
            num = float(t)
            varia += math.pow(num - average, 2)
        varia = varia / float(len(temp))
    return mmax, mmin, average, varia

with open('df_enhance_thermal.csv','r') as f:
    reader = csv.reader(f)
    with open('en_thermal.csv','w',newline='') as w:
        writer = csv.writer(w)
        for i,row in enumerate(reader):
            new_line = []
            # 插入索引
            new_line.append(i+1)
            # 计算有效温度
            row.pop(0)
            effect = filter_thermal(row)
            new_line.append(len(effect))
            # 计算温度中的最大值、最小值、均值和方差
            mmax, mmin, average, varia = mm_thermal(effect)
            new_line.append(mmax)
            new_line.append(mmin)
            new_line.append(average)
            new_line.append(varia)
            # 标记是否为模拟器
            if int(i/100)+1 in emulator:
                new_line.append(1)
            else:
                new_line.append(0)
            writer.writerow(new_line)


