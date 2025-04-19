import re
import threading
import time
import tkinter
from datetime import datetime

import tkinter as tk
from tkinter import ttk

import pytesseract
from gui import grid
from PIL import Image, ImageGrab
from utils import *


def snapshot(region):
    formatted_time = datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot = ImageGrab.grab(bbox=region)
    filename = f"..\\snapshot\\screen_{formatted_time}.png"
    screenshot.save(filename)
    return filename


def to_string(filename, lang):
    image = Image.open(filename)
    text = pytesseract.image_to_string(image, lang=lang)
    return text


class ImageTranslator:

    def __init__(self):
        self.font = ("微软雅黑", 10)
        self.region = None

        root = tk.Tk()
        root.title("实时识图翻译工具")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 300
        height = 200

        # 居中
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

        # 选择区域
        snapshot_zone = tk.Toplevel(root)
        snapshot_zone.title("选择区域")
        snapshot_zone.geometry("400x200")
        snapshot_zone.attributes('-topmost', True)
        snapshot_zone.attributes('-alpha', 0.7)

        tk.Label(snapshot_zone,
                 text="移动到需要翻译的区域用此窗口覆盖，可手动调整窗口大小",
                 font=self.font
                 ).pack(padx=10, pady=50)

        frame = tk.LabelFrame(root, text='设置', bd=2, relief="groove", padx=5, pady=10)
        frame.pack()

        # 下拉框数组
        lang_list = []
        for k in lang_name_2.keys():
            lang_list.append(k)
        lang_select_list = []
        for v in lang_name.values():
            lang_select_list.append(v)

        # 原始语言
        source_lang_label = tk.Label(frame, text="原始语言：")
        grid(source_lang_label, 0, 0)
        source_lang_combobox = ttk.Combobox(frame, values=lang_list)
        source_lang_combobox.config(state='readonly')
        grid(source_lang_combobox, 0, 1)

        # 翻译成的语言
        translate_lang_label = tk.Label(frame, text="翻译成的语言：")
        grid(translate_lang_label, 1, 0)
        translate_lang_combobox = ttk.Combobox(frame, values=lang_select_list)
        translate_lang_combobox.config(state='readonly')
        grid(translate_lang_combobox, 1, 1)

        # 译文输出区域
        translate_zone = tk.Toplevel(root)
        translate_zone.title("译文区域")
        translate_zone.geometry("350x400+400+200")
        translate_area = tk.Text(translate_zone, font=("微软雅黑", 12))
        scrollbar = tk.Scrollbar(translate_zone, command=translate_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        translate_area.config(yscrollcommand=scrollbar.set)
        translate_area.pack()

        get_region_btn = tk.Button(
            frame,
            text="开始翻译",
            command=lambda: self.set_region(snapshot_zone, translate_area)
        )
        grid(get_region_btn, 2, 0, columnspan=2)

        root.mainloop()

    def set_region(self, window: tk.Toplevel, output: tk.Text):
        # 获取窗口位置 (相对于屏幕左上角)
        window_x = window.winfo_x()
        window_y = window.winfo_y()

        # 获取窗口宽度和高度
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        # 获取窗口几何字符串 (如 "300x200+100+50")
        geometry = window.geometry()
        info = {
            "x": window_x,
            "y": window_y,
            "width": window_width,
            "height": window_height,
            "geometry": geometry
        }
        left_x = info['x']
        left_y = info['y']
        right_x = info['x'] + info['width']
        right_y = info['y'] + info['height']
        print(f"窗口区域：{left_x}:{left_y}-{right_x}:{right_y}")
        self.region = (left_x, left_y, right_x, right_y)
        window.iconify()

        def process_data(data: str):
            output.delete("1.0", tk.END)
            text = data.strip("\n")
            cleaned_text = text.replace('\n', ' ')  # 去除换行
            pattern = r'\[Team\] .+? \(.+?\): .*?(?=\[Team\]|$)'
            matches = re.findall(pattern, cleaned_text)
            for s in matches:
                output.insert(tk.END, f"{s}\n")
            output.see(tk.END)

        threading.Thread(target=self.loop_translate, args=(process_data,), daemon=True).start()

    def loop_translate(self, callback):
        while True:
            filename = snapshot(self.region)
            text = to_string(filename, "eng")
            callback(text)
            time.sleep(3)


if __name__ == '__main__':
    it = ImageTranslator()

