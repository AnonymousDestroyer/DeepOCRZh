import io

import fitz
import re
import os
from PIL import Image

def pdf2pic(path, pic_path):
    '''
    # 从pdf中提取图片
    :param path: pdf的路径
    :param pic_path: 图片保存的路径
    :return:
    '''
    # 打开pdf
    doc = fitz.open(path)
    nums = len(doc)
    imgcount = 0  # 图像计数

    # 遍历每一个对象
    for i in range(1, 10):
        page = doc[i]
        # print(i, text)
        for img in doc.get_page_images(i):
            xref = img[0]
            image = doc.extract_image(xref)
            image_bytes = image['image']
            image_ext = image['ext']
            img = Image.open(io.BytesIO(image_bytes))
            img.save(open(os.path.join(pic_path, f"{i}_{xref}.{image_ext}"), "wb"))
            print("saving")
            imgcount += 1

if __name__ == '__main__':
    # pdf路径
    path = 'pdf/more_diagrams.pdf'

    # 保存的图片路径
    pic_path = 'images/'

    pdf2pic(path, pic_path)
