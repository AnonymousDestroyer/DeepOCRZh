# -*- coding: utf-8 -*-
# @Time    : 2022/5/31 3:45
# @Author  : Yujin Wang


# LIBRARIES
import fitz
import time
import os


def extract_images(filename):
    ''' Function that defines the method of image extraction from .pdf (editable) file.'''

    doc = fitz.open(filename)
    dir_name = str(filename[:-4])
    out_path = os.path.join("D:\PycharmProjects\DeepOCRZh\images", dir_name)
    print(out_path)

    if not os.path.exists(out_path):
        os.makedirs(out_path)
    print('Output dir/folder of images created.')

    imgcount = 0
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                imgcount += 1
                if pix.n > 5:
                    name = 'p%s-%s.jpg' % (i, xref)
                    output = os.path.join(out_path, name)
                    pix.save(output)
                else:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    name = 'p%s-%s.jpg' % (i, xref)
                    output = os.path.join(out_path, name)
                    pix1.save(output)
                    pix1 = None
                pix = None
            except:
                print('ERROR ENCOUNTERED AT FILE.')

    return print("Number of images extracted = ", imgcount)


# OUTPUT
pdf_path = '../pdf/more_texts.pdf'
extract_images(pdf_path)
print("Time taken (s) = ", round(time.perf_counter(), 2))
