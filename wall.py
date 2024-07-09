import PySimpleGUI as sg
from layouts import pre_layout, rows
from numpy import cos, sin, pi, sqrt

# Определение массива переменных и их начальных значений
p = d = d0 = alpha = h = sigma = None
c11 = c12 = c21 = c22 = 0

# Создание окна с размерами экрана
window = sg.Window('расчет по выбору толщины стенок обоорудования', pre_layout, size=(1500, 850))

def delete_widget(widget):
    children = list(widget.children.values())
    for child in children:
        delete_widget(child)
    widget.pack_forget()
    widget.destroy()
    del widget

# Обработка цилиндрической обечайки
def cil_ob():
    fi = 1
    checkcrit = False
    global OutDF

    print('Цилиндрическая обечайка')
    m1 = 2
    m2 = 1
    m3 = 1

    sr = (p * d * m3) / (m1 * (m2 * fi * sigma - p))
    srr = round(sr, 2)

    crit = sr / d

    print(crit)

    if crit > .3:
        print('fail!')
        checkcrit = True


# Обработка конической обечайки
def kon_ob():
    fi = 1
    checkcrit = False
    global OutDF

    print('Коническая обечайка')
    m1 = 2
    m2 = cos(alpha * pi / 180)
    m3 = 1

    sr = (p * d * m3) / (m1 * (m2 * fi * sigma - p))
    srr = round(sr, 2)

    crit1 = sr / d
    crit2 = d0 / d
    crit3 = 1 - (2 * sqrt(crit1 + crit1 ** 2) * sin(alpha * pi / 180)) / (sqrt(cos(alpha * pi / 180)))

    print(crit1, crit2, crit3)

    if (crit1 < 0.005) or (crit1 > .1) or (alpha > 45):
        print('fail!')
        checkcrit = True
    elif (crit2 > crit3) or (alpha > 45):
        print('fail!')
        checkcrit = True


# Обработка эллиптического днища
def elliptic_dno():
    fi = 1
    checkcrit = False
    global OutDF

    print('Эллиптическое днище')
    m1 = 4
    m2 = 1
    m3 = 0.5 * d / h

    sr = (p * d * m3) / (m1 * (m2 * fi * sigma - p))
    srr = round(sr, 2)

    crit1 = sr / d
    crit2 = h / d

    print(crit1, crit2)

    if (crit1 < 0.0025) or (crit1 > 0.1) or (crit2 < 0.2) or (crit2 > 0.5):
        print('fail!')
        checkcrit = True


# Обработка цилиндрической обечайки
def semispheric_dno():
    fi = 1
    checkcrit = False
    global OutDF

    print('Полусферическое днище')
    m1 = 4
    m2 = 1
    m3 = 1

    sr = (p * d * m3) / (m1 * (m2 * fi * sigma - p))
    srr = round(sr, 2)

    crit = sr / d

    print(crit)


# Цилиндрический(ая) \n коллектор, штуцер, \n труба или колено
def long_hren():
    print('ne sdelano poka')
    return True

def count(selected_item):
    if selected_item == 0:
        cil_ob()
    elif selected_item == 1:
        kon_ob()
    elif selected_item == 2:
        elliptic_dno()
    elif selected_item == 3:
        semispheric_dno()
    elif selected_item == 4:
        long_hren()


# Цикл обработки событий
selected_id = -1
flag = False


def validate(selected_id):
    assert selected_id <= 4 or selected_id >= 0, 'The selected item did not get into the scope [0, 4]'
    if selected_id == 0:
        p = int(values['input_0'])
        d = int(values['input_1'])
        sigma = int(values['input_2'])
        c11 = int(values['input_3'])
        c12 = int(values['input_4'])
        c21 = int(values['input_5'])
        c22 = int(values['input_6'])
    elif selected_id == 1:
        p = int(values['input_0'])
        d = int(values['input_1'])
        d0 = int(values['input_2'])
        alpha = int(values['input_3'])
        sigma = int(values['input_4'])
        c11 = int(values['input_5'])
        c12 = int(values['input_6'])
        c21 = int(values['input_7'])
        c22 = int(values['input_8'])
    elif selected_id == 2:
        p = int(values['input_0'])
        d = int(values['input_1'])
        h = int(values['input_2'])
        sigma = int(values['input_3'])
        c11 = int(values['input_4'])
        c12 = int(values['input_5'])
        c21 = int(values['input_6'])
        c22 = int(values['input_7'])
    elif selected_id == 3:
        p = int(values['input_0'])
        d = int(values['input_1'])
        sigma = int(values['input_2'])
        c11 = int(values['input_3'])
        c12 = int(values['input_4'])
        c21 = int(values['input_5'])
        c22 = int(values['input_6'])
    elif selected_id == 4:
        p = int(values['input_0'])
        d = int(values['input_1'])
        sigma = int(values['input_2'])
        c11 = int(values['input_3'])
        c12 = int(values['input_4'])
        c21 = int(values['input_5'])
        c22 = int(values['input_6'])

