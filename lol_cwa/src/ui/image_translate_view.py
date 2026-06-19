# encoding=utf-8
"""
划区识图翻译 - UI 层
只负责界面布局和用户交互，业务逻辑委托给 service 模块
"""

import os
import sys
import tkinter as tk
import difflib
import keyboard

from tkinter import ttk, messagebox
from service.translator import LANG_NAME, LANG_CODE, LANG_NAME_2, translate_text
from service.ocr import ocr_image
from service.image_capture import snapshot


class ImageTranslateView(tk.Frame):
    """划区识图翻译 - 界面"""

    def __init__(self, master):
        super().__init__(master=master)
        self.font = ("微软雅黑", 10)

        # ---------- 状态 ----------
        self.region = None               # 截图区域 (left, top, right, bottom)
        self.source_lang = None          # 源语言 Tesseract 代码
        self.translate_lang = None       # 目标语言百度翻译代码
        self._output_cache = set()       # 已输出译文（模糊去重）

        # ---------- 配置 Tesseract 路径 ----------
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

        lang_list = list(LANG_NAME_2.keys())
        lang_select_list = list(LANG_NAME.values())

        def on_select(event):
            widget = event.widget
            if widget == source_lang_combobox:
                self.source_lang = LANG_NAME_2[widget.get()]
            if widget == translate_lang_combobox:
                self.translate_lang = LANG_CODE[widget.get()]

        tk.Label(frame, text="识别的语言：").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        source_lang_combobox = ttk.Combobox(frame, values=lang_list, state='readonly')
        source_lang_combobox.set("选择")
        source_lang_combobox.bind('<<ComboboxSelected>>', on_select)
        source_lang_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="翻译成的语言：").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        translate_lang_combobox = ttk.Combobox(frame, values=lang_select_list, state='readonly')
        translate_lang_combobox.set("选择")
        translate_lang_combobox.bind('<<ComboboxSelected>>', on_select)
        translate_lang_combobox.grid(row=1, column=1, padx=5, pady=5)

        # ---------- 确认区域按钮 ----------
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.confirm_btn = tk.Button(
            btn_frame, text="确认区域并绑定 F1",
            command=self._confirm_region
        )
        self.confirm_btn.pack(padx=5)

        # ---------- 译文输出区 ----------
        translate_zone = tk.LabelFrame(master, text="译文区域", bd=2, relief="groove", padx=5, pady=10)
        translate_zone.pack(fill=tk.BOTH, expand=True)
        self.output_text = tk.Text(translate_zone, font=("微软雅黑", 12))
        scrollbar = tk.Scrollbar(translate_zone, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # ---------- 自动注册 F1 全局热键 ----------
        keyboard.add_hotkey('f1', self._on_f1, suppress=True)

    # ---------------------------------------------------------------
    # 确认区域
    # ---------------------------------------------------------------
    def _confirm_region(self):
        """从区域窗口读取坐标，确认截图区域"""
        if self.source_lang is None or self.translate_lang is None:
            messagebox.showwarning("提示", "请先选择识别的语言和翻译成的语言！")
            return

        x = self._snapshot_zone.winfo_x()
        y = self._snapshot_zone.winfo_y()
        w = self._snapshot_zone.winfo_width()
        h = self._snapshot_zone.winfo_height()
        self.region = (x, y, x + w, y + h)
        self._snapshot_zone.withdraw()
        print(f"[截图区域] {self.region}")

        self.output_text.delete(1.0, tk.END)
        self.confirm_btn.config(text=f"区域已确认 (F1)", state=tk.DISABLED)
        self.output_text.insert(tk.END, "[区域已确认，按下 F1 截图翻译]\n")

    # ---------------------------------------------------------------
    # F1 快捷键触发
    # ---------------------------------------------------------------
    def _on_f1(self):
        """F1 回调（keyboard 线程），通过 after 回到主线程执行"""
        self.after(0, self._capture_and_translate)

    def _capture_and_translate(self):
        """截图 → OCR → 翻译 → 输出"""
        if not self.region:
            return

        filename = snapshot(self.region, self.snapshot_path)

        text = ocr_image(filename, self.source_lang)
        if not text:
            self._cleanup_file(filename)
            return

        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            translated = translate_text(line, self.source_lang, self.translate_lang)
            if not translated:
                continue

            normalized = translated.strip().lower()
            if not self._is_duplicate(normalized, self._output_cache):
                self._output_cache.add(normalized)
                self.output_text.insert(tk.END, f"{translated}\n")
                self.output_text.see(tk.END)

        self._cleanup_file(filename)

    def _is_duplicate(self, text: str, cache: set) -> bool:
        for existing in cache:
            ratio = difflib.SequenceMatcher(None, text, existing).ratio()
            if ratio > 0.85:
                return True
        return False

    @staticmethod
    def _cleanup_file(filepath: str):
        try:
            os.remove(filepath)
        except Exception:
            pass
