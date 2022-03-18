import os
import open3d as o3d
import numpy as np
seq_dir = '/media/silence/DataT/dataset_collect2/annotated_dataset_01/'
# seq_list = os.listdir(seq_dir)
seq_list = ['backpack04_3']
for seq in seq_list:
    seq_path = os.path.join(seq_dir, seq)
    if not os.path.isdir(seq_path):
        continue
    

    pcdfile = os.path.join(seq_path, 'pcd_orii')
    save_path = os.path.join(seq_path, 'pcd')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    pcd_list = os.listdir(pcdfile)
    pcd_list.sort()
    for j in range(len(pcd_list)):
        npy = []
        pcd_path = os.path.join(pcdfile, pcd_list[j])
        point_cloud = o3d.io.read_point_cloud(pcd_path)
        pcd_array = np.asarray(point_cloud.points)
        pcd_color = np.asarray(point_cloud.colors)
        for i in range(len(pcd_array)):
            npy.append([pcd_array[i],pcd_color[i]])
        np.save(os.path.join(save_path, '%08d.npy' % (j+1)), npy)
        print(os.path.join(save_path, '%08d.npy' % (j+1)))
    print(seq, ' saved ok')
        