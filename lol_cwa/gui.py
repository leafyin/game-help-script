# encoding=utf-8

import threading
import time
import tkinter as tk

import keyboard

from demo import audio_listener
from translate import trans


def gui():

    def process_data(data):
        entry.delete(0, tk.END)
        entry.insert(0, data)
        keyboard.send('enter')
        time.sleep(0.05)
        t = trans(data,'zh', 'jp')
        keyboard.write(f'{data}-翻译-{t}')
        keyboard.send('enter')
        # print(data)

    root = tk.Tk()

    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(pady=10)

    # 让窗口始终保持在最前，50%透明、移除标题栏
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.5)
    root.overrideredirect(True)

    # 启用音频监听
    threading.Thread(target=audio_listener, args=(process_data, )).start()

    # 运行 Tkinter 主循环
    root.mainloop()


if __name__ == '__main__':
    gui()

