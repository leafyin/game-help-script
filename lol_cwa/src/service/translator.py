# encoding=utf-8
"""
翻译服务模块
封装百度翻译 API，提供语言代码映射和翻译缓存
"""

import hashlib
import random
import time
import requests

# ============================================================
# 百度翻译 API 凭证（请替换为你自己的 appid 和密钥）
# ============================================================
APP_ID = '20250321002311115'
PRIVATE_KEY = '2CIieDd6J1OvEWpSyoej'

# ============================================================
# 语言名称映射表
# ============================================================

# 语言英文代码 → 中文名称（用于 UI 下拉框）
LANG_NAME = {
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

# 中文名称 → 百度翻译语言代码（用于翻译目标语言选择）
LANG_CODE = {
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

# 中文名称 → Tesseract 语言代码（用于 OCR 源语言选择）
LANG_NAME_2 = {
    "英语": "eng",
    "日语": "jpn",
    "韩语": "kor"
}

# ============================================================
# 翻译缓存（避免频繁调用百度 API）
# ============================================================
_translation_cache: dict = {}


def _cache_key(text: str, src: str, dst: str) -> tuple:
    """生成缓存键，归一化处理以匹配相似文本"""
    normalized = text.strip().lower()
    return (normalized, src, dst)


def _get_cached(text: str, src: str, dst: str) -> str | None:
    """查缓存，命中直接返回翻译结果"""
    key = _cache_key(text, src, dst)
    cached = _translation_cache.get(key)
    if cached is not None:
        print(f"[翻译缓存命中] {text[:40]} -> {cached[:40]}")
        return cached
    return None


def _set_cache(text: str, src: str, dst: str, translated: str):
    """写入翻译缓存"""
    key = _cache_key(text, src, dst)
    _translation_cache[key] = translated


def get_lang_names() -> list:
    """获取所有语言的中文名称列表（用于 UI 下拉框）"""
    return list(LANG_NAME.values())


def map_source_lang(source_lang: str) -> str:
    """将 Tesseract 语言代码映射为百度翻译语言代码"""
    mapping = {
        "eng": "en",
        "jpn": "jp",
        "kor": "kor",
    }
    return mapping.get(source_lang, source_lang)


def _sign(q: str, salt: str) -> str:
    """生成百度翻译 API 签名"""
    text = APP_ID + q + salt + PRIVATE_KEY
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def baidu_translate(text: str, src: str, to: str) -> str | None:
    """
    调用百度翻译 API
    :param text: 原文
    :param src:   源语言代码（如 en, jp, kor）
    :param to:    目标语言代码（如 zh）
    :return: 译文，失败返回 None
    """
    salt = str(random.randint(10 ** 7, 10 ** 8 - 1))
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "q": text,
        "from": src,
        "to": to,
        "appid": APP_ID,
        "salt": salt,
        "sign": _sign(text, salt)
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        result = response.json()
        # print(f"[百度翻译] {text[:40]} -> {result}")
        return result['trans_result'][0]['dst']
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"[百度翻译失败] {e}")
        return None


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    翻译单行文本（带缓存）
    :param text:         原文
    :param source_lang:  Tesseract 语言代码（eng/jpn/kor）
    :param target_lang:  百度翻译目标语言代码（zh/en/jp...）
    :return: 翻译后的文本
    """
    if not text:
        return ""

    src = map_source_lang(source_lang)

    # 查缓存
    cached = _get_cached(text, src, target_lang)
    if cached is not None:
        return cached

    # 缓存未命中，调用 API
    translated = baidu_translate(text, src, target_lang)
    if translated:
        _set_cache(text, src, target_lang, translated)
    return translated or ""
