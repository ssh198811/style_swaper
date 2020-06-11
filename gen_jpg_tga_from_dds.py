import os
from path_util import  PathUtils
import InfoNotifier

# 设置工作目录
default_work_dir = "H:\\sword3-products-head\\client\\"
# 设置资源导出列表
file_path = "稻香村.txt"
# 设置第三方导出工具路径
exe_dir = os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"


def gen_jpg_tga(file_='', work_="", dds_list=[]):
    try:

        # f = open(file_, "r", encoding='utf-8-sig')
        # f.readline()

        for file in dds_list:
            file = file.replace("\n", "")
            # 实例化
            # file = file.replace("\n", "")
            a = PathUtils(_work=work_, dds_path=file)
            file_real_path = a.real_dds_path()
            # file_real_path = work_ + file
            if os.path.exists(file_real_path) is False:
                InfoNotifier.InfoNotifier.g_progress_info.append(f"{file_real_path} 不存在")
                continue
            jpg_path, tga_path = a.dds_to_jpg_path(), a.dds_to_tga_path()
            if os.path.exists(os.path.dirname(jpg_path)) is False:
                os.makedirs(os.path.dirname(jpg_path))
            if os.path.exists(jpg_path) is False:

                main_cmd = f"{exe_dir} {file_real_path} {jpg_path} {tga_path}"
                main_cmd = main_cmd.replace("\n", "")
                print(main_cmd)
                # do real job
                os.system(main_cmd)
            else:
                print(jpg_path+' 已存在，跳过')
    except BaseException as e:
        print(e)

#
# if __name__ == '__main__':
#     gen_jpg_tga(file_path, default_work_dir)
