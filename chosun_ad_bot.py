from class_metabot import *
# class to handle chosun univ. alzheimer's disease brain MRI data set
class ADBrainMRI(MetaBot):
    def find_all_fld_chosun_AD(self, path):
        file_list = self.get_file_list(path)
        for file_name in file_list:
            new_path = self.join_path(path, file_name)
            if self.is_dir(new_path):
                self.fld_list.append(new_path)
                self.find_all_fld_chosun_AD(new_path)

    def MRI_chosun(self, class_name) -> list:
        class_path = self.join_path(self.base_path, class_name)
        class_path = self.join_path(class_path, 'T1sag')
        subj_name_list = self.get_file_list(class_path)
        # print(subj_name_list)
        meta_list = []
        for subj in sorted(subj_name_list):
            subj_path = self.join_path(class_path, subj)
            if not self.is_dir(subj_path):
                continue
            T1_path = self.join_path(subj_path, 'T1.nii.gz')
            if not self.is_exist(T1_path):
                print('T1 image does not exists.', T1_path, subj)
                assert False
            folder_path = class_path
            subj_name = subj
            input = T1_path

            new_line = [folder_path, subj_name, input]
            meta_list.append(new_line)
        # print(new_line)
        return meta_list

    def copy_directory_only(self, base_folder_path):
        self.find_all_fld_chosun_AD(base_folder_path)
        dir_path_list = self.get_fld_list()
        # print("/".join(folder_path_split))
        # print(folder_path_split)
        # print(base_folder_path)

        mkdir_bot = MakeDirectory()
        a = self.convert_path(base_folder_path, base_folder_path, 'empty_copy')
        print(a)
        mkdir_bot.mkdir(a)
        assert False

        for dir_path in dir_path_list:
            print(base_folder_path)
            print(dir_path)
            print(self.convert_path(base_folder_path, dir_path, 'empty_copy'))
            new_dir_path = self.convert_path(base_folder_path, dir_path, 'empty_copy')
            # mkdir_bot.mkdir(new_dir_path)

    def convert_path(self, base_folder_path, path, new_dir_name):
        folder_path_split = [e for e in base_folder_path.split('/') if e != '']
        path_split = [e for e in path.split('/') if e != '']

        new_folder_path = ''
        for i, e in enumerate(folder_path_split):
            # print(i,e, path_split[i])
            assert e == path_split[i]

        folder_path_split[-1] = folder_path_split[-1] + '_' + new_dir_name
        folder_path_split = folder_path_split + path_split[i+1:]
        new_dir_path = "/" + "/".join(folder_path_split)
        return new_dir_path