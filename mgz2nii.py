import os
import sys
import argparse

"""parsing and configuration"""
def parse_args()->argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mgz_folder_path', type=str, default='no path', help='the path of folder to convert to nifti files')
    return parser.parse_args()

def convert_all(folder_path):
	old_path = folder_path
	print(old_path)
	file_list = os.listdir(old_path)
	print(file_list)
	# assert False

	nii_dir_name = 'nifti'
	nii_dir_path = os.path.join(old_path, nii_dir_name)
	if nii_dir_name not in file_list:
		os.mkdir(nii_dir_path)
	for file_name in file_list:
		if file_name[-3:] != 'mgz':
			print(file_name, 'is not mgz format. : ', file_name[-4:] )
			continue
		'''
			don't convert useless and too big mgz files like ctrl_pts
		'''
		if file_name[:-4] == 'ctrl_pts':
			continue
		new_file_name = file_name[:-4] + '.nii'
		new_file_path = os.path.join(nii_dir_path, new_file_name)
		old_file_path = os.path.join(old_path, file_name)
		print(new_file_name)
		command = 'mri_convert '+ old_file_path + ' ' + new_file_path
		print(command)
		os.system(command)

def main()->None:
    args = parse_args()
    folder_path = args.mgz_folder_path
    convert_all(folder_path)
    return

'''
old_path = '.'
file_list = os.listdir(old_path)
print(file_list)
#assert False
nii_dir_name = 'nifti'
nii_dir_path = os.path.join(old_path, nii_dir_name)
if nii_dir_name not in file_list:
	os.mkdir(nii_dir_path)
for file_name in file_list:
	if file_name[-4] != '.':
		print(file_name, 'is not an nifti format')
		continue
	new_file_name = file_name[:-4] + '.nii'
	new_file_path = os.path.join(nii_dir_path, new_file_name)
	old_file_path = os.path.join(old_path, file_name)
	print(new_file_name)
	command = 'mri_convert '+ old_file_path + ' ' + new_file_path
	print(command)
	os.system(command)
'''
