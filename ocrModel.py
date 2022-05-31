import cv2
import layoutparser as lp
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import pandas as pd
from replace_paddleocr import PaddleOCR

boundary = 5
MODEL_CATALOG = {
    "FasterRCNN": "lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",
    "MaskedRCNN": {
        "resnet50": "lp://PubLayNet/mask_rcnn_R_50_FPN_3x/config",
        "resnet101": "lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config"
    },
    "PaddleYoLov2": "lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
    "TableBank": "lp://TableBank/faster_rcnn_R_101_FPN_3x/config",
    "Newspaper": "lp://NewspaperNavigator/faster_rcnn_R_50_FPN_3x/config"
}


def layout_analysis(net, ocr_net, img_path, save_path):
    sorted_imgs = sorted(os.listdir(img_path),
                         key=lambda x: int("".join(re.findall(r"[\d*]", x))))
    total_num = 0
    block_record = []
    for i, f in enumerate(sorted_imgs):

        img = os.path.join(img_path, f)
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        height, width, channels = img.shape  # y, x, c
        print(height, width)
        # img = img[..., ::-1]
        layout = net.detect(img)

        for j, block in enumerate(layout._blocks):
            if block.type == "Title":
                _block = block.block
                x_2, y_2 = int(_block.x_2), int(_block.y_2)
                x_1, y_1 = int(_block.x_1), int(_block.y_1)
                text_region = img[y_1:y_2, x_1:x_2, ...]  # crop text region out
                ocr_title = ocr_net(text_region, cls=True)

            if block.type == "Figure":
                _block = block.block
                x_2, y_2 = int(_block.x_2), int(_block.y_2)
                x_1, y_1 = int(_block.x_1), int(_block.y_1)
                x_1 = max(x_1 - boundary, 0)
                y_1 = max(y_1 - boundary, 0)
                x_2 = min(x_2 + boundary, width)
                y_2 = min(y_2 + boundary, height)
                minipage = img[y_1:y_2, x_1:x_2, ...]  # crop

                # visualize
                # plt.imshow(minipage)
                # plt.show()
                cv2.imwrite("/content/minipages/img_%i_mini_%s.png" % (i, j), minipage)

                # record
                block_record.append(pd.DataFrame([[i, total_num, (x_1, y_1, x_2, y_2), block.score]],
                                                 columns=['page', 'id', 'coordinate', 'score']))
                #  columns=['page', 'id', 'title', 'coordinate', 'score']))
                total_num += 1
        # bbox analysis
        show_img = lp.draw_box(img, layout, box_width=3, show_element_type=True)
        show_img.save(os.path.join(save_path, "layout%s.png" % i))

    block_record = pd.concat(block_record, axis=0, ignore_index=True)
    block_record.to_csv("/content/block_record.csv")


# load layout model
# model = lp.PaddleDetectionLayoutModel(config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
#                                 threshold=0.5,
#                                 label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
#                                 enforce_cpu=False,
#                                 enable_mkldnn=True)
ocr_model_paddle = PaddleOCR(use_angle_cls=True, lang='ch')

model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                                 extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.80],
                                 label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})

# model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_R_101_FPN_3x/config',
#                                  extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.90],
#                                  label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})
layout_analysis(model, "/content/DeepOCRZh/images", "/content/processed")