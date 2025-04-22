# encoding=utf-8
import json
import os.path
import hashlib
import random
import requests
import pytesseract

from pathlib import Path
from datetime import datetime
from PIL import Image, ImageGrab
from modelscope import snapshot_download

app_id = '20250321002311115'
private_key = '2CIieDd6J1OvEWpSyoej'
lang_name = {
    "zh": "中文",
    "cht": "繁体中文",
    "yue": "粤语",
    "wyw": "文言文",
    "en": "英语",
    "jp": "日语",
    "kor": "韩语",
    "fra": "法语",
    "spa": "西班牙语",
    "th": "泰语",
    "ara": "阿拉伯语",
    "ru": "俄语",
    "pt": "葡萄牙语",
    "de": "德语",
    "it": "意大利语",
    "el": "希腊语",
    "nl": "荷兰语",
    "pl": "波兰语",
    "bul": "保加利亚语",
    "est": "爱沙尼亚语",
    "dan": "丹麦语",
    "fin": "芬兰语",
    "cs": "捷克语",
    "rom": "罗马尼亚语",
    "slo": "斯洛文尼亚语",
    "swe": "瑞典语",
    "hu": "匈牙利语",
    "vie": "越南语"
}

lang_code = {
    "中文": "zh",
    "繁体中文": "cht",
    "英语": "en",
    "粤语": "yue",
    "文言文": "wyw",
    "日语": "jp",
    "韩语": "kor",
    "法语": "fra",
    "西班牙语": "spa",
    "泰语": "th",
    "阿拉伯语": "ara",
    "俄语": "ru",
    "葡萄牙语": "pt",
    "德语": "de",
    "意大利语": "it",
    "希腊语": "el",
    "荷兰语": "nl",
    "波兰语": "pl",
    "保加利亚语": "bul",
    "爱沙尼亚语": "est",
    "丹麦语": "dan",
    "芬兰语": "fin",
    "捷克语": "cs",
    "罗马尼亚语": "rom",
    "斯洛文尼亚语": "slo",
    "瑞典语": "swe",
    "匈牙利语": "hu",
    "越南语": "vie"
}

lang_name_2 = {
    "英语": "eng",
    "日语": "jpn",
    "韩语": "kor"
}


class Config:

    def __init__(self):
        self.config_path = '../config.json'

    def save(self, json_data):
        with open(self.config_path, 'w') as f:
            json.dump(json_data, f, indent=4)

    def load(self):
        if not os.path.exists(self.config_path):
            return None
        with open(self.config_path, 'r') as f:
            return json.load(f)


def snapshot(region, snapshot_path):
    formatted_time = datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot = ImageGrab.grab(bbox=region)
    filename = f"{snapshot_path}\\screen_{formatted_time}.png"
    screenshot.save(filename)
    return filename


def image_to_string(filename, lang):
    image = Image.open(filename)
    text = pytesseract.image_to_string(image, lang=lang)
    return text


def sign(q, salt):
    text = app_id + q + salt + private_key
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode("utf-8"))
    return md5_hash.hexdigest()


def baidu_translate(text, src, to):
    """
    百度翻译api
    :param text: 原文
    :param src: 原文语言
    :param to: 译文语言
    :return: 译文
    """
    salt = str(random.randint(10 ** 7, 10 ** 8 - 1))
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "q": text,
        "from": src,
        "to": to,
        "appid": app_id,
        "salt": salt,
        "sign": sign(text, salt)
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        result = response.json()
        print(result)
        return result['trans_result'][0]['dst']
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def model_download(path):
    """
    模型下载
    :param path: 路径
    :return: ？？？
    """
    model_name = 'iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
    for i in model_name.split('/'):
        path += f'{i}\\'
        Path(path).mkdir(exist_ok=True)
    model_dir = snapshot_download(
        model_id=model_name,
        local_dir=path
    )
    return model_dir

