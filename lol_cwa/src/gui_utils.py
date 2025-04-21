# encoding-utf-8
import tkinter as tk


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