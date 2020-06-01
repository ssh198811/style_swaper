# j3_style_swap

Unofficial Pytorch(1.0+) implementation of paper [Fast Patch-based Style Transfer of Arbitrary Style](https://arxiv.org/abs/1612.04337).

Original torch implementation from the author can be found [here](https://github.com/rtqichen/style-swap).

This repository provides a pre-trained model for you to generate your own image given content image and style image. Also, you can download the training dataset or prepare your own dataset to train the model from scratch.

If you have any question, please feel free to contact me. (Language in English/Japanese/Chinese will be ok!)

主要目的不是进行训练，而是直接使用结果

使用步骤：
1. 要从dds贴图生成jpg和tga格式的素材，使用的是gen_jpg_tga_from_dds.py, 生成后的资源会存在输入资源/style_transfer/目录下
    这个目录也会成为之后操作的base目录
2. 因为贴图有所谓无缝贴图的需求，所以需要根据实际用途来决定之后操作
3. 如果是无缝贴图 要使用gen_expanded_tex.py 为其生成一个扩展后的贴图，存在base/expanded/目录下
4. 如果是普通贴图，则不需要expanded操作
5. 生成风格图片，使用gen_style_tex.py操作，生成的图片存在base/style_output/{风格名}目录下，如果是expanded贴图会存在base/style_output/
    expanded/{风格名}/下， 同时根据风格名，建立各自的目录
6. 用gen_lerp_tex产生原始图和风格图的插值图像
7. 需要调用texconv.exe 将lerp后的tga转成dds图片作为最终的输出

## Notice
I propose a structure-emphasized multimodal style transfer(SEMST), feel free to use it [here](https://github.com/irasin/Structure-emphasized-Multimodal-Style-Transfer).


------

## Requirements

- Python 3.7
- PyTorch 1.0+
- TorchVision
- Pillow

Anaconda environment recommended here!

- **GPU environment** (For the calculation of style-swap)



## Usage

------

## test

1. Clone this repository 

   ```bash
   git clone https://github.com/irasin/Pytorch_Style_Swap
   cd Pytorch_Style_Swap
   ```

2. Prepare your content image and style image. I provide some in the `content` and `style` and you can try to use them easily. Notice that they may be too large to tranfer because the `style_swap.py` really consume a lot of gpu memory, So I'm not sure all the image provided can be transferred.

3. Generate the output image. A transferred output image and a content_output_pair image and a NST_demo_like image will be generated.

   ```python
   python test -c content_image_path -s style_image_path
   ```

   ```
   usage: test.py [-h] 
                  [--content CONTENT] 
                  [--style STYLE]
                  [--output_name OUTPUT_NAME] 
                  [--patch_size PATCH_SIZE]
                  [--gpu GPU] 
                  [--model_state_path MODEL_STATE_PATH]
   
   ```

   If output_name is not given, it will use the combination of content image name and style image name.

------

## train

1. Download [COCO](http://cocodataset.org/#download) (as content dataset)and [Wikiart](https://www.kaggle.com/c/painter-by-numbers) (as style dataset) and unzip them, rename them as `content` and `style`  respectively (recommended).

2. Modify the argument in the` train.py` such as the path of directory, epoch, learning_rate or you can add your own training code.

3. Train the model using gpu.

4. ```python
   python train.py
   ```

   ```
   usage: train.py [-h] 
                   [--batch_size BATCH_SIZE] 
                   [--epoch EPOCH]
                   [--patch_size PATCH_SIZE] 
                   [--gpu GPU]
                   [--learning_rate LEARNING_RATE] 
                   [--tv_weight TV_WEIGHT]
                   [--snapshot_interval SNAPSHOT_INTERVAL]
                   [--train_content_dir TRAIN_CONTENT_DIR]
                   [--train_style_dir TRAIN_STYLE_DIR]
                   [--test_content_dir TEST_CONTENT_DIR]
                   [--test_style_dir TEST_STYLE_DIR] 
                   [--save_dir SAVE_DIR]
   ```

   

# Result

Some results of content image and my cat (called Sora) will be shown here.

![image](https://github.com/irasin/Pytorch_Style_Swap/blob/master/res/brad_pitt_en_campo_gris_demo.jpg)
![image](https://github.com/irasin/Pytorch_Style_Swap/blob/master/res/golden_gate_101308.jpg)
![image](https://github.com/irasin/Pytorch_Style_Swap/blob/master/res/golden_gate_hosi_demo.jpg)
![image](https://github.com/irasin/Pytorch_Style_Swap/blob/master/res/lenna_sketch_demo.jpg)
![image](https://github.com/irasin/Pytorch_Style_Swap/blob/master/res/neko_scene_de_rue_demo.jpg)
![image](https://github.com/irasin/Pytorch_Style_Swap/blob/master/res/neko_hosi_pair.jpg)



# My Opinion

The style-swap is implemented by a serious of convolutional operation.I am a beginner of Pytorch, so I afraid that my implementation technique are too poor so that it caused  style-swap consuming too much gpu memory. I will be very appreciated if you can improve this implementation.Feel free to give me a PR.Thanks.


Also, as you may know, [Adain](https://github.com/irasin/Pytorch_Adain_from_scratch) and [WCT](https://github.com/irasin/Pytorch_WCT) are more powerful than style-swap, check them if you are interested.
