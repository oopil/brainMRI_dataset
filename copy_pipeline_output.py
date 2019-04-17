import os
import sys
import time
import argparse
from chosun_ad_bot import *

"""parsing and configuration"""
def parse_args() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', type=int, default='0', help='the index of class from 0 to 3')
    parser.add_argument('--sub_divide_num', type=int, default='1',
                        help='the number to divide the group to run multiple pipeline in parallel way')
    parser.add_argument('--sub_index', type=int, default='0', help='the index of group inside the class')
    parser.add_argument('--hi', type=int, default='0', help='the index of group inside the class')
    # base_folder_path = '/home/sp/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0' # desktop setting
    # base_folder_path = '/home/sp/Datasets/MRI_chosun/test_sample_2/freesurfer_2_and_3' # desktop setting
    # base_folder_path = '/user/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0' # server 144 setting
    # base_folder_path = '/home/soopil/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0' # server202 account
    # base_folder_path = '/home/public/Dataset/MRI_chosun/ADAI_MRI_Result_V1_0'  # server 186 setting
    parser.add_argument('--base_folder_path', type=str, default='/home/sp/Datasets/MRI_chosun/test_sample_2/freesurfer_2_and_3')
    parser.add_argument('--file_to_copy', type=str, default=\
        'T1.nii aparc+aseg.nii aparc.DKTatlas+aseg.nii norm.nii aparc.a2009s+aseg.nii brain.nii nu.nii wm.nii aseg.auto.nii orig.nii aseg.auto_noCCseg.nii orig_nu.nii wmparc.nii aseg.nii')
    # 'T1.nii aseg.presurf.hypos.nii filled.nii rh.ribbon.nii aparc+aseg.nii aseg.presurf.nii lh.ribbon.nii ribbon.nii aparc.DKTatlas+aseg.nii brain.finalsurfs.nii norm.nii wm.asegedit.nii aparc.a2009s+aseg.nii brain.nii nu.nii wm.nii aseg.auto.nii brainmask.auto.nii orig.nii wm.seg.nii aseg.auto_noCCseg.nii brainmask.nii orig_nu.nii wmparc.nii aseg.nii ctrl_pts.nii rawavg.nii'
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
    index = args.index
    sub_index = args.sub_index
    sub_divide_num = args.sub_divide_num

    base_folder_path = args.base_folder_path
    file_to_copy_str = args.file_to_copy
    file_to_copy_list = [e for e in file_to_copy_str.split(' ') if e != '']

    print(file_to_copy_str)
    print(file_to_copy_list)
    print(base_folder_path)

    # is_remove_exist_folder = True
    is_remove_exist_folder = False
    bot = ADBrainMRI('.')
    bot.copy_directory_only(base_folder_path)

    assert False

    # need to change the result file name according to the pipeline options.
    result_file_name = 'chosun_MRI_pipeline_finish_list_' + str(index) + '_' + str(sub_index) + '_' + str(sub_divide_num - 1)
    contents = []
    if bot.is_exist(result_file_name):
        fd = open(result_file_name, 'rt')
        contents = fd.readlines()
        print(contents)
        fd.close()

    fd = open(result_file_name, 'a+t')
    class_name = ['aAD', 'ADD', 'mAD', 'NC']
    total_meta_data_list = extr_meta_data(class_name[index], base_folder_path)
    total_data_count = len(total_meta_data_list)

    pipeline_data_num = total_data_count // sub_divide_num
    if sub_index == sub_divide_num - 1:
        meta_data_list = total_meta_data_list[pipeline_data_num * sub_index:]
    elif sub_index < sub_divide_num:
        meta_data_list = total_meta_data_list[pipeline_data_num * sub_index:pipeline_data_num * (sub_index + 1)]
    else:
        print('the sub index and divide number is inappropriate')
        print(':', index, sub_index, sub_divide_num, total_data_count, pipeline_data_num)
        assert False

    batch_data_num = len(meta_data_list)
    for i, subj in enumerate(meta_data_list):
        subj_name = subj[1]
        name = subj_name + '\n'
        print('<<< Index : ', i + 1, '/', batch_data_num, ' >>>')
        if name in contents:
            print('this subj is already processed.', subj_name)
            continue

        result_folder_name = 'freesurfer'
        subj_dir_path = os.path.join(subj[0], subj[1])
        result_folder_path = os.path.join(subj_dir_path, result_folder_name)
        target_output_file_path = os.path.join(result_folder_path, 'label/rh.entorhinal_exvivo.label')

        # /home/public/Dataset/MRI_chosun/ADAI_MRI_Result_V1_0/ADD/T1sag/14051002/freesurfer/label/rh.entorhinal_exvivo.label
        # this is the path of last output file.
        # if this file exist, the pipeline is done correctly.

        if bot.is_exist(target_output_file_path):
            print('Output file of the last process is already exist.')
            print('this subj is already processed.', subj_name)
            continue

        if bot.is_exist(result_folder_path) and is_remove_exist_folder:
            rm_command = 'rm -r ' + result_folder_path
            print('freesurfer folder already exists. try to remove it')
            print(rm_command)
            os.system(rm_command)

        print('subject {} has not been processed completely.'.format(subj_name))
        chosun_MRI_copy_use_only(subj[0], subj[1], subj[2])
    # fd.writelines(subj_name+'\n')
    # assert False

    fd.close()
    fd = open(result_file_name, 'rt')
    print(fd.readlines())
    fd.close()
    del bot
    return


