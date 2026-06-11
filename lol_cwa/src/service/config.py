# encoding=utf-8
"""
配置管理模块
负责用户配置的读取、保存、持久化
"""

import json
import os


class Config:
    """用户配置管理器，将配置保存为 JSON 文件"""

    def __init__(self, config_path='../config.json'):
        self.config_path = config_path

    def save(self, json_data):
        """保存配置到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    def load(self):
        """从文件加载配置，文件不存在时返回 None"""
        if not os.path.exists(self.config_path):
            return None
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
