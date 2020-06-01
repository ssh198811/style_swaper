import os
from PIL import Image
import torch
from torchvision import transforms
from torchvision.utils import save_image
from model import VGGEncoder, Decoder
from style_swap import style_swap
import InfoNotifier
img_base = 256
img_pad = 100

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

trans = transforms.Compose([transforms.ToTensor(),
                            normalize])


def denorm(tensor, device):
    std = torch.Tensor([0.229, 0.224, 0.225]).reshape(-1, 1, 1).to(device)
    mean = torch.Tensor([0.485, 0.456, 0.406]).reshape(-1, 1, 1).to(device)
    res = torch.clamp(tensor * std + mean, 0, 1)
    return res

def style_main3(pics_dir=[],style_dir='',save_dir=''):
    patch_size=1
    model_state_path = "./model_state.pth"
    if pics_dir is not None:
        content_name=pics_dir[0].replace("\\","/").split("/")[-2]
        # set device on GPU if available, else CPU
        if torch.cuda.is_available():
            device = torch.device('cuda')
            print(f'# CUDA available: {torch.cuda.get_device_name(0)}')
        else:
            device = 'cpu'

        # set model

        d = Decoder()
        d.load_state_dict(torch.load(model_state_path))
        d = d.to(device)

        s = Image.open(style_dir)
        s_tensor = trans(s).unsqueeze(0).to(device)

        for file_path in pics_dir:
            if file_path.endswith(".jpg") is False:
                continue
            try:
                e = VGGEncoder().to(device)
                c = Image.open(file_path)
                width_d = c.width // img_base
                height_d = c.height // img_base
                tar = Image.new('RGB', (c.width, c.height))
                ##文件名
                file=os.path.basename(file_path)
                c_name = os.path.splitext(os.path.basename(file_path))[0]
                s_name = os.path.splitext(os.path.basename(style_dir))[0]
                print(s_name)

                # 切分大图为小图
                for i in range(width_d):
                    for j in range(height_d):
                        c_div = c.crop((i * img_base - img_pad, j * img_base - img_pad, (i + 1) * img_base + img_pad,
                                        (j + 1) * img_base + img_pad))

                        c_tensor = trans(c_div).unsqueeze(0).to(device)

                        with torch.no_grad():
                            cf = e(c_tensor)
                            sf = e(s_tensor)
                            style_swap_res = style_swap(cf, sf, patch_size, 1)
                            del cf
                            del sf
                            out = d(style_swap_res)

                        c_denorm = denorm(c_tensor, device)
                        out_denorm = denorm(out, device)
                        res = torch.cat([c_denorm, out_denorm], dim=0)
                        res = res.to('cpu')

                        output_name = f'{c_name}_{s_name}_{i}_{j}'
                        save_image(out_denorm, f'{save_dir}/{output_name}.jpg', nrow=1)

                        img_tmp = Image.open(f'{save_dir}/{output_name}.jpg')
                        img_tmp = img_tmp.crop((img_pad, img_pad, img_tmp.width - img_pad, img_tmp.height - img_pad))
                        tar.paste(img_tmp, (i * img_base, j * img_base, (i + 1) * img_base, (j + 1) * img_base))

                        os.unlink(f'{save_dir}/{output_name}.jpg')

            except RuntimeError:
                print('Images are too large to transfer. Size under 1000 are recommended ' + file_path)

            try:
                 # save style transfer result
                if os.path.exists(f'{save_dir}{s_name}/') is False:
                    os.makedirs(f'{save_dir}{s_name}/')

                    # tga_img = Image.open(content_dir + file.replace('.jpg', '.tga'))
                    # ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                    # ir, ig, ib = tar.split()
                    # tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                # file=file.replace("style_transfer/","")
                print(f'contentname:{content_name};file:{file}')
                # if os.path.exists(f'{save_dir}{s_name}/{content_name}/') is False
                tar.save(f'{save_dir}{s_name}/' + file, quality=100)
                print(f'result saved into files {save_dir}{s_name}/' + file)
                # import  InfoNotifier
                # InfoNotifier.InfoNotifier.style_preview_pic_dir3.append(f'{save_dir}{s_name}/' + file)

            except BaseException as ec:
                print(ec)

            del e