def chosun_MRI_copy_use_only(folder_path, subj_name, input_image) -> None:
    print('run the pipeline for chosun univ MRI data.')
    result_folder_name = 'freesurfer'
    subj_dir_path = os.path.join(folder_path, subj_name)
    result_folder_path = os.path.join(subj_dir_path, result_folder_name)
    options = ['-autorecon1', '-autorecon2-inflate1', '-autorecon2', '-autorecon3']
    is_run = [False, False, True, True]

    command = [ \
        'recon-all ' + '-i ' + input_image + ' -s ' + result_folder_name + ' -sd ' + subj_dir_path + ' ' + options[0], \
        'recon-all ' + ' -s ' + result_folder_name + ' -sd ' + subj_dir_path + ' ' + options[1], \
        'recon-all ' + ' -s ' + result_folder_name + ' -sd ' + subj_dir_path + ' ' + options[2], \
        'recon-all ' + ' -s ' + result_folder_name + ' -sd ' + subj_dir_path + ' ' + options[3]]
    export_command = 'export SUBJECT_DIR=' + folder_path

    print('\n')
    print('the pipeline contains')
    print('\n' + export_command)
    for i, run in enumerate(is_run):
        if run:
            print('-- {:30}'.format(options[i]))
            print('>> {}'.format(command[i]))

    start_time_1 = time.strftime("20%y:%m:%d %H:%M")
    if is_run[0]:
        # assert False
        os.system(export_command)
        print(command[0], '\n')
        os.system(command[0])
        start_time_2 = time.strftime("20%y:%m:%d %H:%M")

    for i in range(len(is_run) - 1):
        if is_run[i + 1]:
            print(command[i + 1], '\n')
            os.system(command[i + 1])

    end_time = time.strftime("20%y:%m:%d %H:%M")
    print('processing pipeline is done.')
    if is_run[0]:
        print('start time 1 : ', start_time_1)
    if is_run[1]:
        print('start time 2 : ', start_time_2)
    print('end time : ', end_time)

    # if succeed to run all pipeline,
    # write the name in the finished list file
    return

def test():
    test = ['a', 'b', 'c', 'd']
    fd = open('test_file', 'a+t')
    for i in test:
        fd.writelines(i + '\n')
    fd.close()
    fd = open('test_file', 'r')
    contents = fd.readlines()
    print(contents)
    fd.close()

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
