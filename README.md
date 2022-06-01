# 中文光学字符辨识(OCR)

## 步骤
安装需要的环境:
Python 3.7.13
CUDA 11.x

```shell
pip install -r requirement.txt
```
## detectron2 (中间�)
!pip install layoutparser torchvision && pip install "git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2"

## efficientnet (最后装
!pip install "layoutparser[effdet]"
## paddle (先装
!pip install "layoutparser[paddledetection]"

### 使用detectron2可能存在的兼容问题
环境中包含tools, 解决paddleocr安装包兼容问题(https://github.com/PaddlePaddle/PaddleOCR/issues/1024)
5.31 Efficient和paddle环境不存在上述问题

将paddle中.tools替换成paddleocr.tools
```
mv replace_paddleocr.py pathToYourPaddleOCR/paddleocr.py
```
colab
```
mv replace_paddleocr.py /usr/local/lib/python3.7/dist-packages/paddleocr/paddleocr.py
```
## Run the code
先运行extract_image.py将pdf中的每一页存成图片
```shell
python extract_from_pdf.py
```

## Layout Analysis
```
python layout_analysis.py
```

---------------------------- 文字信息抽取 --------------------------
之后下载模型
```shell
python3 image2text.py
```
可视化(Optional)
```shell
python3 visualization.py
```