# def main(content_dir='', content_name=None, style_dir='', output_dir=''):
#     patch_size = 3
#     model_state_path = "./model_state.pth"
#
#     # set device on GPU if available, else CPU
#     if torch.cuda.is_available():
#         device = torch.device('cuda')
#         print(f'# CUDA available: {torch.cuda.get_device_name(0)}')
#     else:
#         device = 'cpu'
#
#     # set model
#     e = VGGEncoder().to(device)
#     d = Decoder()
#     d.load_state_dict(torch.load(model_state_path))
#     d = d.to(device)
#
#     s = Image.open(style_dir)
#     s_tensor = trans(s).unsqueeze(0).to(device)
#
#     for file in os.listdir(content_dir):
#         if file.endswith(".jpg") is False:
#             continue
#
#         if content_name is not None and content_name != file:
#             continue
#
#         file_path = os.path.join(content_dir, file)
#         torch.cuda.empty_cache()
#         try:
#             c = Image.open(file_path)
#             width_d = c.width // img_base
#             height_d = c.height // img_base
#             tar = Image.new('RGB', (c.width, c.height))
#
#             c_name = os.path.splitext(os.path.basename(file))[0]
#             s_name = os.path.splitext(os.path.basename(style_dir))[0]
#
#             # 切分大图为小图
#             for i in range(width_d):
#                 for j in range(height_d):
#                     c_div = c.crop((i * img_base - img_pad, j * img_base - img_pad, (i + 1) * img_base + img_pad,
#                                     (j + 1) * img_base + img_pad))
#
#                     c_tensor = trans(c_div).unsqueeze(0).to(device)
#
#                     with torch.no_grad():
#                         cf = e(c_tensor)
#                         sf = e(s_tensor)
#                         style_swap_res = style_swap(cf, sf, patch_size, 1)
#                         del cf
#                         del sf
#                         out = d(style_swap_res)
#
#                     c_denorm = denorm(c_tensor, device)
#                     out_denorm = denorm(out, device)
#                     res = torch.cat([c_denorm, out_denorm], dim=0)
#                     res = res.to('cpu')
#
#                     output_name = f'{c_name}_{s_name}_{i}_{j}'
#                     save_image(out_denorm, f'{output_dir}/{output_name}.jpg', nrow=1)
#
#                     img_tmp = Image.open(f'{output_dir}/{output_name}.jpg')
#                     img_tmp = img_tmp.crop((img_pad, img_pad, img_tmp.width - img_pad, img_tmp.height - img_pad))
#                     tar.paste(img_tmp, (i * img_base, j * img_base, (i + 1) * img_base, (j + 1) * img_base))
#
#                     os.unlink(f'{output_dir}/{output_name}.jpg')
#
#         except RuntimeError:
#             print('Images are too large to transfer. Size under 1000 are recommended ' + file_path)
#
#         try:
#             # save style transfer result
#             if os.path.exists(f'{output_dir}{s_name}/') is False:
#                 os.makedirs(f'{output_dir}{s_name}/')
#
#             # tga_img = Image.open(content_dir + file.replace('.jpg', '.tga'))
#             # ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
#             # ir, ig, ib = tar.split()
#             # tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
#             tar.save(f'{output_dir}{s_name}/' + file, quality=100)
#             print(f'result saved into files {output_dir}/{s_name}/' + file)
#
#         except BaseException as ec:
#             print(ec)
#
#     del e


if __name__ == '__main__':

    set_content_dir = 'H:/sword3-products-head/client/data/source/maps_source/foliage/Texture/style_transfer/'

    set_content_name = 'gm_aglaiaodorata001_billboards.jpg'

    set_style_dir = 'E:/Users/shishaohua.SHISHAOHUA1/PycharmProjects/Pytorch_Style_Swap-master/style_test/8.jpeg'

    set_output_dir = set_content_dir+"style_output/"

    # 判断是否是无缝贴图
    set_b_use_expended_dir = False

    if set_b_use_expended_dir is True:
        set_content_dir += "expanded/"
        set_output_dir += "expanded/"

    assert os.path.exists(set_content_dir)
    if os.path.exists(set_output_dir) is False:
        os.makedirs(set_output_dir)

    # main(set_content_dir, set_content_name, set_style_dir, set_output_dir)
