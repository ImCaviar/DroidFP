# -*- coding:utf-8 -*-
# 预处理android_basic.csv表
import csv
import re

# 模拟器序号
emulator = [5,11,62,107,108,122,126,128,132,134,135,136,137,138,139,140,141,143,148,151,152,157,159,160,161,162,163]
# 枚举数据所在列数
enum = [1, 8, 10, 11, 14, 16, 32, 40, 36, 37, 45, 46, 47, 50, 52, 53, 62, 63, 65, 73, 76, 77, 81, 82, 90, 87]
# 提取数值，空白作-1
extract = [2, 6, 7, 20, 21, 24, 26, 27, 28, 29, 31, 33, 34, 35, 38, 41, 42, 44, 48, 49, 55, 57, 59, 61, 64, 66, 67, 68, 69, 71, 74, 75, 78, 79, 80, 83, 84, 85, 89, 91]
# 布尔型数据
bbool = [3, 19]
# 映射0-9A-Za-z到0-61，62进制表示字符串
str62 = [12, 22, 40, 43, 60]
# 按指定字符分割字符串，取4个字符串，62进制数值化并加权求和
split_4str = [15, 30, 58]
# 提取16进制数字，null作0，空白作-1
num16 = [17, 39, 51]
# 分割字符串，枚举+数值化，加权求和
split_num_str = [25, 87]

# 用字典存储枚举列表
dict_enum = {'str1':[],'str8':[],'str10':[],'str11':[],'str14':[],'str16':[], 'str32':[], 'str40':[],'str36':[],'str37':[],'str45':[],'str46':[],'str47':[],'str50':[],'str52':[],'str53':[],'str62':[],'str63':[],'str65':[],'str73':[],'str76':[],'str77':[],'str81':[],'str82':[],'str90':[],'str87':[]}
# 枚举法处理属性值，空白作-1，返回单个数值
def deal_enum(var, list):
    if var == '':
        return -1
    elif var in list:
        return list.index(var)
    else:
        list.append(var)
        return list.index(var)

# 直接提取字符串中的数值，空白作-1，返回单个数值
def deal_extract(var):
    if var == '':
        return -1
    else:
        num = float(var)
        return num

# 处理布尔型数据，"TRUE"/"is Emulator"->1;"FALSE"/"is not Emulator"->0;空白->-1，返回单个数值
def deal_bool(var):
    if var == '':
        return -1
    elif var == "TRUE" or var == "is Emulator":
        return 1
    else:
        return 0

# 处理E列，提取MemTotal、MemFree、MemAvailable、Active、Inactive、SwapTotal、SwapFree、VmallocTotal、VmallocUsed、CmaTotal、CmaFree对应的数据信息，返回列表
def deal_4(var):
    # 子属性名称
    attr = ['MemTotal:','MemFree:','MemAvailable:','Active:','Inactive:','SwapTotal:','SwapFree:','VmallocTotal:','VmallocUsed:','CmaTotal:','CmaFree:']
    value = []
    # 某一项子属性为空，则其对应的数值置-1，否则提取kB前的数值
    if var == '':
        for x in range(len(attr)):
            value.append(-1)
    else:
        for a in attr:
            if a in var:
                temp = var.split(a)
                num = re.findall(r'\d+', temp[1])
                value.append(int(num[0]))
            else:
                value.append(-1)
    return value

# 处理F列，以/为单位分割字符串，将分割后的字符串的ASCII码相加，然后加权求和，返回单个数值
def deal_5(var):
    # 空值返回-1
    if var == '':
        return -1
    else:
        str = re.split(' |/|:|\.',var)
        # 删除列表中的所有空元素
        while '' in str:
            str.remove('')
        # num_list存储所有的分割后的字符串对应的数据
        num_list = []
        for s in str:
            num = 0
            for l in s:
                num = num*80+ord(l)-48 # 以字符0对应的ASCII码为0
            num_list.append(num)
        # 对num_list里的数据加权求和
        num = 0
        for n in num_list:
            num = num*10+n
        return num

# 处理J列，提取时间为数字，例如GMT+08:00->8，GMT-05:00->-5，返回单个数值
def deal_9(var):
    # 空值返回-1
    if var == '':
        return -1
    else:
        num = re.findall(r'\d+', var)
        if '+' in var:
            return int(num[0])
        else:
            return 0-int(num[0])

