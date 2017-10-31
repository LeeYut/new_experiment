# -*- coding: utf-8 -*- 
import os
folder_pre = 'same_floor'
folder_list = os.listdir(folder_pre)
#创建 baro acc mag的folder,注意这一步一定要在folder_list之后
os.mkdir(folder_pre + '/baro')
os.mkdir(folder_pre + '/acc')
os.mkdir(folder_pre + '/mag')

for index, i in enumerate(folder_list):
    folder = folder_pre + '/' + i
	
    dest_dir_baro = folder_pre + '/baro'
    dest_dir_acc = folder_pre + '/acc'
    dest_dir_mag = folder_pre + '/mag'

    current_dir_baro = folder + '/p_new.csv'
    current_dir_acc = folder + '/acc_new.csv'
    current_dir_mag = folder + '/mag_new.csv'

    os.rename(current_dir_baro,dest_dir_baro+'/'+'b_diff'+str(index)+'.csv')
    os.rename(current_dir_acc,dest_dir_acc+'/'+'acc'+str(index)+'.csv')
    os.rename(current_dir_mag,dest_dir_mag+'/'+'mag'+str(index)+'.csv')
