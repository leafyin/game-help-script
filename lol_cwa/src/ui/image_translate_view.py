# encoding=utf-8
"""
划区识图翻译 - UI 层
只负责界面布局和用户交互，业务逻辑委托给 service 模块
"""

import os
import sys
import time
import threading
import tkinter as tk
import difflib

from tkinter import ttk, messagebox
from service.translator import LANG_NAME, LANG_CODE, LANG_NAME_2, translate_text
from service.ocr import ocr_image
from service.image_capture import snapshot
from utils import grid


class ImageTranslateView(tk.Frame):
    """划区识图翻译 - 界面"""

    def __init__(self, master):
        super().__init__(master=master)
        self.font = ("微软雅黑", 10)

        # ---------- 状态 ----------
        self.region = None          # 截图区域 (left, top, right, bottom)
        self.source_lang = None     # 源语言 Tesseract 代码
        self.translate_lang = None  # 目标语言百度翻译代码
        self._stop_event = threading.Event()
        self._thread = None

        # ---------- 配置 Tesseract 路径 ----------
        # 支持两种模式：
        #   1) 源码调试：base_dir = src/
        #   2) PyInstaller 打包：base_dir = sys._MEIPASS（exe 解压出的临时目录）
        if hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        tesseract_path = os.path.join(base_dir, 'Tesseract-OCR', 'tesseract.exe')
        if os.path.exists(tesseract_path):
            import pytesseract as _pt
            _pt.pytesseract.tesseract_cmd = tesseract_path
        tessdata_dir = os.path.join(base_dir, 'tessdata')
        if os.path.exists(tessdata_dir):
            os.environ['TESSDATA_PREFIX'] = tessdata_dir

        # ---------- 截图保存目录 ----------
        self.snapshot_path = "snapshot"
        os.makedirs(self.snapshot_path, exist_ok=True)

        # ---------- 区域选择窗口 ----------
        self._snapshot_zone = tk.Toplevel(master)
        self._snapshot_zone.title("选择区域")
        self._snapshot_zone.geometry("400x200")
        self._snapshot_zone.attributes('-topmost', True)
        self._snapshot_zone.attributes('-alpha', 0.7)
        tk.Label(
            self._snapshot_zone,
            text="移动到需要翻译的区域用此窗口覆盖，可手动调整窗口大小",
            font=self.font,
        ).pack(padx=10, pady=50)

        # ---------- 设置面板 ----------
        frame = tk.LabelFrame(master, text='设置', bd=2, relief="groove", padx=5, pady=10)
        frame.pack()

        # 语言下拉框
        lang_list = list(LANG_NAME_2.keys())
        lang_select_list = list(LANG_NAME.values())

        def on_select(event):
            widget = event.widget
            if widget == source_lang_combobox:
                self.source_lang = LANG_NAME_2[widget.get()]
            if widget == translate_lang_combobox:
                self.translate_lang = LANG_CODE[widget.get()]

        # 识别的语言
        tk.Label(frame, text="识别的语言：").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        source_lang_combobox = ttk.Combobox(frame, values=lang_list, state='readonly')
        source_lang_combobox.set("选择")
        source_lang_combobox.bind('<<ComboboxSelected>>', on_select)
        source_lang_combobox.grid(row=0, column=1, padx=5, pady=5)

        # 翻译成的语言
        tk.Label(frame, text="翻译成的语言：").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        translate_lang_combobox = ttk.Combobox(frame, values=lang_select_list, state='readonly')
        translate_lang_combobox.set("选择")
        translate_lang_combobox.bind('<<ComboboxSelected>>', on_select)
        translate_lang_combobox.grid(row=1, column=1, padx=5, pady=5)

        # ---------- 译文输出区 ----------
        translate_zone = tk.LabelFrame(master, text="译文区域", bd=2, relief="groove", padx=5, pady=10)
        translate_zone.pack()
        self.output_text = tk.Text(translate_zone, font=("微软雅黑", 12), height=15)
        scrollbar = tk.Scrollbar(translate_zone, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # ---------- 按钮 ----------
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

    # ---------------------------------------------------------------
    # 按钮回调
    # ---------------------------------------------------------------
    def _start(self):
        """开始截图翻译循环"""
        if self.source_lang is None or self.translate_lang is None:
            messagebox.showwarning("提示", "请选择识别的语言和翻译成的语言！")
            return

        # 读取区域窗口位置
        x = self._snapshot_zone.winfo_x()
        y = self._snapshot_zone.winfo_y()
        w = self._snapshot_zone.winfo_width()
        h = self._snapshot_zone.winfo_height()
        self.region = (x, y, x + w, y + h)
        print(f"[截图区域] {self.region}")

        self._snapshot_zone.withdraw()  # 隐藏区域选择窗口
        self.output_text.delete(1.0, tk.END)
        self._stop_event.clear()

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _stop(self):
        """停止截图翻译循环"""
        self._stop_event.set()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.output_text.insert(tk.END, "\n[已停止]\n")

    
    def _is_duplicate(self, text: str, cache: set) -> bool:
        """模糊判断 text 是否和 cache 中已有内容相似（相似度 > 85% 视为重复）"""
        for existing in cache:
            ratio = difflib.SequenceMatcher(None, text, existing).ratio()
            if ratio > 0.85:
                return True
        return False

    # ---------------------------------------------------------------
    # 后台循环（截图 → OCR → 翻译 → 显示）
    # ---------------------------------------------------------------
    def _loop(self):
        """后台线程：截图 → OCR → 翻译 → 显示（相似内容跳过不输出）"""
        output_cache = set()  # 已输出的译文集合（用于模糊去重）
        while not self._stop_event.is_set():
            # 1. 截图
            filename = snapshot(self.region, self.snapshot_path)

            # 2. OCR 识别
            text = ocr_image(filename, self.source_lang)
            if not text:
                self._cleanup_file(filename)
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # 3. 翻译
                translated = translate_text(line, self.source_lang, self.translate_lang)
                if not translated:
                    continue

                # 4. 模糊去重：和已输出内容相似度 > 85% 则跳过
                normalized = translated.strip().lower()
                if self._is_duplicate(normalized, output_cache):
                    print(f"[跳过相似] {translated[:40]}")
                else:
                    print(f"[翻译] {translated[:40]}")
                    output_cache.add(normalized)
                    self.after(0, lambda t=translated: self._append_output(t))

                time.sleep(1.0)

    def _append_output(self, text: str):
        """追加译文到输出框（主线程安全）"""
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.see(tk.END)
