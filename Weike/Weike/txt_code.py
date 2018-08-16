# -*- coding: utf-8 -*-
from pytesseract import *
import PIL.ImageOps
import json
import math
import random
import requests
from PIL import Image
# class Get_code():
#     def __init__(self):
#         self.s =  requests.session()

def txt_code():
    # 打开图片
    threshold=170
    im=Image.open('E:/secode_show1.png')
    # 图片的处理过程 从颜色图像转为黑白图像, PLG 使用 PIL库使用ITU-R601-2 luma转换公式：
    # L = R * 299/1000 + G * 587/1000 + B * 114/1000
    initTable=lambda x: 0 if x < threshold else 1
    im=im.convert('L')
    # 当转换为2位图像（模式“1”）时，源图像首先被转换为黑白图像。结果数据中大于127的值被设置为白色，
    # 其他的设置为黑色；这样图像会出现抖动。如果要使用其他阈值，更改阈值127，可以使用方法point()。
    # 为了去掉图像抖动现象，可以使用dither选项。
    # 改变图像的阈值,为了更好的识别图片里面的内容
    binaryImage=im.point(initTable, '1')
    # 修改完阈值的设置为L模式 也就是转化为黑白图像
    im1=binaryImage.convert('L')
    # 对图像进行校准
    im2=PIL.ImageOps.invert(im1)
    # 校准完了以后设置为模式1
    im3=im2.convert('1')
    # 继续设置为黑吧图像
    im4=im3.convert('L')

    # 将图片中字符裁剪保留
    # 图片宽度为135，高度为40
    box=(0, 0, 140, 45)

    # 设置图片的大小
    region = im4.crop(box)
    # 将图片字符放大
    out=region.resize((135, 40))
    # 讲图片识别出来
    asd=pytesseract.image_to_string(im4)

    # 将图片打印GUI显示出来
    out.show()
    return input('请输入：')
def get_code():
    res = requests.get('https://www.epwk.com/secode_show.php?pre=login&sid='+str(math.radians(1)))
    with open('E:\secode_show1.png','wb') as f:
        f.write(res.content)

# if __name__ == '__main__':
# Start = Get_code()
get_code()
# txt_code()
   # Start.txt_code()
