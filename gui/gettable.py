#coding=utf-8
import tkinter as tk
from datetime import datetime
from tkinter import LEFT

from logic.get_text import get_text_from_db, get_texts


class GetTable():
    def __init__(self, root, path_save, map_path):
        self.f_top = tk.Frame(root)
        self.f_bot = tk.Frame(root)

        self.path_save = path_save
        self.map_path = map_path
        self.month = 13

        self.btn_get_csv = tk.Button(
            self.f_top,
            text='Получить таблицs аномалий(После нажатия подождать\n несколько минут пока отработает программа ',
            fg='black',
            padx="14", pady="7", font="13",
            width=50,

            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.get_tables
        )
        self.message = tk.StringVar()
        self.entry_month = tk.Entry(
            self.f_top,
            textvariable=self.message,
            width=30,
            font="13",
        )
        self.hint = tk.Label(self.f_bot, width=80, height=100, text="Введите месяц (номер)")
        self.text = tk.Entry(self.f_bot, width=100)

        self.List_for_paste_data = [
            self.btn_get_csv,
            self.entry_month,
            self.text,
            self.f_top,
            self.f_bot
        ]

    def rendre_get_table(self):
        self.f_top.pack()
        self.f_bot.pack()
        self.btn_get_csv.pack(expand=1, side=LEFT)
        self.entry_month.pack(expand=1, side=LEFT)
        self.text.pack(expand=1, side=LEFT)
        self.hint.pack(expand=1, side=LEFT)

        # self.btn_paste_1db.grid(row=1, rowspan=1, columnspan=1)
        # self.btn_paste_2db.grid(rowspan=1, columnspan=1)

    def update_get_table(self):
        self.delete_get_table()
        self.rendre_get_table()

    def delete_get_table(self):
        for i in self.List_for_paste_data:
            i.pack_forget()

    def get_tables(self):
        self.month = self.message.get()
        if (self.month.isdigit()):
            self.month = int(self.month)
            if (self.month < 13 and self.month > 0):
                print("here")
                # print(self.path_save + "/" + str(datetime.now().date()) + '.csv')
                # my_file = open(self.path_save + str(datetime.now()) + '.csv', "w+")
                # with open(self.path_save + str(datetime.now()) + '.csv', 'wb'):
                #     pass
                self.text.delete(0, tk.END)
                self.text.insert(0, get_texts(map_path=self.map_path , save_path=self.path_save , month=self.month))
            #             todo save is save path
            else:
                pass
                # mb.showerror("Введите месяц в пределах 1 - 12 ")
        else:
            pass
            # mb.showerror("Введите число ")
