import os
from PIL import Image
import torch
from torchvision import transforms
from torchvision.utils import save_image
from model import VGGEncoder, Decoder
from style_swap import style_swap
import InfoNotifier
from path_util import PathUtils
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
def style_txt_main2(txt_path='',work_='',style_dir='',chosen_content_file_list=[],dir_dict={},seamless=False):
    #txt_path='',work_=''
    patch_size=1
    model_state_path = "./model_state.pth"
    if os.path.exists(txt_path) is not None:
        # content_name=pics_dir[0].replace("\\","/").split("/")[-2]
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


        #read txt
        style_name=os.path.basename(style_dir).split('.')[0]
        f=open(txt_path,"r",encoding='utf-8-sig')

        for file_path in f:
            file_path=file_path.replace("\n","").replace("\\","/")
            a=False
            #判断该图片是否在选中目录中
            for  file in chosen_content_file_list:
                if dir_dict[file] in file_path:
                    a=True
                    break

            if a is True:
                # file_path=file_path.replace("\n","")
                # file_name=os.path.basename(file_path)
                # file_path=work_+'/'+file_path
                # parent_path=os.path.dirname(file_path)
                get_path = PathUtils(work_,style_dir,file_path)
                # get_path.work_ = work_
                # get_path.style_path = style_dir
                # get_path.dds_path=file_path
                if seamless is False:
                    jpg_path=get_path.dds_to_jpg_path()
                else:
                    jpg_path=get_path.get_expanded_jpg_path()
                # jpg_path=parent_path+'/style_transfer/'+file_name.replace(".dds",".jpg")
                if os.path.exists(jpg_path) is False:
                    print(jpg_path+"is not exist,jump from process")
                    continue
                if seamless is False:
                    style_output_path=get_path.get_style_path()
                else:
                    style_output_path=get_path.get_expanded_style_path()


                style_outdir=os.path.dirname(os.path.dirname(style_output_path))
                if os.path.exists(style_outdir) is False:
                    os.makedirs(style_outdir)

                if jpg_path.endswith(".jpg") is False:
                    continue
                try:
                    ##文件名
                    # file = os.path.basename(jpg_path)
                    c_name = os.path.splitext(os.path.basename(jpg_path))[0]
                    s_name = os.path.splitext(os.path.basename(style_dir))[0]
                    if os.path.exists(style_output_path) is False:

                        # if os.path.exists(f'{style_outdir}{s_name}/' + file) is False:
                        e = VGGEncoder().to(device)
                        c = Image.open(jpg_path)
                        width_d = c.width // img_base
                        height_d = c.height // img_base
                        tar = Image.new('RGB', (c.width, c.height))


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
                                save_image(out_denorm, f'{style_outdir}/{output_name}.jpg', nrow=1)

                                img_tmp = Image.open(f'{style_outdir}/{output_name}.jpg')
                                img_tmp = img_tmp.crop((img_pad, img_pad, img_tmp.width - img_pad, img_tmp.height - img_pad))
                                tar.paste(img_tmp, (i * img_base, j * img_base, (i + 1) * img_base, (j + 1) * img_base))

                                os.unlink(f'{style_outdir}/{output_name}.jpg')
                    else:
                        print("file exists")
                        InfoNotifier.InfoNotifier.g_progress_info.append(style_output_path+'已存在，跳过')

                except RuntimeError:
                    print('Images are too large to transfer. Size under 1000 are recommended ' + file_path)
                    InfoNotifier.InfoNotifier.g_progress_info.append(f"{file_path}太大，无法迁移风格，推荐尝试1000×1000以下图片")

                try:
                    if os.path.exists(style_output_path) is False:
                         # save style transfer result
                        if os.path.exists(os.path.dirname(style_output_path)) is False:
                            os.makedirs(os.path.dirname(style_output_path))

                            # tga_img = Image.open(content_dir + file.replace('.jpg', '.tga'))
                            # ir_tmp, ig_tmp, ib_tmp, ia = tga_img.split()
                            # ir, ig, ib = tar.split()
                            # tga_img = Image.merge('RGBA', (ir, ig, ib, ia))
                        # file=file.replace("style_transfer/","")
                        # print(f'save_path:{style_outdir};file:{file}')
                        # if os.path.exists(f'{save_dir}{s_name}/{content_name}/') is False
                        tar.save(style_output_path, quality=100)
                        print(f'result saved into files {style_output_path}/')
                        InfoNotifier.InfoNotifier.g_progress_info.append(f'stylized image has saved into files: {style_output_path}')
                        InfoNotifier.InfoNotifier.style_preview_pic_dir2.append(style_output_path)
                    else:
                        print("exists")
                except BaseException as ec:
                    print(ec)
                    InfoNotifier.InfoNotifier.g_progress_info.append('error when saving stylized image')
        try:
            del e
        except:
            pass