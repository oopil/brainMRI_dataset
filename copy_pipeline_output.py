import os
import sys
import time
import argparse
from chosun_ad_bot import *
"""parsing and configuration"""
def parse_args() -> argparse:
    parser = argparse.ArgumentParser()
    # base_folder_path = '/home/sp/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0' # desktop setting
    # base_folder_path = '/home/sp/Datasets/MRI_chosun/test_sample_2/freesurfer_2_and_3' # desktop setting
    # base_folder_path = '/user/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0' # server 144 setting
    # base_folder_path = '/home/soopil/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0' # server202 account
    # base_folder_path = '/home/public/Dataset/MRI_chosun/ADAI_MRI_Result_V1_0'  # server 186 setting
    parser.add_argument('--base_folder_path', type=str, default='/home/public/Dataset/MRI_chosun/ADAI_MRI_Result_V1_0')
    parser.add_argument('--file_to_copy', type=str, default=\
        'brainmask.auto.nii T1.nii aparc+aseg.nii aparc.DKTatlas+aseg.nii '+\
        'norm.nii aparc.a2009s+aseg.nii brain.nii nu.nii wm.nii aseg.auto.nii '+\
        'orig.nii aseg.auto_noCCseg.nii orig_nu.nii wmparc.nii aseg.nii')
    # 'T1.nii aseg.presurf.hypos.nii filled.nii rh.ribbon.nii
    # aparc+aseg.nii aseg.presurf.nii lh.ribbon.nii ribbon.nii
    # aparc.DKTatlas+aseg.nii brain.finalsurfs.nii norm.nii
    # wm.asegedit.nii aparc.a2009s+aseg.nii brain.nii nu.nii wm.nii
    # aseg.auto.nii brainmask.auto.nii orig.nii wm.seg.nii
    # aseg.auto_noCCseg.nii brainmask.nii orig_nu.nii wmparc.nii
    # aseg.nii ctrl_pts.nii rawavg.nii'
    print(parser.parse_args())
    return parser.parse_args()

def extr_meta_data(class_name, folder_path) -> list:
    print('start to extract meta data from dataset folder')
    base_folder_path = folder_path
    bot = ADBrainMRI(base_folder_path)
    meta_list = bot.MRI_chosun(class_name)
    print(class_name, len(meta_list), meta_list)
    del bot
    return meta_list

def chosun_MRI_copy_use_only_pipeline(args) -> None:
    '''
    1. copy(make) the directory
    2. copy the only files i need
    :param args:
    :return:
    '''
    base_folder_path = args.base_folder_path
    file_to_copy_str = args.file_to_copy
    file_to_copy_list = [e for e in file_to_copy_str.split(' ') if e != '']

    print(file_to_copy_str)
    print(file_to_copy_list)
    print(base_folder_path)

    # is_remove_exist_folder = True
    is_remove_exist_folder = False
    bot = ADBrainMRI('.')
    copy_dir_path = bot.copy_directory_only(base_folder_path)

    # assert False
    class_name = ['aAD', 'ADD', 'mAD', 'NC']
    total_meta_data_list = extr_meta_data(class_name[0], base_folder_path)
    total_data_count = len(total_meta_data_list)
    # test_dir_path = ['/home/sp/Datasets/MRI_chosun/test_sample_2/freesurfer_2_and_3/',\
    #                  '14062105',''
    #                  '/home/sp/Datasets/MRI_chosun/test_sample_2/freesurfer_2_and_3/14062105/T1.nii.gz'\
    #                  ]
    # test_data_count = 1
    # bot.copy_only_useful_file(copy_dir_path, [test_dir_path], file_to_copy_list)
    bot.copy_only_useful_file(copy_dir_path, total_meta_data_list, file_to_copy_list)

def print_list(l:list)->None:
    for line in l:
        print(line)

def main() -> None:
    # test()
    args = parse_args()
    # extr_meta_data('aAD')
    chosun_MRI_copy_use_only_pipeline(args)
    return


if __name__ == '__main__':
    main()
