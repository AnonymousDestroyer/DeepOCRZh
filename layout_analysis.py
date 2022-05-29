import cv2
import layoutparser as lp
import numpy as np
import re
import os


def layout_analysis(net, img_path, save_path):
    sorted_imgs = sorted(os.listdir("/content/images"),
                         key=lambda x:int("".join(re.findall(r"[\d*]", x))))
    for i, f in enumerate(sorted_imgs[7:]):
        img_path = os.path.join(img_path, f)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # img = img[..., ::-1]
        layout = net.detect(img)
        show_img = lp.draw_box(img, layout, box_width=3, show_element_type=True)
        show_img.save(os.path.join(save_path, "layout%s.png"%i))


# load layout model
model = lp.PaddleDetectionLayoutModel(config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
                                threshold=0.5,
                                label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
                                enforce_cpu=False,
                                enable_mkldnn=True)
layout_analysis(model, "/content/images", "/content/processed_images")