# -*- coding: utf-8 -*- 
import pandas as pd  
import os
import numpy as np

def trimmer(folder, file_array, time_skip_head, time_skip_end):
    #根据词典顺序添加每一个传感器的读数，因为file_array里面的内容是词典序的
    #加速度
    df0 = pd.read_csv(folder+'/'+file_array[0])
    #气压读数
    df1 = pd.read_csv(folder + '/'+file_array[1])
    #磁力计
    df2 = pd.read_csv(folder + '/' + file_array[2])
    #注意这里设定的频率是多少
    acc_head = int(time_skip_head*51)
    acc_end = int(time_skip_end*51)
    baro_head = int(time_skip_head*10)
    baro_end = int(time_skip_end*10)
    mag_head = int(time_skip_head*51)
    mag_end = int(time_skip_end*51)
	
    df0[acc_head:-acc_end].to_csv(os.path.join(folder, r'acc.csv'), index=False)
    df1[baro_head:-baro_end].to_csv(os.path.join(folder, r'baro.csv'), index=False)
    df2[mag_head:-mag_end].to_csv(os.path.join(folder, r'mag.csv'), index = False)
	
#进行插值，frequency的单位是纳秒，这里用的是10Hz插值。可以依据相似的办法很容易的扩展到新的传感器数据
def findCommonParts(folder, file_array, frequency = 100000000):
    df0 = pd.read_csv(folder + '/'+file_array[0])
    df1 = pd.read_csv(folder + '/' +file_array[1])
    df2 = pd.read_csv(folder + '/' + file_array[2])
    time0 = df0.UPTIMENANO.values
    time1 = df1.UPTIMENANO.values
    time2 = df2.UPTIMENANO.values
    #可以在这里对数据做一些基础的处理，例如求相反数之类的
    acc = np.sqrt(df0.Ax*df0.Ax + df0.Ay*df0.Ay +df0.Az*df0.Az)
    p = df1.P
    mag = np.sqrt(df2.Mx*df2.Mx + df2.My*df2.My +df2.Mz*df2.Mz)
    
    startTime = min(time0[0], time1[0], time2[0])
    endTime = max(time0[-1], time1[-1], time2[-1])
    
    standardAxis = np.arange(startTime, endTime, frequency)
	
    x = time0
    y = acc.values
    yinter = np.interp(standardAxis, x, y)
    data_acc = pd.DataFrame({"time":standardAxis, "acc":yinter})
    data_acc.to_csv(os.path.join(folder,"acc_new.csv"),index=False)
	
    x1 = time1
    y1 = p.values
    yinter1 = np.interp(standardAxis, x1, y1)
    data_p = pd.DataFrame({"time":standardAxis, "p":yinter1})
    data_p.to_csv(os.path.join(folder,"p_new.csv"), index = False)
	
    x2 = time2
    y2 = mag.values
    yinter2 = np.interp(standardAxis, x2, y2)
    data_mag = pd.DataFrame({"time":standardAxis, "m":yinter2})
    data_mag.to_csv(os.path.join(folder,"mag_new.csv"), index = False)
	
#输进去的文件名
#folder = "201710201445"
#folder = "201710201447"
#folder = "201710201448"
#现在的结构中，这样可以比较批量的处理文件

#folder_pre = 'escalator_up/test'
#folder_list = os.listdir(folder_pre)

folder_pre = 'subway'
folder_list = os.listdir(folder_pre)
for i in folder_list:
    folder = folder_pre + '/' + i
    #指定folder后通过修改这个部分，决定要取出并进行处理的文件有哪些
    file_array =  [i for i in os.listdir(folder) if (i.startswith ('acc') or i.startswith("Baro") or i.startswith('Magne'))]
    print (file_array)
    #后两个参数是trim头和尾的时间，单位是s。输出是acc.csv baro.csv
    trimmer(folder, file_array,8,8)
    #进行同步，上一步trim后文件名已经统一化了，输出是acc_new.csv 和 p_new.csv
    findCommonParts(folder, ['acc.csv', 'baro.csv', 'mag.csv'])
