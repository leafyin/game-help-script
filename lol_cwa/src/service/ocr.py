# encoding=utf-8
"""
OCR 识别服务模块
使用 pytesseract 对图片进行文字识别
"""

import os
import pytesseract

from PIL import Image


def ocr_image(image_path: str, source_lang: str = "eng") -> str:
    """
    对图片文件进行 OCR 文字识别
    :param image_path:  图片文件路径
    :param source_lang: Tesseract 语言代码（eng/jpn/kor）
    :return: 识别出的文本，失败返回空字符串
    """
    # image_path = '/Users/yinye/code/game-help-script/lol_cwa/snapshot/screen_20260611000257.png'
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    try:
        image = Image.open(image_path)
        lang = f"chi_sim+{source_lang}"
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"[OCR 识别失败] {e}")
        return ""
