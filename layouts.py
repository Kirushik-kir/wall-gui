import PySimpleGUI as sg
from vars import GlblVarList

# Определение макета (layout) интерфейса
names = ['Цилиндрическая обечайка', 'Коническая обечайка', 'Эллиптическое днище', 'Полусферическое днище', 'Цилиндрический(ая) коллектор, \n штуцер, труба', 'Колено']
radios_p = [[sg.Radio(name, 'RADIOp', key=f'Radio_{i}', enable_events=True)] for i, name in enumerate(names)]

def get_rows(prefix, id):
    return [
        [sg.Text(field_name, size=(72, 1)), sg.Text('', size=(1, 1)),
         sg.InputText(key=f'input_{prefix}-{index}', enable_events=True, size=10)] for index, field_name in enumerate(GlblVarList[id])
    ]

def get_menu():
    layout = [
        [sg.Text('Выберите вид рассчета')],
        [sg.Button('Толщина стенки', pad=((10, 0), (20, 10)))],
        [sg.Button('Толщина крышки', pad=((10, 0), (0, 10)))],
        [sg.Button('Крепеж', pad=((10, 0), (0, 10)))],
        [sg.Button('OK', pad=((10, 0), (30, 10))), sg.Button('Выход', pad=((50, 0), (30, 10)))]
        # Кнопки "OK" и "Выход" внизу
    ]

    # Создание окна с размерами экрана
    window = sg.Window('Выбор рассчета', layout, size=(250, 220), resizable=True,
                       margins=(0, 0), finalize=True)
    return window