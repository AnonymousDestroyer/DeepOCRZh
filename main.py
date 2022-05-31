from image2text import ocr_img
from visualization import visualise_current_plot
from replace_paddleocr import PaddleOCR

if __name__ == "__main__":
    # 单张图片测试
    img_path = 'images/images_16.png'
    out_path = './text'
    ocr_model_paddle = PaddleOCR(use_angle_cls=True, lang='ch')
    print("model loaded successfully")
    result = ocr_img(ocr_model_paddle, img_path, 'images_16', out_path)
    print(result)
    # 多张图片测试
    # traverse_file("images/", "text")
    visualise_current_plot(ocr_model_paddle, img_path)
