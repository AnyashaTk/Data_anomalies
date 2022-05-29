#coding=utf-8
import os
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import LEFT


class PasteData():
    def __init__(self, root):
        self.btn_paste_1db = tk.Button(
            root,
            text='Загрузить 1 базу',
            fg='black',
            padx="14", pady="7", font="13",

            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.choose_directory1,
        )
        self.map_path = dict()
        self.btn_paste_2db = tk.Button(
            root,
            text='Загрузить 2 базу ',
            fg='black',
            padx="14", pady="7", font="13",

            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.choose_directory2,
        )

        self.List_for_paste_data = [
            self.btn_paste_2db,
            self.btn_paste_1db
        ]

    def rendre_paste_data(self):
        self.btn_paste_1db.pack(expand=1, side=LEFT)
        self.btn_paste_2db.pack(expand=2, side=LEFT )

    def update_paste_data(self):
        self.delete_paste_data()
        self.rendre_paste_data()

    def delete_paste_data(self):
        for i in self.List_for_paste_data:
            i.pack_forget()

    def choose_directory1(self):

        directory = fd.askdirectory(title="Открыть папку", initialdir="/")
        if directory:

            if os.path.exists(directory + "/catch.csv") and os.path.exists(directory + "/product.csv"):
                self.map_path["db1"] = directory
                self.map_path["catch.csv"] = directory + "/catch.csv"
                self.map_path["product.csv"] = directory + "/product.csv"

                print(directory)


            else:
                mb.showerror("Ошибка выбрана не та папка ", directory)

    def choose_directory2(self):

        directory = fd.askdirectory(title="Открыть папку", initialdir="/")
        if directory:
            if os.path.exists(directory + "/Ext.csv") and os.path.exists(directory + "/Ext2.csv"):
                self.map_path["db2"] = directory
                self.map_path["Ext.csv"] = directory + "/Ext.csv"
                self.map_path["Ext2.csv"] = directory + "/Ext2.csv"
                print(directory)
            else:
                mb.showerror("Ошибка выбрана не та папка ", directory)
