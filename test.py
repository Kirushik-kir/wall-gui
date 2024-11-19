from os import getcwd

import PySimpleGUI as sg
from layouts import radios_p, get_rows, get_menu
from numpy import cos, sin, pi, sqrt
from math import ceil
from tkinter.filedialog import asksaveasfilename
import pandas as pd


from vars import pics
from vars import GlblVarList

menu = get_menu()

layout = [
    [sg.Text('Название расчета')],
    [sg.InputText(key='name_of_count', expand_x=True)],
    [sg.Column(radios_p, size=(250, 200), pad=((0, 0), (30, 0))), sg.Image(key='-PIC-', pad=((50, 0), (50, 0)))],  # Группа радио-кнопок
    [sg.Button('OK', pad=((10, 0), (0, 10))), sg.Button('Выход', pad=((1100, 0), (0, 10)))]
    # Кнопки "OK" и "Выход" внизу
]
window = None
while True:
    if window:
        event, values = window.read()
    else:
        event, values = menu.read()
    if event == "Толщина стенки":
        window = sg.Window('Расчет по выбору толщины стенок оборудования', layout, size=(1300, 725), resizable=True,        #240909 - исправил опечатки в названии окна
                   margins=(0, 0), finalize=True)
        window.read()
        menu.close()
    elif event == sg.WIN_CLOSED or "Выход":
        break
if window:
    window.close()