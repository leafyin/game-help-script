# encoding=utf-8
"""
主窗口 UI
包含多标签页导航，整合各个功能模块
"""

import tkinter as tk

from tkinter import ttk
from ui.image_translate_view import ImageTranslateView
from ui.speech_translate_view import SpeechTranslateView


class MainWindow(tk.Tk):
    """应用程序主窗口"""

    def __init__(self):
        super().__init__()
        self.title('火花spk工具箱')

        # 居中显示
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w, win_h = 600, 600
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        self.geometry(f"{win_w}x{win_h}+{x}+{y}")

        # 标签页导航
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # Tab 1: 语音识别翻译
        speech_frame = tk.Frame(self)
        SpeechTranslateView(speech_frame)
        speech_frame.pack()
        notebook.add(speech_frame, text='语音识别翻译')

        # Tab 2: 划区识图翻译
        image_frame = tk.Frame(self)
        ImageTranslateView(image_frame)
        image_frame.pack()
        notebook.add(image_frame, text='划区识图翻译')
