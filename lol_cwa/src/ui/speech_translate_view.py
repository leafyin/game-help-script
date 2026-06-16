# encoding=utf-8
"""
语音识别翻译 - UI 层
只负责界面布局和用户交互，业务逻辑委托给 service 模块
"""

import threading
import tkinter as tk

from tkinter import ttk, filedialog, messagebox
from service.translator import LANG_NAME, LANG_CODE, baidu_translate
from service.config import Config
from service.speech_recognizer import SpeechRecognizer, download_model
from utils import grid


class SpeechTranslateView(tk.Frame):
    """语音识别翻译 - 界面"""

    def __init__(self, master):
        super().__init__(master)
        self.font = ("微软雅黑", 10)
        self.entry_font = ("微软雅黑", 20)

        # ---------- 状态 ----------
        self.lang = None             # 翻译目标语言代码
        self._recognizer = None      # SpeechRecognizer 实例
        self._stop_event = threading.Event()
        self._listen_thread = None

        # 加载配置
        self.config = Config().load()
        if self.config is None:
            self.config = {'model_saved_path': None, 'lang': None}

        # ---------- 操作面板 ----------
        top_frame = tk.LabelFrame(master, text='操作', bd=2, relief="groove", padx=5, pady=10)
        top_frame.pack()

        self.start_btn = tk.Button(top_frame, text='启动', command=self._start)
        grid(self.start_btn, row=0, column=0)

        self.toggle_window_btn = tk.Button(top_frame, text='隐藏窗口', command=self._toggle_float_window)
        grid(self.toggle_window_btn, row=0, column=1)

        self.key_listen_btn = tk.Button(top_frame, text='点击绑定按键', command=self._bind_key_listener)
        grid(self.key_listen_btn, row=1, column=0)

        # ---------- 配置面板 ----------
        frame = tk.LabelFrame(master, text='配置', bd=2, relief="groove", padx=5, pady=10)
        frame.pack()

        tk.Label(frame, text='模型保存位置：', font=self.font).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.save_path_entry = tk.Entry(frame)
        if self.config['model_saved_path'] is not None:
            self.save_path_entry.insert(0, self.config['model_saved_path'])
        self.save_path_entry.config(state='readonly')
        self.save_path_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame, text="选择", command=self._select_save_path).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame, text='下载', command=self._download).grid(row=0, column=3, padx=5, pady=5)

        # 语言选择
        self.combobox = ttk.Combobox(frame, values=list(LANG_NAME.values()))
        if self.config['lang'] is not None:
            self.lang = self.config['lang']
            self.combobox.set(LANG_NAME[self.config['lang']])
        else:
            self.combobox.set('请选择要翻译成什么语言')
        self.combobox.config(state='readonly')
        self.combobox.bind('<<ComboboxSelected>>', self._on_lang_select)
        self.combobox.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        # ---------- 控制台输出 ----------
        log_frame = tk.LabelFrame(master, text='控制台输出', bd=2, relief="groove", padx=5, pady=10)
        log_frame.pack()
        self.log_text = tk.Text(log_frame, height=10, width=55)
        self.log_text.pack()

        # ---------- 使用帮助 ----------
        help_frame = tk.LabelFrame(master, text='使用帮助', bd=2, relief="groove", padx=5, pady=10)
        help_frame.pack()
        help_text = tk.Text(help_frame, height=12, width=55)
        help_text.insert(
            1.0,
            '1. 第一次使用请选择模型保存路径，点击下载，下载进度在控制台输出\n'
            '2. 选择需要翻译的语言\n'
            '3. 上述操作完成之后点击启动，等待数秒后开始说话即可\n'
            '4. 配置会自动保存，非首次使用无需重新选择\n'
        )
        help_text.config(state='disabled')
        help_text.pack()

        # ---------- 浮动翻译窗口 ----------
        self._float_window = tk.Toplevel(master)
        self._float_window.title('')
        self._float_window.attributes('-topmost', True)
        self._float_window.attributes('-alpha', 0.8)

        self.source_text = tk.Entry(self._float_window, width=50, font=self.entry_font)
        self.translate_text = tk.Entry(self._float_window, width=50, font=self.entry_font)
        self.source_text.pack()
        self.translate_text.pack()

        import keyboard
        def _on_enter(event):
            keyboard.send('enter')
            import time
            time.sleep(0.05)
            keyboard.write(self.translate_text.get())
            keyboard.send('enter')
        keyboard.on_press_key('enter', _on_enter)

    # ---------------------------------------------------------------
    # 按钮回调
    # ---------------------------------------------------------------
    def _toggle_float_window(self):
        """切换浮动翻译窗口的显示/隐藏"""
        if self._float_window.state() == 'normal':
            self._float_window.withdraw()
            self.toggle_window_btn.config(text='显示窗口')
        else:
            self._float_window.deiconify()
            self.toggle_window_btn.config(text='隐藏窗口')

    def _start(self):
        """启动语音监听"""
        model_dir = self.save_path_entry.get()
        if not model_dir:
            messagebox.showwarning("警告", "请选择模型存放位置！")
            return
        if self.combobox.get() == '请选择要翻译成什么语言':
            messagebox.showwarning("警告", "请选择翻译语言！")
            return

        if self.config['model_saved_path'] is not None and self._recognizer is None:
            self._recognizer = SpeechRecognizer(model_dir)

        self._stop_event.clear()
        self._listen_thread = threading.Thread(
            target=self._recognizer.start_listening,
            args=(self._stop_event, self._on_speech_result),
            daemon=True,
        )
        self._listen_thread.start()

    def _bind_key_listener(self):
        """绑定按键监听"""
        self.master.bind_all('<Key>', self._on_key_press)
        self.key_listen_btn.config(text='正在监听按键...')
        self.master.focus_set()

    def _on_key_press(self, event):
        """按键绑定回调"""
        key = event.keysym
        print(f"按下键: {key} ({event.keycode})")
        self.key_listen_btn.config(text=f'已绑定到按键: {key}')
        self.master.unbind_all('<Key>')
        self.master.bind_all(f'<KeyPress-{key}>', self._on_binded_key)

    def _on_binded_key(self, event):
        """绑定的按键按下时，重启语音监听"""
        self._stop_event.set()
        if self._listen_thread:
            self._listen_thread.join(timeout=2)
        self._stop_event.clear()
        self._listen_thread = threading.Thread(
            target=self._recognizer.start_listening,
            args=(self._stop_event, self._on_speech_result),
            daemon=True,
        )
        self._listen_thread.start()

    def _on_lang_select(self, event):
        """语言选择回调"""
        self.lang = LANG_CODE[self.combobox.get()]
        self.config['lang'] = self.lang
        Config().save(self.config)

    def _download(self):
        """下载模型"""
        save_path = self.save_path_entry.get()
        if not save_path:
            messagebox.showwarning("提示", "请选择保存位置！")
            return
        threading.Thread(target=download_model, args=(save_path,), daemon=True).start()

    def _select_save_path(self):
        """选择模型保存路径"""
        filepath = filedialog.askdirectory(title='选择保存位置')
        if not filepath:
            return
        self.save_path_entry.config(state='normal')
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0, filepath)
        self.config['model_saved_path'] = filepath
        Config().save(self.config)
        self.save_path_entry.config(state='readonly')

    # ---------------------------------------------------------------
    # 语音识别结果回调
    # ---------------------------------------------------------------
    def _on_speech_result(self, data: str):
        """
        语音识别结果回调 — 更新界面并翻译
        :param data: 识别出的文本
        """
        self.source_text.delete(0, tk.END)
        self.source_text.insert(0, data)
        self.translate_text.delete(0, tk.END)

        if self.lang is None or self.lang == 'zh':
            self.translate_text.insert(0, data)
        else:
            translated = baidu_translate(data, 'zh', self.lang)
            self.translate_text.insert(0, translated or data)
