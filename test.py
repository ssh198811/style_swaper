import os
import shutil

def del_spe_sir(path):
    if os.path.isdir(path):
        if 'lerp_output' in path or 'temp' in path or 'seamless_output' in path:
            shutil.rmtree(path)
        else:
            for item in os.listdir(path):
                itempath = os.path.join(path, item)
                del_spe_sir(itempath)

def del_deep_temp_dir(path):
    if os.path.isdir(path) and 'style_output' in path and 'style_transfer' in path:
        shutil.rmtree(path)
    if os.path.isdir(path) and 'dds_output' not in path and 'style_transfer' in path:
        for item in os.listdir(path):
            itemPath = os.path.join(path, item)
            if os.path.isfile(itemPath):
                os.remove(itemPath)
            else:
                del_deep_temp_dir(itemPath)
path = 'G:\稻香村605'
# del_spe_sir(path)
del_deep_temp_dir(path)