import os
from path_util import PathUtils
import InfoNotifier

# 设置工作目录
default_work_dir = "H:\\sword3-products-head\\client\\"
# 设置资源导出列表
file_path = "稻香村.txt"
# 设置第三方导出工具路径
exe_dir = os.getcwd() + "\\dds_to_jpg/dds_to_jpg.exe"

def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)

    return round(fsize, 2)

def gen_jpg_tga(file_='', work_="", dds_list=None):
    try:
        if dds_list is None:
            dds_list = []
        # f = open(file_, "r", encoding='utf-8-sig')
        # f.readline()
        for file in dds_list:
            file = file.replace("\n", "")

            low_file = file.lower()
            if low_file.find('_mre') > -1 or low_file.find('_nor') > -1:
                continue
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

                main_cmd = f"{exe_dir} \"{file_real_path}\" \"{jpg_path}\" \"{tga_path}\""
                main_cmd = main_cmd.replace("\n", "")
                print(main_cmd)
                # do real job
                os.system(main_cmd)
            else:
                print(jpg_path + ' 已存在，跳过')
    except BaseException as e:
        print(e)


rootdir = "E:\\client\\client\\data\\source\\maps_source\\data\style_transfer\\final_output\\583_\\Texture\\地表test"
outdir = "E:\\client\\client\\data\\source\\maps_source\\data\style_transfer\\final_output\\583_\\Texture\\地表test"
exe = "E:/Users/shishaohua.SHISHAOHUA1/PycharmProjects/style_swapper_new/dds_to_jpg/dds_to_jpg.exe"

def gen(input_dir):
    fileNames = os.listdir(input_dir)  # 获取当前路径下的文件名，返回List
    for file in fileNames:
        newDir = input_dir + '/' + file # 将文件命加入到当前文件路径后面
        if os.path.isfile(newDir):  # 如果是文件
            if newDir.find('.dds') != -1:

                low_dir = newDir.lower()
                if low_dir.find('_mre')!= -1 or low_dir.find('_nor')!= -1:
                    continue

                img_size = get_FileSize(newDir)
                # if img_size > 2.0 or img_size < 0.5:
                # if img_size < 0.5:
                #     continue

                dds_path = newDir
                out_path = os.path.join(outdir, file)

                jpg_path = out_path.replace('.dds', '.jpg')
                tga_path = out_path.replace('.dds', '.tga')

                if os.path.exists(jpg_path):
                    continue

                main_cmd = f"{exe} {dds_path} {jpg_path} {tga_path}"
                main_cmd = main_cmd.replace("\n", "")
                print(main_cmd)
                # do real job
                os.system(main_cmd)
        else:
            gen(newDir)                #如果不是文件，递归这个文件夹的路径
if __name__ == '__main__':
    gen(rootdir)
