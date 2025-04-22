# encoding-utf-8
import tkinter as tk


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