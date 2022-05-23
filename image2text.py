import os
from paddleocr import PaddleOCR
import datetime
import re
# group txt into (info, boxx, boxy) sort_with_upperleft
def bbox_info(results):
    '''

    :param results:
    :return:
    '''
    data_list = []
    for result in results:
        info = result[1][0]
        boxx,boxy = result[0][0]
        data_list.append([info,int(boxx),int(boxy)])
    return data_list



def traverse_file(img_path,out_path):
    list = os.listdir(img_path)
    for i in range(0,len(list)):
        path = os.path.join(img_path,list[i])
        file_name = list[i][:-4]
        ocr_img(path, file_name, out_path)


def ocr_img(path,name,out_path):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(path, cls=True)
    text_sorted_list = result
    # text_sorted_list = xy_info(result)
    # print(text_sorted_list[:5])
    # text_sorted_list.sort(key=lambda x:-x[1])
    # data = xy_info.sort(key=takeSecond)
    datas = []
    for xy in text_sorted_list:
        # if (len(xy[0])>4) and re.match(r'[\u4e00-\u9fa5]+',xy[0],re.S):
        datas.append(xy)
        # print(xy[0],xy[1],xy[2])
    print(datas)
    if datas:
        file_path = os.path.join(out_path,name+'.txt')
        with open(file_path,'w',encoding='utf-8') as f:
            for line in datas:
                f.write(str(line))
                # f.write(line[0]+'\t'+str(line[1])+'\t'+str(line[2])+'\n')
    endTime_pdf2img = datetime.datetime.now()
    print(name,'time elapse', (endTime_pdf2img - startTime_pdf2img).seconds,'S')
    return result

if __name__ == "__main__":
    # 单张图片测试
    img_path = 'images/images_0.png'
    out_path = '/text'
    result = ocr_img(img_path, 'images_0', out_path)
    # 多张图片测试
    traverse_file("images/", "text")