from genericpath import exists
import os
import pexpect
import argparse

# host = ''
# user = ''
# password = '.'
scp_cmd = 'scp -r {}@{}:{} {}'
# dir_path = ''
# target_path = ''
files = []


def login(user, host, password, filepath, target_path):
    scp_handle = pexpect.spawn(scp_cmd.format(user, host, filepath, target_path))
    scp_handle.expect('password:')
    scp_handle.sendline(password)
    scp_handle.read()
    print('发送完毕：{}/{}'.format(target_path,os.path.basename(filepath)))




        


if __name__ == '__main__':
    # jparse = argparse.ArgumentParser(description='scp scrapy')
    # parse.add_argument('-i', '--ip', required=True, type=str, help='scp的ip地址')
    # parse.add_argument('-u', '--user', required=True, type=str, help='scp用户')
    # parse.add_argument('-p', '--password', required=True, type=str, help='scp的密码')
    # parse.add_argument('-d', '--dir', required=True, type=str, help='需要传输的目录')
    # parse.add_argument('-t', '--target', required=True, type=str, help='传送到的目录')
    # args = parse.parse_args()
    
    
    # login(file, args.user, args.ip, args.target, args.password)
    server_path = '/data1/yjy/rgbd_benchmark/alldata'
    sequence_list = ['cup04-indoor']
    frame_list = [
['0.0_high_00000292.jpg',
'0.0_high_00002096_loss_CSRKCF.jpg',
'0.34835038188317563_high_00000192.jpg',
'0.3807566385381053_high_00000948.jpg',
'0.39585131635735865_high_00001621_loss_CSRKCF.jpg',
'0.3419256424840995_high_00000356.jpg',

'0.5345650134136832_medium_00001005.jpg',
'0.5356090649682541_medium_00001156_loss_CSRKCF.jpg',
'0.5438015124479565_medium_00000947.jpg',
'0.5449718509031725_medium_00000855.jpg',
'0.7312554203568894_medium_00000472.jpg',
'0.743989452972314_medium_00001358_loss_CSRKCF.jpg',
'1.0082329077675696_low_00001185_loss_CSRKCF.jpg',
'1.0356198374089916_low_00001958_loss_CA3DMS_loss_CSRKCF.jpg',
'1.0831489675516224_low_00000559.jpg',
'1.1813543997201708_low_00000568.jpg',
'1.2369884742901103_low_00001931_loss_CA3DMS_loss_CSRKCF.jpg',
'1.5634619417777869_low_00000759.jpg'],
    ]
    savepath = '/Users/lizhe/Data/TMM2022/plot/depthQ/origindata'
    for i, seq in enumerate(sequence_list):
        saveseq = os.path.join(savepath, seq)
        savecolor = os.path.join(saveseq, 'color')
        savedepth = os.path.join(saveseq, 'depth')
        if not os.path.exists(savecolor) or not os.path.exists(savedepth):
            os.makedirs(savecolor)
            os.makedirs(savedepth)
        
        frame = frame_list[i]
        seqpath = os.path.join(server_path, seq)
        for id, frameid in enumerate(frame):

            frameid = frameid.split("_")[2]
            frameid = frameid.split(".")[0]
            frameid = int(frameid)
            
            colorfile = os.path.join(seqpath, 'color', '{:08d}.jpg'.format(frameid))
            depthfile = os.path.join(seqpath, 'depth', '{:08d}.png'.format(frameid))
        
            try:
                login('yangjinyu','10.20.4.112', 'yjy1029', colorfile, savecolor)
            except:
                colorfile = os.path.join(seqpath, 'color', '{:08d}.png'.format(frameid))
                login('yangjinyu','10.20.4.112', 'yjy1029', colorfile, savecolor)
        
            login('yangjinyu','10.20.4.112', 'yjy1029', depthfile, savedepth)
    print('end')
