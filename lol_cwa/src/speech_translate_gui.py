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
        self.lang = None
        self.config = Config().load()
        if self.config is None:
            self.config = {
                'model_saved_path': None,
                'lang': None
            }
        
        self.speech_model = None
        self.model_name = 'iic\\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
        model_dir = self.config['model_saved_path']
        if model_dir is not None:
            self.speech_model = SpeechModel(f"{model_dir}\\{self.model_name}")
        
        # 线程控制事件
        self.stop_event = threading.Event()
        self.is_audio_listening = False

        # 顶部frame
        top_frame = tk.LabelFrame(master, text='操作', bd=2, relief="groove", padx=5, pady=10)
        top_frame.pack()

        # 启动按钮
        self.start_btn = tk.Button(top_frame, text='启动', command=self.start)
        grid(self.start_btn, row=0, column=0)

        # 监听按键按钮
        self.key_listen_btn = tk.Button(top_frame, text='点击绑定按键', command=self.bind_key_listener)
        grid(self.key_listen_btn, row=1, column=0)

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

        # 将控制台的错误和print输出重定向到GUI的文本框中
        self.log_text = tk.Text(frame2, height=10, width=55)
        self.log_text.pack()
        # sys.stdout = RedirectText(self.log_text)
        # sys.stderr = RedirectText(self.log_text)

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


    def bind_key_listener(self):
        self.master.bind_all('<Key>', self.on_key_press)
        self.key_listen_btn.config(text='正在监听按键...')
        self.master.focus_set()

    def on_key_press(self, event):
        key = event.keysym
        print(f"按下键: {key} ({event.keycode})")
        self.key_listen_btn.config(text=f'已绑定到按键: {key}')
        self.master.unbind_all('<Key>')
        # 给已经绑定的按键添加事件
        self.master.bind_all(f'<KeyPress-{key}>', self.binded_key_pressed)

    def binded_key_pressed(self, event):
        self.stop_event.set()  # 停止之前的监听线程
        self.is_audio_listening.join(timeout=2)  # 等待线程结束，避免资源冲突
        self.stop_event.clear()  # 重置事件状态，为下一次监听做准备    

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
        save_path = self.save_path_entry.get()
        if not save_path:
            messagebox.showwarning("提示", "请选择保存位置！")
            return
        threading.Thread(target=model_download, args=(f"{save_path}\\",), daemon=True).start()


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


    def start(self):
        # 启用音频监听
        model_dir = self.save_path_entry.get()
        if not model_dir:
            messagebox.showwarning("警告", "请选择模型存放位置！")
            return
        if self.combobox.get() == '请选择要翻译成什么语言':
            messagebox.showwarning("警告", "请选择翻译语言！")
            return
        if self.config['model_saved_path'] is not None and self.speech_model is None:
            self.speech_model = SpeechModel(f"{model_dir}\\{self.model_name}")
        else:
            self.is_audio_listening = threading.Thread(
                target=self.speech_model.audio_listener, 
                args=(self.stop_event, self.process_data), 
                daemon=True)
            self.is_audio_listening.start()


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
            '2.选择需要翻译的语言，支持多种语言翻译\n'
            '3.上述操作完成之后点击启动，会等待数秒，启动后控制台会持续输出，此时麦克风音频已经开始监听，开始说话即可\n'
            '4.第一次使用后会将模型目录、上次选择的语言记录在配置文件中，非第一次进入后无需重新选择\n'
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


    def audio_listener(self, stop_event, callback=None):
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
            while not stop_event.is_set():
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
    sm = SpeechModel('~/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online')
    sm.audio_listener()
