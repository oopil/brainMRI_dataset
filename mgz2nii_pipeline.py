import os
import sys
import time
import argparse
from class_metabot import *
from mgz2nii import *

def parse_args()->argparse:
	parser = argparse.ArgumentParser()
	parser.add_argument('--index', type=int, default='0', help='the index of class from 0 to 3')
	return parser.parse_args()

def extr_meta_data(class_name)->list:
	print('start to extract meta data from dataset folder')
	# base_folder_path = '/home/sp/Datasets/MRI_chosun/ADAI_MRI_Result_V1_0'
	# base_folder_path = '/home/sp/Datasets/MRI_chosun/test_sample_2'
	base_folder_path = '/home/public/Dataset/MRI_chosun/ADAI_MRI_Result_V1_0'  # server 186 setting

	bot = MetaBot(base_folder_path)
	meta_list = bot.MRI_chosun(class_name)
	print(class_name, len(meta_list), meta_list)
	del bot
	return meta_list

def chosun_MRI_mgz2nii_pipeline(index)->None:
	is_convert = True
	is_remove_exist_folder = True

	bot = MetaBot('.')
	result_file_name = 'chosun_MRI_pipeline_mgz2nii_list_' + str(index)
	contents = []
	if bot.is_exist(result_file_name):
		file = open(result_file_name, 'rt')
		contents = file.readlines()
		print(contents)
		file.close()

	file = open(result_file_name, 'a+t')
	class_name = ['aAD', 'ADD', 'mAD', 'NC']
	meta_data_list = extr_meta_data(class_name[index])
	total_num = len(meta_data_list)
	print(meta_data_list)
	# assert False
	for i, subj in enumerate(meta_data_list):
		subj_name = subj[1]
		name = subj_name + '\n'
		print('<<< Index : ', i+1, '/', total_num ,' >>>')
		if name in contents:
			print('this subj is already processed.', subj_name)
			continue

		result_folder_name = 'nifti'
		subj_dir_path = os.path.join(subj[0], subj[1])
		target_folder = 'freesurfer/mri'
		target_path = os.path.join(subj_dir_path, target_folder)
		result_folder_path = os.path.join(subj_dir_path, result_folder_name)

		if bot.is_exist(result_folder_path) and is_remove_exist_folder:
			rm_command = 'rm -r ' + result_folder_path
			print('nifti folder already exists. try to remove it')
			print(rm_command)
			os.system(rm_command)

		# command = 'python mgz2nii.py --mgz_folder_path ' + target_path
		# print(command)
		# assert False
		# os.system(command)

		if is_convert:
			convert_all(target_path)
		file.writelines(subj_name+'\n')

	file.close()
	file = open(result_file_name, 'rt')
	print(file.readlines())
	file.close()
	del bot
	return

if __name__ == '__main__':
	args = parse_args()
	index = args.index
	chosun_MRI_mgz2nii_pipeline(index)
