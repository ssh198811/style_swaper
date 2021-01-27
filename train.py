import warnings
warnings.simplefilter("ignore", UserWarning)
import os
import argparse
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision.utils import save_image
from dataset import PreprocessDataset, denorm
from model import VGGEncoder, Decoder
from style_swap import style_swap


def TVloss(img, tv_weight):
    """
    Compute total variation loss.
    Inputs:
    - img: PyTorch Variable of shape (1, 3, H, W) holding an input image.
    - tv_weight: Scalar giving the weight w_t to use for the TV loss.
    Returns:
    - loss: PyTorch Variable holding a scalar giving the total variation loss
      for img weighted by tv_weight.
    """
    w_variance = torch.sum(torch.pow(img[:, :, :, :-1] - img[:, :, :, 1:], 2))
    h_variance = torch.sum(torch.pow(img[:, :, :-1, :] - img[:, :, 1:, :], 2))
    loss = tv_weight * (h_variance + w_variance)
    return loss


def main():
    parser = argparse.ArgumentParser(description='Style Swap by Pytorch')
    parser.add_argument('--batch_size', '-b', type=int, default=12,
                        help='Number of images in each mini-batch')
    parser.add_argument('--epoch', '-e', type=int, default=10000,
                        help='Number of sweeps over the dataset to train')
    parser.add_argument('--patch_size', '-p', type=int, default=3,
                        help='Size of extracted patches from style features')
    parser.add_argument('--gpu', '-g', type=int, default=0,
                        help='GPU ID(nagative value indicate CPU)')
    parser.add_argument('--learning_rate', '-lr', type=int, default=1e-4,
                        help='learning rate for Adam')
    parser.add_argument('--tv_weight', type=int, default=1e-6,
                        help='weight for total variation loss')
    parser.add_argument('--snapshot_interval', type=int, default=1,
                        help='Interval of snapshot to generate image')
    parser.add_argument('--train_content_dir', type=str, default='./content/',
                        help='content images directory for train')
    parser.add_argument('--train_style_dir', type=str, default='./style/',
                        help='style images directory for train')
    parser.add_argument('--test_content_dir', type=str, default='./content/',
                        help='content images directory for test')
    parser.add_argument('--test_style_dir', type=str, default='./style/',
                        help='style images directory for test')
    parser.add_argument('--save_dir', type=str, default='result',
                        help='save directory for result and loss')

    args = parser.parse_args()

    # create directory to save
    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)

    loss_dir = f'{args.save_dir}/loss'
    model_state_dir = f'{args.save_dir}/model_state'
    image_dir = f'{args.save_dir}/image'

    if not os.path.exists(loss_dir):
        os.mkdir(loss_dir)
        os.mkdir(model_state_dir)
        os.mkdir(image_dir)

    # set device on GPU if available, else CPU
    if torch.cuda.is_available() and args.gpu >= 0:
        device = torch.device(f'cuda:{args.gpu}')
        print(f'# CUDA available: {torch.cuda.get_device_name(0)}')
    else:
        device = 'cpu'

    print(f'# Minibatch-size: {args.batch_size}')
    print(f'# epoch: {args.epoch}')
    print('')

    # prepare dataset and dataLoader
    train_dataset = PreprocessDataset(args.train_content_dir, args.train_style_dir)
    test_dataset = PreprocessDataset(args.test_content_dir, args.test_style_dir)
    iters = len(train_dataset)
    print(f'Length of train image pairs: {iters}')

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=True)
    test_iter = iter(test_loader)

    # set model and optimizer
    encoder = VGGEncoder().to(device)
    decoder = Decoder()
    # decoder.load_state_dict(torch.load(model_state_dir+'/model_state.pth'))
    decoder.to(device)
    # optimizer = Adam(decoder.parameters(), lr=args.learning_rate)
    optimizer = torch.optim.SGD(decoder.parameters(), lr=args.learning_rate, momentum=0.9)

    print(decoder)

    # start training
    criterion = nn.MSELoss()
    loss_list = []

    min_loss = 10000

    for e in range(1, args.epoch + 1):
        print(f'Start {e} epoch')
        for i, (content, style) in tqdm(enumerate(train_loader, 1)):
            content = content.to(device)
            style = style.to(device)

            content_feature = encoder(content)
            style_feature = encoder(style)

            style_swap_res = []
            for b in range(content_feature.shape[0]):
                c = content_feature[b].unsqueeze(0)
                s = style_feature[b].unsqueeze(0)
                cs = style_swap(c, s, args.patch_size, 1)
                style_swap_res.append(cs)
            style_swap_res = torch.cat(style_swap_res, 0)

            out_style_swap = decoder(style_swap_res)
            out_content = decoder(content_feature)
            out_style = decoder(style_feature)

            out_style_swap_latent = encoder(out_style_swap)
            out_content_latent = encoder(out_content)
            out_style_latent = encoder(out_style)


            image_reconstruction_loss = criterion(content, out_content) + criterion(style, out_style)

            feature_reconstruction_loss = criterion(style_feature, out_style_latent) + \
                                          criterion(content_feature, out_content_latent) + \
                                          criterion(style_swap_res, out_style_swap_latent)
            tv_loss = TVloss(out_style_swap, args.tv_weight) + TVloss(out_content, args.tv_weight) \
                + TVloss(out_style, args.tv_weight)

            loss = image_reconstruction_loss + feature_reconstruction_loss + tv_loss

            # feature_reconstruction_loss = criterion(style_swap_res, out_style_swap_latent)
            # tv_loss = TVloss(out_style_swap, args.tv_weight)
            # loss = feature_reconstruction_loss + tv_loss

            loss_list.append(loss.item())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print(f'[{e}/total {args.epoch} epoch],[{i} /'
                  f'total {round(iters/args.batch_size)} iteration]: {loss.item()} '
                  f'feature_reconstruction_loss:{feature_reconstruction_loss} '
                  f'tv_loss:{tv_loss}')

            if i == args.snapshot_interval:
                content, style = next(test_iter)
                content = content.to(device)
                style = style.to(device)
                with torch.no_grad():
                    content_feature = encoder(content)
                    style_feature = encoder(style)
                    style_swap_res = []
                    print(content_feature.shape)
                    for b in range(content_feature.shape[0]):
                        c = content_feature[b].unsqueeze(0)
                        s = style_feature[b].unsqueeze(0)
                        cs = style_swap(c, s, args.patch_size, 1)
                        style_swap_res.append(cs)
                    style_swap_res = torch.cat(style_swap_res, 0)
                    out_style_swap = decoder(style_swap_res)
                    out_content = decoder(content_feature)
                    out_style = decoder(style_feature)

                content = denorm(content, device)
                style = denorm(style, device)
                out_style_swap = denorm(out_style_swap, device)
                # out_gray = denorm(out_gray, device)
                out_content = denorm(out_content, device)
                out_style = denorm(out_style, device)
                res = torch.cat([content, style, out_content, out_style, out_style_swap], dim=0)
                res = res.to('cpu')
                save_image(res, f'{image_dir}/{e}_epoch_{i}_iteration.png', nrow=content_feature.shape[0])
        loss_total = 0.0
        loss_avg = 0.0
        for i in loss_list:
            loss_total += i
        loss_avg = loss_total / round(iters/args.batch_size)
        loss_list = []
        print(f"current epoch {e} ... min loss is {min_loss} avg loss is {loss_avg}")
        if min_loss > loss_avg:
            print(f"saving epoch {e} ... avg loss is {loss_avg}")
            min_loss = loss_avg
            torch.save(decoder.state_dict(), f'{model_state_dir}/model_state.pth')

    plt.plot(range(len(loss_list)), loss_list)
    plt.xlabel('iteration')
    plt.ylabel('loss')
    plt.title('train loss')
    plt.savefig(f'{loss_dir}/train_loss.png')
    with open(f'{loss_dir}/loss_log.txt', 'w') as f:
        for l in loss_list:
            f.write(f'{l}\n')
    print(f'Loss saved in {loss_dir}')


if __name__ == '__main__':
    main()
