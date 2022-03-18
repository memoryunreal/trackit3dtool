import os
from shutil import copy2, copyfile, copytree

dir_path = '/media/silence/DataT/dataset_collect2/hongjunminghui'
# minghuihongjun_dataset_path = '/media/silence/DataT/dataset_collect2/hongjunminghui'
dest_path = '/media/silence/DataT/dataset_collect2/newfiles'
subdir_name = os.listdir(dir_path)
subdir_colorpath = []
destdir_colorpath = []


for dirname in subdir_name:
    subdir_path = os.path.join(dir_path, dirname)
    subdir_colorpath.append(os.path.join(subdir_path, 'color'))

for color in subdir_colorpath:

    destdir_colorpath = os.path.join(dest_path, os.path.split(os.path.split(color)[0])[1])
    dest = os.path.join(destdir_colorpath, 'color')
    try:
        copytree(color,dest)
        print("%s is copied success" % dest)
    except:
        print("%s is already existed" % dest)
        continue
