# encoding=utf-8
from gui_utils import tk
from tkinter import ttk

from image_translate_gui import ImageTranslator
from speech_translate_gui import SpeechTranslate


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('火花spk工具箱')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        height = 500
        width = 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        # tab导航标签
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        frame_box = tk.Frame(self)
        SpeechTranslate(self, frame_box)
        frame_box.pack()

        frame_box2 = tk.Frame(self)
        ImageTranslator(frame_box2)
        frame_box2.pack()

        notebook.add(frame_box, text='语音识别翻译')
        notebook.add(frame_box2, text='划区识图翻译')

        self.mainloop()


if __name__ == '__main__':
    GUI()
