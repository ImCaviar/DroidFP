# -*- coding:utf-8 -*-
# 预处理android_cpu.csv表
import csv
import re

# 模拟器序号
emulator = [5,11,62,107,108,122,126,128,132,134,135,136,137,138,139,140,141,143,148,151,152,157,159,160,161,162,163]
# 如果带单位，去除单位MHz/GHz，提取数字，空白记-1
del_unit = [1,2,3,4,6,7,8,9,10,11,15,17,18]
# 枚举与提值相结合处理架构信息
arch = [5,14]
# 硬件信息枚举列表
hardware = []

# 提取数字，删除单位，空白记-1
def deal_unit(var):
    if var == '':
        return -1
    elif 'MHz' in var:
        return int(var.split('MHz')[0])
    elif 'GHz' in var:
        return int(var.split('GHz')[0])
    else:
        return int(var)

# 枚举与提值相结合，空值-1
def deal_arch(var):
    arch = ['armeabi','arm64','x86','x86_64']
    if var == '':
        return -1
    elif '-' in var:
        # 例如”arm64-v8a“，‘-’前为枚举，‘-’后提取数值
        result = 0
        str = var.split('-')
        result += arch.index(str[0])*10
        # 正则提取'-'后数值
        num = re.findall(r"\d+", str[1])
        result += int(num[0])
        return result
    else:
        # 直接匹配arch中的字符串，索引*10
        return arch.index(var)*10

# 处理CPU Infor这一长串字符串，返回attr_num,hard_name,processor_num,mips,flags
def deal_cpuInfor(var):
    # 统计子属性个数，每个‘：’都对应一个属性名以及属性值
    attr_num = var.count(':')
    # 提取芯片名称，即"Hardware	:"后的字符串
    if "Hardware	:" in var:
        hard = var.split("Hardware	:")[1]
        if hard in hardware:
            hard_name = hardware.index(hard)
        else:
            hardware.append(hard)
            hard_name = hardware.index(hard)
    else:
        hard_name = -1
    # 统计处理器核心数量，即出现多少个"processor"
    processor_num = var.count("processor")
    # 统计BogoMIPS/bogomips的总和
    mips = 0
    if "BogoMIPS	:" in var:
        bogo_list = var.split("BogoMIPS	:")
        bogo_list.pop(0)
        for i in bogo_list:
            num = re.findall(r"\d+\.?\d*",i)
            mips += float(num[0])
    elif "bogomips	:" in var:
        bogo_list = var.split("bogomips	:")
        bogo_list.pop(0)
        for i in bogo_list:
            num = re.findall(r"\d+\.?\d*", i)
            mips += float(num[0])
    # 是否有"flags"这个属性名
    if "flags" in var:
        flags = 1
    else:
        flags = 0
    return attr_num,hard_name,processor_num,mips,flags

# 处理CPU处理器名称
def deal_processor(var):
    # 对于“AArch64 Processor rev 4 (aarch64)”等字符串，取"Processor rev/processor rev"前枚举，"Processor rev/processor rev"后提取数值
    # 对于0、1、空白，都记作-1
    enum = ["AArch64 ","ARMv7 "]
    null = ['0','1','']
    if var in null:
        return -1
    else:
        result = 0
        if "Processor rev" in var:
            pro = var.split("Processor rev")
        elif "processor rev" in var:
            pro = var.split("processor rev")
        result += enum.index(pro[0])*10
        # 提取括号之前的数字
        num = pro[1].split('(')
        n = re.findall(r"\d+", num[0])
        result += int(n[0])
        return result

with open('df_enhance_cpu.csv','r') as f:
    reader = csv.reader(f)
    with open('en_cpu.csv','w',newline='') as w:
        writer = csv.writer(w)
        for index,row in enumerate(reader):
            new_line = []
            for i,value in enumerate(row):
                if i == 0:               # 按设备顺序排序，从1开始
                    new_line.append(index+1)
                elif i == 16:            # 直接填充
                    new_line.append(value)
                elif i in del_unit:      # 去除单位
                    new_line.append(deal_unit(value))
                elif i in arch:          # 处理架构信息
                    new_line.append(deal_arch(value))
                elif i == 12:            # 处理CPU信息
                    attr_num,hard_name,processor_num,mips,flags = deal_cpuInfor(value)
                    new_line.append(attr_num)
                    new_line.append(hard_name)
                    new_line.append(processor_num)
                    new_line.append(mips)
                    new_line.append(flags)
                elif i == 13:            # 处理CPU处理器名称
                    new_line.append(deal_processor(value))
            # 插入一列作为label
            if int(index/100)+1 in emulator:
                new_line.append(1)
            else:
                new_line.append(0)
            writer.writerow(new_line)