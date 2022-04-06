import os
import numpy as np
import pandas as pd

path = os.getcwd()  # 当前文件所在路径
filetype = '.dat'  # 指定文件类型
NEDOS=3000 # 对应VASP中的参数设置


def get_filename(path, filetype):
    name = []
    final_name = []
    csv_name=[]
    for root, dirs, files in os.walk(path):
        for i in files:
            if filetype in i:
                name.append(i.replace(filetype, ''))  # 生成不带‘.dat’后缀的文件名组成的列表
    final_name = [item + '.dat' for item in name]  # 生成‘.dat’后缀的文件名组成的列表
    csv_name = [item + '.csv' for item in name]
    return final_name , csv_name  # 输出由有‘.dat’后缀的文件名组成的列表


file_name , csv_name= get_filename(path, filetype)
num=len(file_name)

for j in range(num):
    df0 = pd.read_table(file_name[j], sep='\s+', header=None, engine='python')  # 直接读取dat文件，读取后无空行
    l = len(df0)  # 获取长度
    # l=l+1 #把最后一行空行也算上
    print(l)  # 得到值：3000
    print(df0.head())

    df = df0.iloc[0:NEDOS, :].reset_index(
        drop=True)  # 前3000行数据为第一组（0-300行，第301不取），reset_index(drop=True) 是为了去除原有的index，重新从0生成index

    print(df.tail())

    df_values = locals()
    l = int(l / NEDOS)  # 用除法后要变为int，不然默认float，到后面range部分会出错
    print(l)
    for i in range(2, l + 1):  # range括号左含右不含
        l1 = NEDOS * (i - 1)
        l2 = NEDOS * i
        df_values['df' + str(i)] = df0.iloc[l1:l2, :].reset_index(drop=True)  # 随着i的不同，每301行都取出，index不受原始数据影响，都是从0开始
        df = pd.concat([df, df_values['df' + str(i)]], axis=1,
                       join='outer')  # 将取出的数据横着排列,axis=1，形成新的df，然后与下一个i产生的新的列继续合并直到结束

    print(df)
    df.to_csv(csv_name[j], header=None, index=None)
    print('Done!')

    # input("Press Enter key to exit.")
