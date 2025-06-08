# encoding=utf-8
import sys
import threading
import time
import keyboard

from gui_utils import grid, tk, RedirectText
from utils import *
from model import SpeechModel
from tkinter import ttk, filedialog, messagebox


class SpeechTranslate(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.font = ("微软雅黑", 10)
        self.entry_font = ("微软雅黑", 20)

        # 初始化用户配置
        self.config = Config().load()
        if self.config is None or len(self.config) < 2:
            self.config = None
            my_config = {}
        else:
            my_config = self.config

        self.lang = None

        def onoff():
            # 启用音频监听
            model_name = '\\iic\\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
            model_dir = save_path_entry.get()
            if not model_dir:
                messagebox.showwarning("警告", "请选择模型存放位置！")
                return
            speech_model = SpeechModel(model_dir + model_name)
            sys.stdout = RedirectText(log_text)
            sys.stderr = RedirectText(log_text)
            # self.config.save(my_config)    # 保存配置
            threading.Thread(target=speech_model.audio_listener, args=(process_data,), daemon=True).start()

        # 启动按钮
        onoff_btn = tk.Button(master, text='启动', command=onoff)
        onoff_btn.pack()

        # frame
        frame = tk.LabelFrame(master, text='配置', bd=2, relief="groove", padx=5, pady=10)
        frame.pack()

        save_path_label = tk.Label(frame, text='模型保存路径：', font=self.font)
        save_path_entry = tk.Entry(frame)

        if self.config is not None:         # 模型路径配置
            save_path_entry.insert(0, self.config['model_saved_path'])

        save_path_entry.config(state='readonly')

        grid(save_path_label, row=0, column=0)
        grid(save_path_entry, row=0, column=1)

        def select_save_path():
            """
            选择模型存放位置
            :return:
            """
            filepath = filedialog.askdirectory(
                title='选择保存位置'
            )
            save_path_entry.config(state='normal')
            save_path_entry.delete(0, tk.END)  # 清空输入框
            save_path_entry.insert(0, filepath)  # 插入用户选择的路径
            my_config['model_saved_path'] = filepath
            save_path_entry.config(state='readonly')

        select_btn = tk.Button(frame, text="选择", command=select_save_path)
        grid(select_btn, row=0, column=2)

        # 下载模型
        def download_model():
            save_path = save_path_entry.get()
            if not save_path:
                messagebox.showwarning("提示", "请选择保存位置！")
                return
            model_download(save_path + '\\')

        def start_download():
            sys.stdout = RedirectText(log_text)
            sys.stderr = RedirectText(log_text)
            threading.Thread(target=download_model, daemon=True).start()

        download_btn = tk.Button(frame, text='下载', command=start_download)
        grid(download_btn, row=0, column=3)

        # 选择语言
        select_lang_label = tk.Label(frame, text="要翻译成什么语言？", font=self.font)
        grid(select_lang_label, row=1, column=0)

        def on_select(event):
            """
            语言选择
            :param event:
            :return:
            """
            self.lang = lang_code[combobox.get()]
            my_config['lang'] = self.lang

        lang_select_list = []
        for v in lang_name.values():
            lang_select_list.append(v)
        combobox = ttk.Combobox(frame, values=lang_select_list)

        if self.config is not None:     # 语言配置
            self.lang = self.config['lang']
            combobox.set(lang_name[self.config['lang']])     # lang name
        else:
            combobox.set('请选择')

        combobox.config(state='readonly')
        combobox.bind('<<ComboboxSelected>>', on_select)
        grid(combobox, row=1, column=1, columnspan=3)

        # frame2
        frame2 = tk.LabelFrame(master, text='控制台输出', bd=2, relief="groove", padx=5, pady=10)
        frame2.pack()

        # 控制台输出
        log_text = tk.Text(frame2, height=10, width=55)
        log_text.pack()

        # frame3
        frame3 = tk.LabelFrame(master, text='使用帮助', bd=2, relief="groove", padx=5, pady=10)
        frame3.pack()

        help_text = tk.Text(frame3, height=10, width=55)
        help_text.insert(
            '1.0',
            '1.第一次使用请先下载模型，选择模型保存路径，点击下载，下载进度在控制台输出，下载完成后控制台停止输出\n'
            '2.选择需要翻译的语言，支持（英语、韩语、日语、俄语）翻译\n'
            '3.上述操作完成之后点击启动，会等待数秒，启动后控制台会持续输出，此时麦克风音频已经开始监听，开始说话即可\n'
            '4.如果已经下载好模型，请直接选择模型保存路径，一般是根目录，iic目录的上一级目录，再选择翻译的语言，点击启动\n'
        )
        help_text.config(state='disabled')
        help_text.pack()

        # 浮动窗口，让窗口始终保持在最前，80%透明
        window = tk.Toplevel(master)
        window.title('')
        window.attributes('-topmost', True)
        window.attributes('-alpha', 0.8)

        source_text = tk.Entry(window, width=50, font=self.entry_font)
        source_text.pack()

        translate_text = tk.Entry(window, width=50, font=self.entry_font)
        translate_text.pack()

        def process_data(data):
            source_text.delete(0, tk.END)
            source_text.insert(0, data)

            translate_text.delete(0, tk.END)

            if self.lang is None or self.lang == 'zh':   # 没选择语言则不翻译
                translate_text.insert(0, data)
            else:
                translate_text.insert(0, baidu_translate(data, 'zh', self.lang))

        def send(event):
            keyboard.send('enter')
            time.sleep(0.05)
            keyboard.write(translate_text.get())
            keyboard.send('enter')

        keyboard.on_press_key('enter', send)


if __name__ == '__main__':
    pass
