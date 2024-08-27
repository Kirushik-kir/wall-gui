import PySimpleGUI as sg
from vars import GlblVarList

# Определение макета (layout) интерфейса
names = ['Цилиндрическая обечайка', 'Коническая обечайка', 'Эллиптическое днище', 'Полусферическое днище', 'Цилиндрический(ая) коллектор, \n штуцер, труба', 'Колено']
radios_p = [[sg.Radio(name, 'RADIOp', key=f'Radio_{i}', enable_events=True)] for i, name in enumerate(names)]

def get_rows(prefix, id):
    return [
        [sg.Text(field_name, size=(40, 1)), sg.Text('', size=(1, 1)),
         sg.InputText(key=f'input_{prefix}-{index}', enable_events=True)] for index, field_name in enumerate(GlblVarList[id])
    ]