from replace_paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import math
import numpy as np
from IPython.display import display
from IPython.display import Image as IImage
import os
# layout analysis
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
def draw_bbox(image,
             boxes,
             scores=None,
             drop_score=0.5,):
    """
    Visualize the results of OCR detection and recognition
    args:
        image(Image|array): RGB image
        boxes(list): boxes with shape(N, 4, 2)
        txts(list): the texts
        scores(list): txxs corresponding scores
        drop_score(float): only scores greater than drop_threshold will be visualized
        font_path: the path of font which is used to draw text
    return(array):
        the visualized img
    """
    if scores is None:
        scores = [1] * len(boxes)
    box_num = len(boxes)
    for i in range(box_num):
        if scores is not None and (scores[i] < drop_score or
                                   math.isnan(scores[i])):
            continue
        box = np.reshape(np.array(boxes[i]), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 0), 2)
    return image

def visualise_current_plot(model, img_path):
    if not os.path.exists("./vis"):
        os.makedirs("./vis")

    result = model.ocr(img_path, cls=True)
    # draw result
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    # 可视化中文采用仿宋
    im_show = draw_bbox(image, boxes, scores)
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('./vis/table_result.png')
    interative_img = IImage('./vis/table_result.png')
    display(interative_img)