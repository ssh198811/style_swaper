from PIL import Image
import os

pad = 256


def gen_seam_tex(work_dir='', generate_test_img=False):
    for file in os.listdir(work_dir):
        if file.endswith(".tga") is True:
            img = Image.open(work_dir + file)
            width = img.width
            height = img.height

            img_crop = img.crop((pad, pad, width - pad, height - pad))
            if os.path.exists(work_dir + "seamless/") is False:
                os.makedirs(work_dir + "seamless/")
            img_crop.save(work_dir + "seamless/" + file, quality=100)

            img_test = Image.new("RGB", (img_crop.width * 3, img_crop.height * 3))
            for i in range(3):
                for j in range(3):
                    img_test.paste(img_crop, (
                        i * img_crop.width, j * img_crop.height, (i + 1) * img_crop.width, (j + 1) * img_crop.height))

            if generate_test_img is True:
                if os.path.exists(work_dir + "test/") is False:
                    os.makedirs(work_dir + "test/")
                img_test.save(work_dir + "test/" + file, quality=100)


if __name__ == '__main__':
    set_work_dir = "H:/sword3-products-head/client/data/source/maps_source/Texture/TerrainTexture/Cliff/style" \
                   "_transfer/lerp_output/"
    b_generate_test_img = False

    gen_seam_tex(set_work_dir, b_generate_test_img)
