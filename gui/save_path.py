#coding=utf-8
import os
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import LEFT


class SavePath():
    def __init__(self, root, path_save):
        self.entry_path = tk.Entry(
            root,
            width=100,
            font="13",
        )
        self.path_to_save = path_save

        self.entry_path.insert(0, self.path_to_save)

        self.btn_paste_1db = tk.Button(
            root,
            text='Выберите путь',
            fg='black',
            padx="14", pady="7", font="13",

            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.choose_directory1,
        )

        # self.btn_choose.grid(rowspan=1, columnspan=1)
        # self.btn_get.grid(rowspan=1, columnspan=1)

        self.List_for_paste_data = [
            self.entry_path,
            self.btn_paste_1db
        ]

    def rendre_save_path(self):
        self.btn_paste_1db.pack(expand=1, side=LEFT)
        self.entry_path.pack(expand=2, side=LEFT)

        # self.btn_paste_1db.grid(row=1, rowspan=1, columnspan=1)
        # self.btn_paste_2db.grid(rowspan=1, columnspan=1)

    def update_save_path(self):
        self.delete_save_path()
        self.rendre_save_path()

    def delete_save_path(self):
        for i in self.List_for_paste_data:
            i.pack_forget()

    def choose_directory1(self):

        directory = fd.askdirectory(title="Выбрать папку", initialdir=self.path_to_save)
        if os.path.exists(directory):
            self.path_to_save = directory
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, self.path_to_save)
            return self.path_to_save
        else:
            mb.showwarning("Ошибка выбрана не сущестуюшая папка  ", directory)
