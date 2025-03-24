# encoding=utf-8
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import keyboard
from modelscope import snapshot_download

from demo import *
from translate import trans

LANG = {
    'en': '英语',
    'kor': '韩语',
    'jp': '日语',
    'ru': '俄语'
}


def model_download(path):
    model_name = 'iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
    for i in model_name.split('/'):
        path += f'{i}\\'
        Path(path).mkdir(exist_ok=True)
    model_dir = snapshot_download(
        model_id=model_name,
        local_dir=path
    )
    return model_dir


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


class AppGui:

    def __init__(self):
        self.font = ("微软雅黑", 10)
        self.entry_font = ("微软雅黑", 20)

        self.lang = None
        root = tk.Tk()
        root.title('语音识别翻译助手')

        # 16:9长宽比
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        height = 500
        width = 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

        def onoff():
            # 启用音频监听
            switch = True
            if switch:
                model_name = '\\iic\\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online'
                model_dir = save_path_entry.get()
                speech_model = SpeechModel(model_dir + model_name)
                sys.stdout = RedirectText(log_text)
                threading.Thread(target=speech_model.audio_listener, args=(process_data,), daemon=True).start()


        # 启动按钮
        onoff_btn = tk.Button(root, text='开启', command=onoff)
        onoff_btn.pack(pady=10)

        download_frame = tk.Frame(root)
        download_frame.pack(expand=True, fill='both')

        # 模型下载存放位置
        def select_save_path():
            filepath = filedialog.askdirectory(
                title='选择保存位置'
            )
            save_path_entry.delete(0, tk.END)  # 清空输入框
            save_path_entry.insert(0, filepath)  # 插入用户选择的路径

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

        tk.Label(download_frame, text='模型保存路径：', font=self.font).pack(pady=10)
        save_path_entry = tk.Entry(download_frame)
        save_path_entry.pack(pady=10)
        select_btn = tk.Button(download_frame, text="选择", command=select_save_path)
        select_btn.pack(pady=10)

        download_btn = tk.Button(download_frame, text='下载模型', command=start_download)
        download_btn.pack(pady=10)

        log_text = tk.Text(download_frame, height=10, width=50)
        log_text.pack(pady=10)

        # frame
        frame = tk.Frame(root)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="要翻译成什么语言？", font=self.font).pack(pady=10)

        def on_select(event):
            reversed_lang = {v: k for k, v in LANG.items()}
            self.lang = reversed_lang[combobox.get()]

        lang_name = []
        for v in LANG.values():
            lang_name.append(v)
        combobox = ttk.Combobox(frame, values=lang_name)
        combobox.pack(pady=10)
        combobox.set('请选择')
        combobox.bind('<<ComboboxSelected>>', on_select)

        # 浮动窗口，让窗口始终保持在最前，50%透明、移除标题栏
        window = tk.Toplevel(root)
        window.attributes('-topmost', True)
        window.attributes('-alpha', 0.8)
        window.overrideredirect(True)

        source_text = tk.Entry(window, width=50, font=self.entry_font)
        source_text.pack()

        translate_text = tk.Entry(window, width=50, font=self.entry_font)
        translate_text.pack()

        def process_data(data):
            source_text.delete(0, tk.END)
            source_text.insert(0, data)

            translate_text.delete(0, tk.END)
            translate_text.insert(0, trans(data, 'zh', self.lang))

            keyboard.send('enter')
            time.sleep(0.05)
            keyboard.write(translate_text.get())
            keyboard.send('enter')

        # 运行 Tkinter 主循环
        root.mainloop()


if __name__ == '__main__':
    app = AppGui()
