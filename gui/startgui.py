#coding=utf-8

from tkinter import Button, Tk, BOTTOM

from gui.startmenu import *


def main():
    root = Tk()
    mm = MainMenu(root)
    mm.rendre_main_manu()
    go_mm_button = Button(
        root,
        text='В главное меню',
        fg='black',
        padx="14", pady="7", font="13",
        highlightbackground='#66a5ad',
        activeforeground='green',
        activebackground='yellow',
        command=mm.update_maim_manu
    )
    go_mm_button.pack(side=BOTTOM)
    root.geometry("1200x900")

    root.mainloop()

if __name__ == '__main__':
    main()