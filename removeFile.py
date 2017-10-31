import os

root = "elevator_down"
folder_list = os.listdir(root)
for path in folder_list: 
    new_root = root + '/' + path  
    new_folder_list = os.listdir(new_root)
    for file in new_folder_list:
        if (file in ['acc.csv', 'acc_new.csv', 'b_diff.csv', 'baro.csv', 'p_new.csv','mag.csv','mag_new.csv']):
            print ("debug3")
            os.remove(new_root+'/'+file)
