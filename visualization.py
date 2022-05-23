from paddleocr import PaddleOCR,draw_ocr
from PIL import Image

# layout analysis
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
img_path = 'images/images_0.png'
result = ocr.ocr(img_path, cls=True)
# draw result

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
# 可视化中文采用仿宋
im_show = draw_ocr(image, boxes, txts, scores, font_path='/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('table_result.png')
