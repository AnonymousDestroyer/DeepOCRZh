import cv2
import layoutparser as lp
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import pandas as pd
import sys

sys.path.append("./")
from paddleocr import PaddleOCR
import time
from collections import deque

BOUNDARY = 5
MINILEN = 1

img_path = "./images"
save_path = "./result"
os.makedirs(save_path, exist_ok=True)
os.makedirs(save_path + "minipages", exist_ok=True)
os.makedirs(save_path + "layout_vis", exist_ok=True)

MODEL_CATALOG = {
    "EfficientNet":
        {
            "d0": "lp://efficientdet/PubLayNet/tf_efficientdet_d0",
            "d1": "lp://efficientdet/PubLayNet/tf_efficientdet_d1"
        },
    "FasterRCNN": "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",
    "MaskedRCNN": {
        "resnet50": "lp://PubLayNet/mask_rcnn_R_50_FPN_3x/config",
        "resnet101": "lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config"
    },
    "PaddleYoLov2": "lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
    "TableBank": "lp://TableBank/faster_rcnn_R_101_FPN_3x/config",
    "Newspaper": "lp://NewspaperNavigator/faster_rcnn_R_50_FPN_3x/config"
}


def ocr_text(text_net, region):
    if region is None:
        return None

    ocr_title = text_net(region, cls=True)
    text_bbox, text_box = ocr_title
    if text_bbox and text_box:
        # filter
        if (len(text_box[0]) < MINILEN) or (re.match(r'[\u4e00-\u9fa5]+', text_box[0][0]) is None):
            return None
        ocr_title = "".join(text_box[0][0])
        title_score = text_box[0][1]

        return ocr_title, title_score
    else:
        return None


def layout_analysis(net, ocr_net, img_path, save_path):
    sorted_imgs = sorted(os.listdir(img_path),
                         key=lambda x: int("".join(re.findall(r"[\d*]", x))))
    total_num = 0
    block_record = []
    for i, f in enumerate(sorted_imgs):

        img = os.path.join(img_path, f)
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        height, width, channels = img.shape  # y, x, c
        # img = img[..., ::-1]
        layout = net.detect(img)

        ocr_title = "None"
        title_score = 0
        last_text_region = None
        for j, block in enumerate(layout._blocks):

            if block.type == "Title":
                _block = block.block
                x_2, y_2 = int(_block.x_2), int(_block.y_2)
                x_1, y_1 = int(_block.x_1), int(_block.y_1)
                text_region = img[y_1:y_2, x_1:x_2, ...]  # crop text region out
                if ocr_title == "None" and title_score == 0:
                    ocr_text_result = ocr_text(ocr_net, text_region)
                    if ocr_text_result is None:
                        continue
                    else:
                        ocr_title, title_score = ocr_text_result

            elif block.type == "Text":
                _block = block.block
                x_2, y_2 = int(_block.x_2), int(_block.y_2)
                x_1, y_1 = int(_block.x_1), int(_block.y_1)
                last_text_region = img[y_1:y_2, x_1:x_2, ...]  # update last text region

            elif block.type == "Figure":
                _block = block.block
                x_2, y_2 = int(_block.x_2), int(_block.y_2)
                x_1, y_1 = int(_block.x_1), int(_block.y_1)
                x_1 = max(x_1 - BOUNDARY, 0)
                y_1 = max(y_1 - BOUNDARY, 0)
                x_2 = min(x_2 + BOUNDARY, width)
                y_2 = min(y_2 + BOUNDARY, height)
                minipage = img[y_1:y_2, x_1:x_2, ...]  # crop

                # visualize
                # plt.imshow(minipage)
                # plt.show()
                cv2.imwrite(os.path.join(save_path + "minipages", "img_%i_mini_%s.png" % (i, j)), minipage)

                # use last text as title
                if ocr_title == "None" and title_score == 0:
                    ocr_text_result = ocr_text(ocr_net, last_text_region)
                    if ocr_text_result is not None:
                        ocr_title, title_score = ocr_text_result

                block_record.append(
                    pd.DataFrame([[i, total_num, ocr_title, title_score, (x_1, y_1, x_2, y_2), block.score]],
                                 columns=['page', 'id', 'title', 'title_score', 'coordinate', 'score']))
                total_num += 1
            else:
                continue

        # bbox analysis
        show_img = lp.draw_box(img, layout, box_width=3, show_element_type=True)
        show_img.save(os.path.join(save_path + "layout_vis", "layout%s.png" % i))

    block_record = pd.concat(block_record, axis=0, ignore_index=True)
    block_record.to_csv(os.path.join(save_path, "block_record.csv"))


# load layout model
model = lp.PaddleDetectionLayoutModel("lp://PubLayNet/ppyolov2_r50vd_dcn_365e/config")
ocr_model_paddle = PaddleOCR(use_angle_cls=True, lang='ch')

# model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
#                                  extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.80],
#                                  label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})

# model = lp.EfficientDetLayoutModel('lp://efficientdet/PubLayNet/tf_efficientdet_d1',
#                                    )
# model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_R_101_FPN_3x/config',
#                                  extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.90],
#                                  label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})

layout_analysis(model, ocr_model_paddle, img_path=img_path, save_path=save_path)
