from datetime import datetime

import tkinter as tk

import pytesseract
from PIL import Image, ImageGrab


def snapshot(region):
    formatted_time = datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot = ImageGrab.grab(bbox=region)
    filename = f"..\\snapshot\\screen_{formatted_time}.png"
    screenshot.save(filename)
    return filename


def to_string(filename):
    image = Image.open(filename)
    text = pytesseract.image_to_string(image, lang="chi_sim")
    return text


class ImageTranslator:

    def __init__(self):
        self.font = ("微软雅黑", 10)
        self.region = None

        root = tk.Tk()
        root.title("实时识图翻译工具")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 300
        height = 200

        # 居中
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

        # 选择区域
        window = tk.Toplevel(root)
        window.title("选择区域")
        window.geometry("400x200")
        window.attributes('-topmost', True)
        window.attributes('-alpha', 0.5)

        window_tip = tk.Label(window, text="移动到需要翻译的区域用此窗口覆盖，可手动调整窗口大小", font=self.font)
        window_tip.pack(padx=10, pady=10)

        def set_region():
            # 获取窗口位置 (相对于屏幕左上角)
            window_x = window.winfo_x()
            window_y = window.winfo_y()

            # 获取窗口宽度和高度
            window_width = window.winfo_width()
            window_height = window.winfo_height()

            # 获取窗口几何字符串 (如 "300x200+100+50")
            geometry = window.geometry()
            info = {
                "x": window_x,
                "y": window_y,
                "width": window_width,
                "height": window_height,
                "geometry": geometry
            }
            left_x = info['x']
            left_y = info['y']
            right_x = info['x'] + info['width']
            right_y = info['y'] + info['height']
            print(f"窗口区域：{left_x}:{left_y}-{right_x}:{right_y}")
            self.region = (left_x, left_y, right_x, right_y)
            window.iconify()

        def snapshot_(event):
            text = to_string(snapshot(self.region))
            print(text)

        root.bind("<Return>", snapshot_)

        get_region_btn = tk.Button(root, text="确认翻译区域", command=set_region)
        get_region_btn.pack()

        root.mainloop()


if __name__ == '__main__':
    it = ImageTranslator()

