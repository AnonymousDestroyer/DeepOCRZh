import datetime
import os
import fitz

def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        # page.get_pixmap() # int(width) int(length) alpha=False dpi=96
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96 (此处需要调节1-2之间)
        zoom_x = 1  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1
        # 提升分辨率
        # zoom factor in each dimension
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        # apply zoomed matrix to image
        pix = page.get_pixmap(matrix=mat, alpha=False)
        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建
        pix.save(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = '/content/DeepOCRZh/pdf/more_diagrams.pdf'
    # 2、需要储存图片的目录
    imagePath = './images'
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    pyMuPDF_fitz(pdfPath, imagePath)

if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = './pdf/more_diagrams.pdf'
    # 2、需要储存图片的目录
    imagePath = './images'
    pyMuPDF_fitz(pdfPath, imagePath)