while True:
    event, values = window.read()
    print(values)
    if event == sg.WIN_CLOSED or event == 'Выход':
        break
    elif event == 'OK':
        if selected_id != -1:
            validate(selected_id)
            count(selected_id)
        else:
            sg.popup('Пожалуйста, выберите вид рассчета')

    elif event.startswith('input_'):
        # Обработка ввода в полях
        input_key = event
        input_value = values[input_key]

        # Проверяем ввод на допустимые символы (цифры и минус)
        if input_value and not input_value.lstrip('-').isdigit():
            # Если ввод содержит что-то кроме цифр и минуса, очищаем поле ввода
            window[input_key].update('')

            sg.popup('Пожалуйста, введите только цифры и знак минус')

    elif event.startswith('Radio_'):
        selected_id = int(event[-1])
        for i in range(0, 5):
            if i != selected_id:
                window[f"Frame_{i}"].update(visible=False)
                window.visibility_changed()
                window['-COL-'].contents_changed()
        window[f"Frame_{selected_id}"].update(visible=True)
        window.visibility_changed()
        window['-COL-'].contents_changed()
# Закрытие окна
window.close()






# """
#     Demonstrates how to use the Window.layout_extend method.
#     Layouts can be extended at the Window level or within any container element such as a Column.
#     This demo shows how to extend both.
#     Note that while you can extend, add to, a layout, you cannot delete items from a layout.  Of course you
#     can make them invisible after adding them.
#
#     When using scrollable Columns be sure and call Column.visibility_changed so that the scrollbars will
#         be correctly reposititioned
#
#     Copyright 2020-2023 PySimpleSoft, Inc. and/or its licensors. All rights reserved.
#
#     Redistribution, modification, or any other use of PySimpleGUI or any portion thereof is subject to the terms of the PySimpleGUI License Agreement available at https://eula.pysimplegui.com.
#
#     You may not redistribute, modify or otherwise use PySimpleGUI or its contents except pursuant to the PySimpleGUI License Agreement.
# """
#
# layout = [[sg.Text('My Window')],
#           [sg.Text('Click to add a row inside the Frame'), sg.B('+', key='-ADD FRAME-')],
#           [sg.Text('Click to add a row inside the Column'), sg.B('+', key='-ADD COL-')],
#           [sg.Text('Click to add a row inside the Window'), sg.B('+', key='-ADD WIN-')],
#           [sg.Frame('Frame', [[sg.T('Frame')]], key='-FRAME-')],
#           [sg.Col([[sg.T('Column')]], scrollable=True, key='-COL-', s=(400, 400))],
#           [sg.Input(key='-IN-'), sg.Text(size=(12, 1), key='-OUT-')],
#           [sg.Button('Button'), sg.Button('Exit')]]
#
# window = sg.Window('Window Title', layout)
#
# i = 0
#
# while True:  # Event Loop
#     event, values = window.read()
#     print(event, values)
#     if event in (sg.WIN_CLOSED, 'Exit'):
#         break
#     if event == '-ADD FRAME-':
#         window.extend_layout(window['-FRAME-'], rows[i])
#         i += 1
#     elif event == '-ADD COL-':
#         window.extend_layout(window['-COL-'], [[sg.T('A New Input Line'), sg.I(key=f'-IN-{i}-')]])
#         window.visibility_changed()
#         window['-COL-'].contents_changed()
#         i += 1
#     elif event == '-ADD WIN-':
#         window.extend_layout(window, [[sg.T('A New Input Line'), sg.I(key=f'-IN-{i}-')]])
#         i += 1
# window.close()









#
# def configure_canvas(event, canvas, frame_id):
#     canvas.itemconfig(frame_id, width=canvas.winfo_width())
#
# def configure_frame(event, canvas):
#     canvas.configure(scrollregion=canvas.bbox("all"))
#
#
#
# def new_rows():
#     global index
#     index += 1
#     layout_frame = [[sg.Text("Hello World"), sg.Push(), sg.Button('Delete', key=('Delete', index))]]
#     return [[sg.Frame(f"Frame {index:0>2d}", layout_frame, expand_x=True, key=('Frame', index))]]
#
# index = 0
#
# layout = [
#     [sg.Button("Add")],
#     [sg.Column(new_rows(), scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, key='Scrollable Column')]
# ]
#
# window = sg.Window("Title", layout, resizable=True, margins=(0, 0), finalize=True)
#
# frame_id = window['Scrollable Column'].Widget.frame_id
# frame = window['Scrollable Column'].Widget.TKFrame
# canvas = window['Scrollable Column'].Widget.canvas
# canvas.bind("<Configure>", lambda event, canvas=canvas, frame_id=frame_id:configure_canvas(event, canvas, frame_id))
# frame.bind("<Configure>", lambda event, canvas=canvas:configure_frame(event, canvas))
#
# window.maximize()
#
# while True:
#
#     event, values = window.read()
#
#     if event in ('Close', sg.WIN_CLOSED):
#         break
#     elif event == 'Add':
#         window.extend_layout(window['Scrollable Column'], rows=new_rows())
#     elif event[0] == 'Delete':
#         i = event[1]
#         widget = window[('Frame', i)].Widget
#         del window.AllKeysDict[('Frame', i)]
#         delete_widget(widget.master)
# window.close()