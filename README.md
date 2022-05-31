# 中文光学字符辨识(OCR)

## 步骤
安装需要的环境:
Python 3.7.13
CUDA 11.x

```shell
pip install -r requirement.txt
```
## detectron2 (推荐)
!pip install layoutparser torchvision && pip install "git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2"
## efficientnet
!pip install "layoutparser[effdet]"
## paddle
!pip install "layoutparser[paddledetection]"

环境中包含tools, 解决paddleocr安装包兼容问题(https://github.com/PaddlePaddle/PaddleOCR/issues/1024)
将paddle中.tools替换成paddleocr.tools

先运行extract_image.py将pdf中的每一页存成图片
```shell
python extract_image.py
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