# 处理M/W/AO/AR/BI列，将0-9A-Za-z分别映射到0-61，用62进制表示字符串，若字符串中出现.-_ ()之类的标点，将第一个标点转换成小数点，其它的标点直接去掉，例如OPR1.170623.027->[24][25][27][1][.][170623027]，返回单个数值
def deal_str62(var):
    # 空值返回-1
    if var == '':
        return -1
    else:
        letter_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        # 处理var中的字符，小数点前后分开处理
        point = 0
        intt = 0
        decc = 0
        for l in var:
            if l in letter_map and point == 0:
                intt = intt*62+letter_map.index(l)
            elif l not in letter_map and point == 0:
                point = 1
            elif l in letter_map and point == 1:
                decc = decc*62+letter_map.index(l)
            else:
                continue
        result = float(intt)+float('0.'+str(decc))
        return result

# 处理N列，将0-9A-Za-z分别映射到0-61，用62进制表示字符串，返回单个数值
def deal_13(var):
    # 空值返回-1
    if var == '':
        return -1
    else:
        letter_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        num = 0
        for l in var:
            if l in letter_map:
                num = num*62+letter_map.index(l)
            else:
                continue
        return num

# 处理P/AE/BG列，先把空格-_.前后字符串切分开，取前4个字符串（如果有的话），将0-9A-Za-z分别映射到0-61，然后加权求和，返回单个数值
def deal_str4(var):
    # 空值返回-1
    if var == '':
        return -1
    else:
        letter_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        num = [] # 存放<=4个字符串对应的数字
        # 分割字符串
        str = re.split(' |\.|-|_|\(|\)',var)
        # 映射
        for i, s in enumerate(str):
            if i<4:
                n = 0
                for l in s:
                    if l in letter_map:
                        n = n * 62 + letter_map.index(l)
                    else:
                        continue
                num.append(n)
            else:
                break
        # 加权求和
        result = 0
        for n in num:
            result = result*1000 + n
        return result

# 处理R/AN/AZ列，直接提取16进制数，null作0，空白作-1，返回单个数值
def hexadecimal(var):
    if var == '':
        return -1
    elif var == 'null':
        return 0
    else:
        return int(var,16)

# 处理S列，计算有cell,bluetooth,wifi,nfc,wimax中的几项，返回单个数值
def deal_18(var):
    if var == '':
        return 0
    else:
        num = var.count(',')+1
        return num

# 处理X列，截取最后一个/后是test-keys、release-keys还是dev-keys，用0/1/2区分，返回单个数值
def deal_23(var):
    keys = ['test-keys','release-keys','dev-keys']
    if var == '':
        return -1
    else:
        for i,key in enumerate(keys):
            if key in var:
                return i

# 处理Z/CJ列，删除_-.，把剩下的数字和大小写字母作62进制的映射，返回单个数值
def deal_25(var):
    if var == '':
        return -1
    else:
        letter_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        num = 0
        str = re.sub(r'_|-|\.','',var)
        # 拼接字符串
        temp = ''
        for s in str:
            temp += s
        # 62进制映射
        for s in temp:
            if s in letter_map:
                num = num*62+letter_map.index(s)
        return num

# 处理BC列，Linux version和gcc version后面的数字提取出来，以第一个.为小数点，记作浮点型数值，返回两个数值
def deal_54(var):
    if var == '':
        return -1,-1
    else:
        # Linux version的格式为X.X.X
        str = var.split('Linux version')[1]
        linux = re.findall(r'\d+.\d+.\d+',str)[0]
        l = linux.split('.')
        lv = float(l[0]+'.'+l[1]+l[2])
        # gcc version的格式为X.X
        str = var.split('gcc version')[1]
        gcc = re.findall(r'\d+.\d+',str)[0]
        gv = float(gcc)
        return lv,gv

# 处理BE列，对rootfs、tmpfs、none、/data/media对应的数据中提取1K-blocks数值（字符串后的第一个数字），如无对应项，则记为-1，返回列表
def deal_56(var):
    attr = ['rootfs','tmpfs','none','/data/media']
    result = []
    for a in attr:
        if a in var:
            str = var.split(a)
            num = re.findall(r'\d+',str[1])[0]
            result.append(int(num))
        else:
            result.append(-1)
    return result

# 处理BS列，把第一个.作为小数点，后面的.去掉，记作浮点型数值，返回单个数值
def deal_70(var):
    if var == '':
        return -1
    else:
        point_num = var.count('.')
        if point_num == 0:
            return int(var)
        elif point_num == 1:
            return float(var)
        else:
            num = re.findall(r'\d+',var)
            result = num[0] + '.'
            for i in range(1,len(num)):
                result += num[i]
            return float(result)

