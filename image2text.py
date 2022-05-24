import os
from paddleocr import PaddleOCR
import datetime
import re
import numpy as np
# group txt into (info, boxx, boxy) sort_with_upperleft

def fullfil_condition(up_left_x, up_left_y, up_right_x, up_right_y,
                      down_left_x, down_left_y, down_right_x, down_right_y):
    '''
    #TODO headline condition

    :param up_left_x:
    :param up_left_y:
    :param up_right_x:
    :param up_right_y:
    :param down_left_x:
    :param down_left_y:
    :param down_right_x:
    :param down_right_y:
    :return:
    '''
    return True
def extract_headline(results):
    '''
    #TODO 根据坐标提取标题
    :param results:
    :return:
    '''
    headline_list = []
    for res in results:
        text_box = res[1]
        up_left_x, up_left_y = res[0][0]
        up_right_x, up_right_y = res[0][1]
        down_left_x, down_left_y = res[0][2]
        down_right_x, down_right_y = res[0][3]
        if fullfil_condition(up_left_x, up_left_y, up_right_x, up_right_y,
                             down_left_x, down_left_y, down_right_x, down_right_y):

            headline_list.append({"text": text_box[0], "confidence": text_box[1]})
    return headline_list


def traverse_file(model, img_path, out_path):
    image_list = os.listdir(img_path)
    text_out_dir = []
    conf_list = []
    for f in image_list:
        path = os.path.join(img_path,f)
        file_name = f[:-4]
        ocrResult = ocr_img(model, path, file_name, out_path)   # 提取文字， bbox
        text_box, conf_list = split_col(ocrResult)      # 分栏 可能需要根据页面布局存数据
        out_file_path, avg_conf = save_current_page(file_name, out_path, text_box, conf_list)
        text_out_dir.append(out_file_path)
        conf_list.append(avg_conf)
    return text_out_dir, conf_list

def split_col(ocr_res):
    '''
    这里先写一个双栏的为了人工检查正确率。具体根据版面设计layout分块还要看paddleocr相应功能
    :param ocr_res:
    :return:
    '''
    left_list = []
    right_list = []
    conf_list = []
    for i, res in enumerate(ocr_res):
        text_box = res[1]
        up_left_x, up_left_y = res[0][0]
        if up_left_x > 600:
            right_list.append(str(i)+","+text_box[0])
        else:
            left_list.append(str(i)+","+text_box[0])
        conf_list.append(res[1][1])

    left_list.extend(right_list)
    return left_list, conf_list

def save_current_page(image_path, out_path, text_box, conf_list):
    '''
    为人工检验存储页面内容
    :param image_path:
    :param out_path:
    :param ocrResult:
    :return:
    '''
    # 最后一行是页码
    text = "\n".join(text_box[:-1])
    avg_conf = np.mean(conf_list)
    num = "".join(re.findall(r"[\d*]", image_path))
    out_file_path = os.path.join(out_path, "text"+num+'.txt')
    with open(out_file_path, "w") as f:
        f.writelines(text)
    return out_file_path, avg_conf

def ocr_img(model, path,name,out_path, min_count=0, ):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    result = model.ocr(path, cls=True)

    datas = []
    for bbox, text_box in result:
        # filter
        if (len(text_box[0]) > min_count) and re.match(r'[\u4e00-\u9fa5]+', text_box[0]):
            datas.append([bbox, text_box])
    if datas:
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        file_path = os.path.join(out_path,name+'.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in datas:
                f.write(str(line))
                # f.write(line[0]+'\t'+str(line[1])+'\t'+str(line[2])+'\n')
    endTime_pdf2img = datetime.datetime.now()
    print(name,'time elapse', (endTime_pdf2img - startTime_pdf2img).seconds,'S')
    return datas

if __name__ == "__main__":
    img_path = '/content/drive/MyDrive/pdf_reader/images/'
    out_path = '/content/drive/MyDrive/pdf_reader/more_text_storage'
    ocr_model_paddle = PaddleOCR(use_angle_cls=True, lang='ch')
    print("model loaded successfully")
    text_out_dir, conf_list = traverse_file(ocr_model_paddle, img_path, out_path)
    print(text_out_dir)
    print(np.mean(conf_list))