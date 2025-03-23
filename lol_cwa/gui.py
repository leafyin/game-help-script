# encoding=utf-8

import threading
import time
import tkinter as tk
from tkinter import ttk
import keyboard

# from demo import audio_listener
from translate import trans


LANG = {
    'zh': '中文',
    'en': '英语',
    'kor': '韩语',
    'jp': '日语',
    'ru': '俄语'
}


class AppGui:

    def __init__(self):
        self.font_size = 10

        root = tk.Tk()
        root.title('语音识别翻译助手')

        # 16:9长宽比
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        height = 250
        width = 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

        def onoff():
            # 启用音频监听
            # threading.Thread(target=audio_listener, args=(process_data, )).start()
            pass

        def download_model():
            print('下载模型')
            pass

        # 启动按钮
        onoff_btn = tk.Button(root, text='开启', command=onoff)
        onoff_btn.pack(pady=10)

        download_btn = tk.Button(root, text='下载模型', command=download_model)
        download_btn.pack(pady=10)

        # frame
        frame = tk.Frame(root)
        frame.pack(expand=True, fill='both')

        tk.Label(frame, text="要翻译的语言：", font=("微软雅黑", self.font_size)).grid(row=0, column=0)

        def on_select(event):
            reversed_lang = {v: k for k, v in LANG.items()}
            self.lang = reversed_lang[combobox.get()]
            if self.lang == 'zh':
                self.is_translate = False

        lang_name = []
        for v in LANG.values():
            lang_name.append(v)
        combobox = ttk.Combobox(frame, values=lang_name)
        combobox.grid(row=0, column=1)
        combobox.set('请选择')
        combobox.bind('<<ComboboxSelected>>', on_select)

        # 让窗口始终保持在最前，50%透明、移除标题栏
        # root.attributes('-topmost', True)
        # root.attributes('-alpha', 0.5)
        # root.overrideredirect(True)

        def process_data(data):
            pass

        def translate(data):
            keyboard.send('enter')
            time.sleep(0.05)
            translated = trans(data, 'zh', 'jp')

            keyboard.write(translated)
            keyboard.send('enter')

        # 运行 Tkinter 主循环
        root.mainloop()


if __name__ == '__main__':
    app = AppGui()

