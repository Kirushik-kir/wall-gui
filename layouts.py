import PySimpleGUI as sg
from vars import GlblVarList

#TODO key и enable_events=True

# Определение макета (layout) интерфейса
names = ['Цилиндрическая обечайка', 'Коническая обечайка', 'Эллиптическое днище', 'Полусферическое днище', 'Цилиндрический(ая) \n коллектор, штуцер, \n труба или колено']
radios_p = [[sg.Radio(name, 'RADIOp', key=f'Radio_{i}', enable_events=True)] for i, name in enumerate(names)]

rows = [
[

    [sg.Text(field_name, size=(40, 1)), sg.Text('', size=(1, 1)),
     sg.InputText(key=f'input_{index}', enable_events=True)] for index, field_name in enumerate(GlblVarList[0])
         ],

[
    [sg.Text(field_name, size=(40, 1)), sg.Text('', size=(1, 1)),
     sg.InputText(key=f'input_{index}', enable_events=True)] for index, field_name in enumerate(GlblVarList[1])
         ],

[
    [sg.Text(field_name, size=(40, 1)), sg.Text('', size=(1, 1)),
     sg.InputText(key=f'input_{index}', enable_events=True)] for index, field_name in enumerate(GlblVarList[2])
         ],
[
    [sg.Text(field_name, size=(40, 1)), sg.Text('', size=(1, 1)),
     sg.InputText(key=f'input_{index}', enable_events=True)] for index, field_name in enumerate(GlblVarList[3])
         ],
[
    [sg.Text(field_name, size=(40, 1)), sg.Text('', size=(1, 1)),
     sg.InputText(key=f'input_{index}', enable_events=True)] for index, field_name in enumerate(GlblVarList[4])
         ]
 ]

pre_layout = [
    [sg.Text('Название расчета')],
    [sg.InputText(key='name_of_count', expand_x=True)],
    [sg.Column(radios_p, size=(200, 200), pad=((0, 0), (30, 0)))],  # Группа радио-кнопок

    [sg.Col([
        [sg.Frame('Frame 0', [[sg.T('Frame')], rows[0]], key='Frame_0', visible=False)],
        [sg.Frame('Frame 1', [[sg.T('Frame')], rows[1]], key='Frame_1', visible=False)],
        [sg.Frame('Frame 2', [[sg.T('Frame')], rows[2]], key='Frame_2', visible=False)],
        [sg.Frame('Frame 3', [[sg.T('Frame')], rows[3]], key='Frame_3', visible=False)],
        [sg.Frame('Frame 4', [[sg.T('Frame')], rows[4]], key='Frame_4', visible=False)]
    ], scrollable=True, key='-COL-', expand_x=True, expand_y=True)],

    [sg.Button('OK', pad=((0, 0), (250, 0))), sg.Button('Выход', pad=((1300, 0), (250, 0)))]  # Кнопки "OK" и "Выход" внизу
]