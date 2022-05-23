# 中文光学字符辨识(OCR)

## 步骤
安装需要的环境
```shell
pip install -r requirement.txt
```
先运行extract_image.py将pdf中的每一页存成图片
```shell
python3 extract_image.py
```
之后下载模型
```shell
python3 image2text.py
```
可视化(Optional)
```shell
python3 visualization.py
```

## TODO
*构建test数据集的文字GT
