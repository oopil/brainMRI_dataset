import os
import sys

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
