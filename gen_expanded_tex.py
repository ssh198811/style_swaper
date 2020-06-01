from PIL import Image
import os

# 为生成四向无缝贴图 使用该方法操作 并非必要处理手段
# 生成结果会存在当前目录的seamless文件加下
pad = 256


def gen_expanded_tex(work_='', sub_=''):
    work_path = work_ + sub_+"style_transfer/"
    for file_jpg in os.listdir(work_path):
        # 如果存在jpg图片，则说明该图片需要被处理
        if file_jpg.endswith(".jpg") is True:

            split_text = os.path.splitext(file_jpg)
            file_tga = split_text[0]+'.tga'

            img_jpg = Image.open(work_path + file_jpg)
            img_tga = Image.open(work_path + file_tga)

            width = img_jpg.width
            height = img_jpg.height
            assert width == img_tga.width and height == img_tga.height

            img_jpg_pad = Image.new("RGB", (width*3, height*3))
            img_tga_pad = Image.new("RGBA", (width * 3, height * 3))

            for i  in range(3):
                for j in range(3):
                    img_jpg_pad.paste(img_jpg, (i*width, j*height, (i+1)*width, (j+1)*height))
                    img_tga_pad.paste(img_tga, (i*width, j*height, (i+1)*width, (j+1)*height))

            if os.path.exists(work_path+"expanded/") is False:
                os.makedirs(work_path+"expanded/")

            img_jpg_crop = img_jpg_pad.crop((width-pad, height-pad, 2*width+pad, 2*height+pad))
            img_jpg_crop.save(work_path + "expanded/" + file_jpg, quality=100)
            print("saveing " + work_path + "expanded/" + file_jpg)

            img_tga_crop = img_tga_pad.crop((width-pad, height-pad, 2*width+pad, 2*height+pad))
            img_tga_crop.save(work_path + "expanded/" + file_tga, quality=100)
            print("saveing " + work_path + "expanded/" + file_tga)


if __name__ == '__main__':
    # 默认操作资源路径
    default_work_path = "H:/sword3-products-head/client/data/source/maps_source/Texture/"
    # 操作子目录
    sub_dir = "TerrainTexture/Cliff/"
    gen_expanded_tex(default_work_path, sub_dir)