# 处理BU列，把density, width, height, scaledDensity, xdpi后的数值提取出来，返回列表
def deal_72(var):
    attr = ['density','width','height','scaledDensity','xdpi']
    result = []
    for a in attr:
        if a in var:
            str = var.split(a)
            num = re.findall(r'\d+.?\d+', str[1])[0]
            result.append(float(num))
        else:
            result.append(-1)
    return result

# 处理CI列，统计total后对应的数值，返回单个数值
def deal_86(var):
    if var == '':
        return -1
    else:
        if 'total' in var:
            str = var.split('total')
            num = re.findall(r'\d+',str[1])[0]
            return int(num)
        else:
            return 0

# 处理CK列，Android后的数字把第一个.作为小数点，后面的.去掉，将最后一个；后面/前后的字符串分别枚举，并加权求和，返回两个数值
# 枚举所用的列表分别为version、model
version = []
model = []
def deal_88(var):
    if var == '':
        return -1,-1
    else:
        # 提取Android版本信息，并转化成浮点型数字
        android = float(0)
        if 'Android' in var:
            str = var.split('Android')
            num = re.findall(r'\d+\.?\d*\.?\d*',str[1])[0]
            point_count = num.count('.')
            if point_count == 0:
                android = float(num)
            elif point_count == 1:
                android = float(num)
            else:
                s = num.split('.')
                result = s[0] + '.'
                for i in range(1,len(s)):
                    result += s[i]
                android = float(result)
        # 将version和model作枚举法处理
        vm_str = var.split(';')[-1]
        if ')' in vm_str:
            vm_str.replace(')','')
        ver = vm_str.split('/')[0]
        mod = vm_str.split('/')[1]
        if ver in version:
            ver_index = version.index(ver)
        else:
            version.append(ver)
            ver_index = version.index(ver)
        if mod in model:
            mod_index = model.index(mod)
        else:
            model.append(mod)
            mod_index = model.index(mod)
        vm = ver_index*100 + mod_index
        return android,vm

# 处理E+字符串的问题
def deal_E(var):
    num = re.findall(r'\d+',var)
    str = num[0]+num[1]
    zero = int(num[2])
    for z in range(zero-2):
        str += '0'
    return str

with open('df_enhance_basic.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    with open('en_basic.csv','w',newline='') as w:
        writer = csv.writer(w)
        for index,row in enumerate(reader):
            new_line = []
            for i, value in enumerate(row):
                if i == 0:          # 直接填充index
                    new_line.append(value)
                elif i in enum:
                    list_name = 'str' + str(i)
                    r = deal_enum(value, dict_enum[list_name])
                    new_line.append(r)
                elif i in extract:
                    if 'E+' in value:
                        value = deal_E(value)
                    r = deal_extract(value)
                    new_line.append(r)
                elif i in bbool:
                    r = deal_bool(value)
                    new_line.append(r)
                elif i in str62:
                    r = deal_str62(value)
                    new_line.append(r)
                elif i in split_4str:
                    r = deal_str4(value)
                    new_line.append(r)
                elif i in num16:
                    if 'E+' in value:
                        value = deal_E(value)
                    r = hexadecimal(value)
                    new_line.append(r)
                elif i in split_num_str:
                    r = deal_25(value)
                    new_line.append(r)
                elif i == 4:
                    rl = deal_4(value)
                    for r in rl:
                        new_line.append(r)
                elif i == 5:
                    r = deal_5(value)
                    new_line.append(r)
                elif i == 9:
                    r = deal_9(value)
                    new_line.append(r)
                elif i == 13:
                    r = deal_13(value)
                    new_line.append(r)
                elif i == 18:
                    r = deal_18(value)
                    new_line.append(r)
                elif i == 23:
                    r = deal_23(value)
                    new_line.append(r)
                elif i == 54:
                    r,s = deal_54(value)
                    new_line.append(r)
                    new_line.append(s)
                elif i == 56:
                    rl = deal_56(value)
                    for r in rl:
                        new_line.append(r)
                elif i == 70:
                    r = deal_70(value)
                    new_line.append(r)
                elif i == 72:
                    rl = deal_72(value)
                    for r in rl:
                        new_line.append(r)
                elif i == 86:
                    r = deal_86(value)
                    new_line.append(r)
                elif i == 88:
                    r,s = deal_88(value)
                    new_line.append(r)
                    new_line.append(s)
            # 插入一列作为label
            id = int(index/100)+1
            if id < 20 and id in emulator:
                new_line.append(1)  # 1为模拟器
            elif id >= 20 and id+1 in emulator:
                new_line.append(1)
            else:
                new_line.append(0)  # 0为真实用户
            writer.writerow(new_line)