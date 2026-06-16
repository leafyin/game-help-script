# encoding=utf-8
"""
截图服务模块
提供屏幕区域截图功能
"""

import os

from PIL import ImageGrab


def snapshot(region: tuple, snapshot_path: str) -> str:
    """
    截取指定区域的屏幕截图
    :param region:        截图区域 (left, top, right, bottom)
    :param snapshot_path: 截图保存目录
    :return: 保存的图片文件路径
    """
    os.makedirs(snapshot_path, exist_ok=True)
    screenshot = ImageGrab.grab(bbox=region)
    filename = os.path.join(snapshot_path, f"screenshot.png")
    screenshot.save(filename)
    return filename
