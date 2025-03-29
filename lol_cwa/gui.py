# encoding=utf-8
import json
import os.path
import sys
import threading
import time
import tkinter as tk
import pyaudio
import numpy as np
import keyboard
import hashlib
import random
import requests

from pathlib import Path
from tkinter import ttk, filedialog, messagebox
from modelscope import snapshot_download

app_id = '20250321002311115'
private_key = '2CIieDd6J1OvEWpSyoej'
LANG = {
    'en': '英语',
    'kor': '韩语',
    'jp': '日语',
    'ru': '俄语'
}


def lang_reverse():
    """
    字典反转
    :return: 反转后的字典
    """
    reversed_lang = {v: k for k, v in LANG.items()}
    return reversed_lang


def model_download(path):
    """
    模型下载器
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


def sign(q, salt):
    text = app_id + q + salt + private_key
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode("utf-8"))
    return md5_hash.hexdigest()


def translate(text, src, to):
    """
    翻译
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
        return result['trans_result'][0]['dst']
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


class SpeechModel:

    def __init__(self, model_dir):
        from funasr import AutoModel
        # 加载实时流式语音识别模型
        self.model = AutoModel(
            model=model_dir,
            model_revision="v2.0.4",
            disable_update=True,
        )

    def audio_listener(self, callback):
        # 配置音频流参数
        chunk_size = [0, 10, 5]  # 600ms
        encoder_chunk_look_back = 4
        decoder_chunk_look_back = 1
        cache = {}

        # 初始化麦克风录音
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=9600)  # 600ms 的音频块
        try:
            result = ''
            count = 0
            while True:
                audio_chunk = stream.read(9600)  # 600ms
                speech_chunk = np.frombuffer(audio_chunk, dtype=np.int16)
                # 传递给模型进行实时识别
                res = self.model.generate(input=speech_chunk, cache=cache, is_final=False,
                                          chunk_size=chunk_size,
                                          encoder_chunk_look_back=encoder_chunk_look_back,
                                          decoder_chunk_look_back=decoder_chunk_look_back)
                talk = res[0]['text']
                if talk == '':
                    count += 1
                    if count == 5:  # 5 * 600ms 设定可能3秒后输出所说的话
                        if len(result) != 0:
                            callback(result)
                            result = ''
                        count = 0
                else:
                    result += talk
        except Exception as e:
            print(f"Error while reading audio: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()


class RedirectText:
    """ 用于重定向 print() 输出到 Tkinter 界面的 Text 组件 """
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)  # 在文本框追加内容
        self.text_widget.see(tk.END)  # 自动滚动到底部
        self.text_widget.update_idletasks()  # 更新 UI

    def flush(self):
        pass  # 必须定义 `flush()` 以兼容 `sys.stdout`


def grid(component: tk.Widget, row, column, padx=5, pady=5, sticky='nsew', columnspan=None, rowspan=None):
    """
    表格布局
    :return:
    """
    component.grid(
        row=row,
        column=column,
        padx=padx,
        pady=pady,
        sticky=sticky,
        rowspan=rowspan,
        columnspan=columnspan,
    )


class Config:

    def __init__(self):
        self.config_path = '.\\config.json'

    def save(self, json_data):
        with open(self.config_path, 'w') as f:
            json.dump(json_data, f, indent=4)

    def load(self):
        if not os.path.exists(self.config_path):
            return None
        with open(self.config_path, 'r') as f:
            return json.load(f)


class AppGui:

    def __init__(self):
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
        root = tk.Tk()
        root.title('语音识别翻译助手')

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        height = 500
        width = 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

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
            Config().save(my_config)    # 保存配置
            threading.Thread(target=speech_model.audio_listener, args=(process_data,), daemon=True).start()

        # 启动按钮
        onoff_btn = tk.Button(root, text='启动', command=onoff)
        onoff_btn.pack()

        # frame
        frame = tk.LabelFrame(root, text='配置', bd=2, relief="groove", padx=5, pady=10)
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
                messagebox.showwarning("警告", "请选择保存位置！")
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
            self.lang = lang_reverse()[combobox.get()]
            my_config['lang'] = self.lang

        lang_name = []
        for v in LANG.values():
            lang_name.append(v)
        combobox = ttk.Combobox(frame, values=lang_name)

        if self.config is not None:     # 语言配置
            combobox.set(LANG[self.config['lang']])     # lang name
        else:
            combobox.set('请选择')

        combobox.config(state='readonly')
        combobox.bind('<<ComboboxSelected>>', on_select)
        grid(combobox, row=1, column=1, columnspan=3)

        # frame2
        frame2 = tk.LabelFrame(root, text='控制台输出', bd=2, relief="groove", padx=5, pady=10)
        frame2.pack()

        # 控制台输出
        log_text = tk.Text(frame2, height=10, width=55)
        log_text.pack()

        # frame3
        frame3 = tk.LabelFrame(root, text='使用帮助', bd=2, relief="groove", padx=5, pady=10)
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

        # 浮动窗口，让窗口始终保持在最前，50%透明、移除标题栏
        window = tk.Toplevel(root)
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

            if self.lang is not None:   # 没选择语言则不翻译
                translate_text.insert(0, translate(data, 'zh', self.lang))
            else:
                translate_text.insert(0, data)

        def send(event):
            keyboard.send('enter')
            time.sleep(0.05)
            keyboard.write(translate_text.get())
            keyboard.send('enter')

        keyboard.on_press_key('enter', send)

        # 运行 Tkinter 主循环
        root.mainloop()


if __name__ == '__main__':
    app = AppGui()
