#coding=utf-8

from gettable import *
from gui import PATH_TO_SAVE
from paste_csv import *
from save_path import SavePath


class MainMenu():
    def __init__(self, root):
        self.path_to_save = PATH_TO_SAVE
        self.pd = PasteData(root)
        self.phsv = SavePath(root, path_save=self.path_to_save)

        self.gt = GetTable(root, path_save=self.phsv.path_to_save, map_path=self.pd.map_path)
        self.btn_choose = tk.Button(
            root,
            text='Загрузить данные',
            fg='black',
            padx="14", pady="7", font="13",
            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.render_pd,
        )
        self.btn_choose_save = tk.Button(
            root,
            text='Выбрать папку для сохранения отчетов',
            fg='black',
            padx="14", pady="7", font="13",
            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.render_phsv,
        )
        self.btn_get = tk.Button(
            root,
            text='Получить отчет',
            fg='black',
            padx="14", pady="7", font="13",
            highlightbackground='#66a5ad',
            activeforeground='green',
            activebackground='yellow',
            command=self.render_gt
        )
        # self.btn_choose.grid(rowspan=1, columnspan=1)
        # self.btn_get.grid(rowspan=1, columnspan=1)

        self.List_for_main_page = [
            self.btn_choose,
            self.btn_get,
            self.btn_choose_save
        ]

    def rendre_main_manu(self):
        # self.pd.delete_paste_data()
        self.btn_choose.pack(expand=1)
        self.btn_choose_save.pack(expand=1)
        self.btn_get.pack(expand=1)
        # self.btn_choose.grid(rowspan=1, columnspan=1)
        # self.btn_get.grid(rowspan=1, columnspan=1)

    def update_maim_manu(self):
        self.pd.delete_paste_data()
        self.gt.delete_get_table()
        self.phsv.delete_save_path()
        self.delete_main_menu()
        self.rendre_main_manu()

    def delete_main_menu(self):
        for i in self.List_for_main_page:
            # i.grid_forget()
            i.pack_forget()

    def render_pd(self):
        self.delete_main_menu()
        self.pd.rendre_paste_data()

    def render_gt(self):
        self.delete_main_menu()
        self.gt.rendre_get_table()

    def render_phsv(self):
        self.delete_main_menu()
        self.phsv.rendre_save_path()
