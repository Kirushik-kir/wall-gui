from os import getcwd

import PySimpleGUI as sg
from layouts import radios_p, get_rows
from numpy import cos, sin, pi, sqrt

from vars import pics

# Определение массива переменных и их начальных значений
p = d = d0 = alpha = h = sigma = 0
c11 = c12 = c21 = c22 = 0
srr = sr = 0  # result
crit = crit1 = crit2 = crit3 = 0
checkcrit = False
last_index = -1
prefix = 0


def configure_canvas(event, canvas, frame_id):
    canvas.itemconfig(frame_id, width=canvas.winfo_width())


def configure_frame(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def get_name(id):
    if id == 0: return 'Цилиндрическая обечайка'
    if id == 1: return 'Коническая обечайка'
    if id == 2: return 'Эллиптическое днище'
    if id == 3: return 'Полусферическое днище'
    if id == 4: return 'Цилиндрический(ая) коллектор, штуцер, труба или колено'

def new_rows(id):
    global last_index
    global prefix

    if last_index != -1:
        if window[('Frame', prefix)].Widget:
            widget = window[('Frame', prefix)].Widget
            del window.AllKeysDict[('Frame', prefix)]
            delete_widget(widget.master)

    last_index = id
    prefix += 1
    return [[sg.Frame("", [[sg.T(get_name(id))], get_rows(prefix, id)], key=('Frame', prefix),
                      visible=(prefix != 1))]]


layout = [
    [sg.Text('Название расчета')],
    [sg.InputText(key='name_of_count', expand_x=True)],
    [sg.Column(radios_p, size=(200, 200), pad=((0, 0), (30, 0)))],  # Группа радио-кнопок
    [sg.Column(new_rows(0), pad=((10, 30), (10, 0)), expand_y=True, key='-COL-'), sg.Image(key='-PIC-', pad=((50, 0), (0, 200)))],
    [sg.Button('OK', pad=((10, 0), (0, 50))), sg.Button('Выход', pad=((1300, 0), (0, 50)))]
    # Кнопки "OK" и "Выход" внизу
]

# Создание окна с размерами экрана
window = sg.Window('расчет по выбору толщины стенок обоорудования', layout, size=(1500, 850), resizable=True,
                   margins=(0, 0), finalize=True)

#frame_id = window['-COL-'].Widget.frame_id
#frame = window['-COL-'].Widget.TKFrame
#canvas = window['-COL-'].Widget.canvas
#canvas.bind("<Configure>", lambda event, canvas=canvas, frame_id=frame_id: configure_canvas(event, canvas, frame_id))
#frame.bind("<Configure>", lambda event, canvas=canvas: configure_frame(event, canvas))


def delete_widget(widget):
    children = list(widget.children.values())
    for child in children:
        delete_widget(child)
    widget.pack_forget()
    widget.destroy()
    del widget


# Обработка цилиндрической обечайки
def cil_ob():
    global p, d, sigma, c11, c12, c21, c22, d0, alpha, h
    global checkcrit, srr, sr, crit
    fi = 1

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
    global p, d, sigma, c11, c12, c21, c22, d0, alpha, h
    global checkcrit, srr, sr, crit1, crit2, crit3
    fi = 1

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
    global p, d, sigma, c11, c12, c21, c22, d0, alpha, h
    global checkcrit, srr, sr, crit1, crit2
    fi = 1

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
    global p, d, sigma, c11, c12, c21, c22, d0, alpha, h
    global checkcrit, srr, sr, crit
    fi = 1

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
        return cil_ob()
    elif selected_item == 1:
        return kon_ob()
    elif selected_item == 2:
        return elliptic_dno()
    elif selected_item == 3:
        return semispheric_dno()
    elif selected_item == 4:
        return long_hren()
    return 0


# Цикл обработки событий
selected_id = -1
flag = False


def validate(selected_id):
    global p, d, sigma, c11, c12, c21, c22, d0, alpha, h
    assert selected_id <= 4 or selected_id >= 0, 'The selected item did not get into the scope [0, 4]'
    if selected_id == 0:
        if not all((values[f"input_{prefix}-{i}"] for i in range(7))): return 0

        p = float(values[f"input_{prefix}-0"])
        d = float(values[f"input_{prefix}-1"])
        sigma = float(values[f"input_{prefix}-2"])
        c11 = float(values[f"input_{prefix}-3"])
        c12 = float(values[f"input_{prefix}-4"])
        c21 = float(values[f"input_{prefix}-5"])
        c22 = float(values[f"input_{prefix}-6"])
    elif selected_id == 1:
        if not all((values[f"input_{prefix}-{i}"] for i in range(9))): return 0

        p = float(values[f"input_{prefix}-0"])
        d = float(values[f"input_{prefix}-1"])
        d0 = float(values[f"input_{prefix}-2"])
        alpha = float(values[f"input_{prefix}-3"])
        sigma = float(values[f"input_{prefix}-4"])
        c11 = float(values[f"input_{prefix}-5"])
        c12 = float(values[f"input_{prefix}-6"])
        c21 = float(values[f"input_{prefix}-7"])
        c22 = float(values[f"input_{prefix}-8"])
    elif selected_id == 2:
        if not all((values[f"input_{prefix}-{i}"] for i in range(8))): return 0
        p = float(values[f"input_{prefix}-0"])
        d = float(values[f"input_{prefix}-1"])
        h = float(values[f"input_{prefix}-2"])
        sigma = float(values[f"input_{prefix}-3"])
        c11 = float(values[f"input_{prefix}-4"])
        c12 = float(values[f"input_{prefix}-5"])
        c21 = float(values[f"input_{prefix}-6"])
        c22 = float(values[f"input_{prefix}-7"])
    elif selected_id == 3:
        if not all((values[f"input_{prefix}-{i}"] for i in range(7))): return 0

        p = float(values[f"input_{prefix}-0"])
        d = float(values[f"input_{prefix}-1"])
        sigma = float(values[f"input_{prefix}-2"])
        c11 = float(values[f"input_{prefix}-3"])
        c12 = float(values[f"input_{prefix}-4"])
        c21 = float(values[f"input_{prefix}-5"])
        c22 = float(values[f"input_{prefix}-6"])
    elif selected_id == 4:
        if not all((values[f"input_{prefix}-{i}"] for i in range(7))): return 0

        p = float(values[f"input_{prefix}-0"])
        d = float(values[f"input_{prefix}-1"])
        sigma = float(values[f"input_{prefix}-2"])
        c11 = float(values[f"input_{prefix}-3"])
        c12 = float(values[f"input_{prefix}-4"])
        c21 = float(values[f"input_{prefix}-5"])
        c22 = float(values[f"input_{prefix}-6"])
    return 1


while True:
    event, values = window.read()
    print(event, values)
    if event == 'Выход' or event == sg.WIN_CLOSED:
        break
    elif event == 'OK':
        if selected_id != -1:
            if validate(selected_id):
                count(selected_id)
                if not checkcrit:
                    #sg.popup('Результат:', srr)
                    critik = ''
                    if selected_id in {0, 3}:
                        critik = f"c = {crit}"
                    elif selected_id == 1:
                        critik = f"c1 = {crit1}" + f" c1 = {crit2}" + f" c1 = {crit3}"
                    elif selected_id == 2:
                        critik = f"c1 = {crit1}" + f" c1 = {crit2}"
                    window2 = sg.Window('расчет по выбору толщины стенок обоорудования', [[sg.T(f" Результат с учётом допусков: {srr}\n Результат без учёта допусков: {sr}\n Результат проверки критерия применимости формулы: {critik}")]], size=(600, 150), margins=(0, 0), finalize=True)
                else:
                    sg.popup('Критический показатель проверки!')
            else:
                sg.popup('Пожалуйста, введите все данные')
        else:
            sg.popup('Пожалуйста, выберите вид рассчета')

    elif event and event.startswith('input_'):
        print(".!.")
        # Обработка ввода в полях
        input_key = event
        input_value = values[input_key]

        # Проверяем ввод на допустимые символы (цифры и минус)
        if input_value and not all(char.isdigit() or char in ['-', '.'] for char in input_value):
            # Если ввод содержит что-то кроме цифр, минуса и точки, очищаем поле ввода
            window[input_key].update('')

            sg.popup('Пожалуйста, введите только цифры и знак минус')

    elif event and event.startswith('Radio_'):
        selected_id = int(event[-1])
        curdir = getcwd()
        cwd = curdir + pics[selected_id]
        print(cwd)
        window['-PIC-'].update(source=cwd)
        window.extend_layout(window['-COL-'], rows=new_rows(selected_id))

# Закрытие окна
window.close()