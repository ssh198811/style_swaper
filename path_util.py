import os


class PathUtils:
    def __init__(self, _work='', _style_path='', dds_path='', txt_file_=''):
        # self.ui = ui.Ui_MainWindow()
        self.work_ = _work.replace("\n", "").replace("\\", "/")
        self.style_path = _style_path.replace("\n", "").replace("\\", "/")
        self.dds_path = dds_path.replace("\n", "").replace("\\", "/")
        self.file_name_jpg = os.path.basename(self.dds_path.replace('.dds', '.jpg'))
        self.file_name_tga = os.path.basename(self.dds_path.replace('.dds', '.tga'))
        self.work_output = self.work_ + '/data/style_transfer'
        self.txt_name = os.path.basename(txt_file_).split('.')[0]

    # dds原图真实路径
    def real_dds_path(self):
        return f"{self.work_}/{self.dds_path}"

    # 原图转 jpg 保存地址
    def dds_to_jpg_path(self):
        return self.work_output + '/' + self.dds_path.replace('.dds', '.jpg')

    # 原图转 tga 保存地址
    def dds_to_tga_path(self):
        return self.work_output + '/'+self.dds_path.replace('.dds', '.tga')

    def get_parent_name(self):
        return os.path.dirname(self.dds_path.replace("\n", ""))

    def get_style_name(self):
        return os.path.basename(self.style_path).split('.')[0]

    # temp预览图保存地址  这里应该是存output/temp？
    def get_temp_preview_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/temp/{self.get_style_name()}/{self.file_name_jpg}"

    # 风格图保存路径
    def get_style_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/style_output/{self.get_style_name()}/{self.file_name_jpg}"

    # lerp图
    def get_jpg_lerp_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/lerp_output/{self.get_style_name()}/{self.file_name_jpg}"

    def get_tga_lerp_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/lerp_output/{self.get_style_name()}/{self.file_name_tga}"

    # dds图
    def get_dds_output_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/dds_output/{self.get_style_name()}/"
    # dds图-txt
    def get_dds_output_path_txt(self):
        return f"{self.work_output}/final_output/{self.txt_name}/{self.get_style_name()}/{self.get_parent_name()}/"

    # expanded jpg,tga
    def get_expanded_jpg_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/{self.file_name_jpg}"

    # expanded jpg,tga
    def get_expanded_tga_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/{self.file_name_tga}"

    # expanded-style
    def get_expanded_style_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/style_output/{self.get_style_name()}/" \
               f"{self.file_name_jpg}"

    # expanded_lerp
    def get_expanded_lerp_path_jpg(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/lerp_output/{self.get_style_name()}/" \
               f"{self.file_name_jpg}"

    def get_expanded_lerp_path_tga(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/lerp_output/{self.get_style_name()}/" \
               f"{self.file_name_tga}"

    # seamless
    def get_seamless_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/seamless_output/{self.get_style_name()}/" \
               f"{self.file_name_tga}"

    # expanded-dds
    def get_seamless_dds_path(self):
        return f"{self.work_output}/{self.get_parent_name()}/expanded/dds_output/{self.get_style_name()}/"

# get temp files' path from jpg path
class PathTemp:
    def __init__(self, jpg_path_='', style_path_=''):
        self.jpg_path = jpg_path_
        self.style_path = style_path_
        self.s_name = os.path.basename(self.style_path).split('.')[0]
    def get_temp_dir_path(self):
        # temp文件夹
        return os.path.dirname(self.jpg_path) + '/temp/'
    def get_temp_after_jpg_path(self):
        return os.path.dirname(self.jpg_path) + '/temp/' + self.s_name + '/' + os.path.basename(
                        self.jpg_path)
    def get_temp_lerp_path(self):
        return os.path.dirname(self.jpg_path) + '/temp/lerp.jpg'




if __name__ == '__main__':
    a = PathUtils(_work='H:/sword3-products-head/client',
                  _style_path=
                  'E:/Users/shishaohua.SHISHAOHUA1/PycharmProjects/style_swaper/style_swaper/style_test/1.jpg',
                  dds_path='data/source/maps_source/texture/wj_gb路标003_01h.dds', txt_file_='G:/稻香村.txt')


    print(a.real_dds_path())
    print(a.dds_to_jpg_path())
    print(a.dds_to_tga_path())
    print(a.get_parent_name())
    print(a.get_style_name())
    print(a.get_temp_preview_path())
    print(a.get_style_path())
    print(a.get_jpg_lerp_path())
    print(a.get_tga_lerp_path())
    print(a.get_dds_output_path())
    print(a.get_dds_output_path_txt())
    print(a.get_expanded_jpg_path())
    print(a.get_expanded_tga_path())
    print(a.get_expanded_style_path())
    print(a.get_expanded_lerp_path_jpg())
    print(a.get_expanded_lerp_path_tga())
    print(a.get_seamless_path())
    print(a.get_seamless_dds_path())

