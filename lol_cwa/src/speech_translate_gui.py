# encoding=utf-8
import sys
import threading
import time
import keyboard
import numpy as np
import pyaudio

from utils import *
from tkinter import ttk, filedialog, messagebox


class SpeechTranslate(tk.Frame):

    def __init__(self, root, master):
        super().__init__(master)
        self.font = ("微软雅黑", 10)
        self.entry_font = ("微软雅黑", 20)

        # 初始化用户配置
        self.config = Config().load()
        if self.config is None:
            self.config = {
                'model_saved_path': None,
                'lang': None
            }
        self.lang = None

        # 状态变量
        self.onoff_ = True
        self.thread = None
        self.is_listening = False
        self.bound_key = None

        # 启动按钮
        self.onoff_btn = tk.Button(master, text='启动', command=self.onoff)
        self.onoff_btn.pack()

        # 配置frame
        frame = tk.LabelFrame(master, text='配置', bd=2, relief="groove", padx=5, pady=10)
        frame.pack()

        save_path_label = tk.Label(frame, text='模型保存位置：', font=self.font)
        grid(save_path_label, row=0, column=0)
        self.save_path_entry = tk.Entry(frame)
        # 如果之前有保存过路径，则默认显示在输入框中
        if self.config['model_saved_path'] is not None:
            self.save_path_entry.insert(0, self.config['model_saved_path'])
        self.save_path_entry.config(state='readonly')
        grid(self.save_path_entry, row=0, column=1)
        self.select_btn = tk.Button(frame, text="选择", command=self.select_save_path)
        grid(self.select_btn, row=0, column=2)

        self.download_btn = tk.Button(frame, text='下载', command=self.download_model)
        grid(self.download_btn, row=0, column=3)

        self.combobox = ttk.Combobox(frame, values=lang_names())
        # 如果之前选择过语言，则默认显示在下拉框中
        if self.config['lang'] is not None:
            self.lang = self.config['lang']
            self.combobox.set(lang_name[self.config['lang']])
        else:
            self.combobox.set('请选择要翻译成什么语言')
        self.combobox.config(state='readonly')
        self.combobox.bind('<<ComboboxSelected>>', self.lang_slector)
        grid(self.combobox, row=1, column=0, columnspan=4)

        # frame2
        frame2 = tk.LabelFrame(master, text='控制台输出', bd=2, relief="groove", padx=5, pady=10)
        frame2.pack()

        # 控制台输出
        self.log_text = tk.Text(frame2, height=10, width=55)
        self.log_text.pack()

        # frame3
        frame3 = tk.LabelFrame(master, text='使用帮助', bd=2, relief="groove", padx=5, pady=10)
        frame3.pack()

        self.help_tips(frame3)

        # 浮动窗口，让窗口始终保持在最前，80%透明
        window = tk.Toplevel(master)
        window.title('')
        window.attributes('-topmost', True)
        window.attributes('-alpha', 0.8)

        # 显示原文和译文的输入框
        self.source_text = tk.Entry(window, width=50, font=self.entry_font)
        self.translate_text = tk.Entry(window, width=50, font=self.entry_font)
        self.source_text.pack()
        self.translate_text.pack()

        def send(event):
            keyboard.send('enter')
            time.sleep(0.05)
            keyboard.write(self.translate_text.get())
            keyboard.send('enter')

        keyboard.on_press_key('enter', send)


    def lang_slector(self, event):
        """
        语言选择
        """
        self.lang = lang_code[self.combobox.get()]
        self.config['lang'] = self.lang
        Config().save(self.config)


    def download_model(self):
        '''
        下载模型，下载进度在控制台输出
        '''
        sys.stdout = RedirectText(self.log_text)
        sys.stderr = RedirectText(self.log_text)
        save_path = self.save_path_entry.get()
        if not save_path:
            messagebox.showwarning("提示", "请选择保存位置！")
            return
        model_download(save_path + '\\')


    def select_save_path(self):
        """
        选择模型存放位置
        :return:
        """
        filepath = filedialog.askdirectory(
            title='选择保存位置'
        )
        self.save_path_entry.config(state='normal')
        self.save_path_entry.delete(0, tk.END)  # 清空输入框
        self.save_path_entry.insert(0, filepath)  # 插入用户选择的路径
        self.config['model_saved_path'] = filepath
        # 更新配置中的模型保存路径
        Config().save(self.config)
        self.save_path_entry.config(state='readonly')


    def onoff(self):
        # 启用音频监听
        model_name = '\\iic\\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
        model_dir = self.save_path_entry.get()
        if not model_dir:
            messagebox.showwarning("警告", "请选择模型存放位置！")
            return
        speech_model = SpeechModel(model_dir + model_name)
        threading.Thread(target=speech_model.audio_listener, args=(self.process_data,), daemon=True).start()


    def process_data(self, data):
        '''
        回调函数，处理识别结果，更新文本并翻译
        :param data: 识别结果文本
        '''
        self.source_text.delete(0, tk.END)
        self.source_text.insert(0, data)
        self.translate_text.delete(0, tk.END)
        if self.lang is None or self.lang == 'zh':   # 没选择语言则不翻译
            self.translate_text.insert(0, data)
        else:
            self.translate_text.insert(0, baidu_translate(data, 'zh', self.lang))


    def help_tips(self, master):
        '''使用帮助提示框组件'''
        help_text = tk.Text(master, height=20, width=55)
        help_text.insert(
            1.0,
            '1.第一次使用请选择模型保存路径，点击下载，下载进度在控制台输出，下载完成后控制台停止输出\n'
            '2.选择需要翻译的语言，支持（英语、韩语、日语、俄语）翻译\n'
            '3.上述操作完成之后点击启动，会等待数秒，启动后控制台会持续输出，此时麦克风音频已经开始监听，开始说话即可\n'
            '4.如果已经下载好模型，请直接选择模型保存路径，一般是根目录，iic目录的上一级目录，再选择翻译的语言，点击启动\n'
        )
        help_text.config(state='disabled')
        help_text.pack()


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


if __name__ == '__main__':
    pass
