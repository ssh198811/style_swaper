import os

# 设置工作目录
default_work_dir = "H:\\sword3-products-head\\client\\"
# 设置资源导出列表
file_path = "稻香村.txt"
# 设置第三方导出工具路径
exe_dir = os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"


def gen_jpg_tga(file_='', work_=""):
    try:

        f = open(file_, "r", encoding='utf-8')
        # f.readline()

        for file in f:
            file=file.replace("\n","")
            file_real_path = work_ + file

            file_name = os.path.basename(file_real_path)

            # 创建style_transfer目录
            parent_path = os.path.dirname(file_real_path)
            style_transfer_path = parent_path+"/style_transfer/"


            # 创建 jpg tga
            jpg_path = style_transfer_path + file_name.replace(".dds", ".jpg")
            tga_path = style_transfer_path + file_name.replace(".dds", ".tga")
            # if (os.path.exists(jpg_path) is False) or (os.path.exists(tga_path) is False):
            if os.path.exists(style_transfer_path) is False:
                os.makedirs(style_transfer_path)
            if os.path.exists(jpg_path) is False:

                main_cmd = f"{exe_dir} {file_real_path} {jpg_path} {tga_path}"
                main_cmd = main_cmd.replace("\n", "")
                print(main_cmd)

                # do real job
                os.system(main_cmd)

    except BaseException as e:
        print(e)

#
# if __name__ == '__main__':
#     gen_jpg_tga(file_path, default_work_dir)
