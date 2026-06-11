# encoding=utf-8
"""
工具模块
提供 UI 布局辅助函数等通用工具
"""

import tkinter as tk


def grid(component: tk.Widget, row, column, padx=5, pady=5, sticky='nsew', columnspan=None, rowspan=None):
    """
    网格布局辅助函数
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

