import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import PySimpleGUI as psg
from datetime import timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import MainForm
import ReqQuery

mpl.use('TkAgg')


def make_graph(canvas, axis_t1, axis_t2, axis_x):
    plt.rcParams['font.size'] = '8'
    fig = plt.figure(dpi=100)
    ind = [i for i in range(len(axis_x))]
    ax = plt.gca()
    ax.spines['bottom'].set_position('zero')  # выставим Ось на ноль
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    margins = {
        "left": 0.060,
        "bottom": 0.060,
        "right": 0.990,
        "top": 0.990
    }
    plt.subplots_adjust(**margins)  # применим поля
    plt.plot(ind, axis_t1, 'blue')  # Прорисовка графика
    plt.plot(ind, axis_t2, 'red')
    plt.xticks(ind, axis_x, rotation='vertical')
    plt.ylim(-35, 100)
    plt.xlim(0, 30)
    plt.figure()

    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0.5)
    plt.close('all')


def get_data(db, dates, tips, boller_id=0):
    cursor = db.cursor()
    list_of_date = []
    list_avr_t1 = []
    list_avr_t2 = []
    if tips == 'daily':
        start_day = datetime.datetime.strptime(dates, '%d.%m.%Y %H:%M:%S')
        end_day = start_day - timedelta(days=30)
        for i in range(31):
            day = (end_day + timedelta(days=i)).strftime('%d.%m.%Y')
            list_of_date.append(day) if i > 0 else list_of_date.append('')
            selectSQL = f'SELECT AVG(T1) as avg_t1, AVG(T2) as avg_t2 FROM HOUR_TABLE ' \
                            f'WHERE DI_DATE = \'{day}\' AND DI_KOT = {boller_id}'
            cursor.execute(selectSQL)
            tmp = cursor.fetchall()[0]
            if tmp[0] is None:
                list_avr_t1.append(0)
            else:
                list_avr_t1.append(round(float(tmp[0]), 2))
            if tmp[1] is None:
                list_avr_t2.append(0)
            else:
                list_avr_t2.append(round(float(tmp[1]), 2))
    else:  # Часовой график
        start_day = datetime.datetime.strptime(dates, '%d.%m.%Y %H:%M:%S')
        day = (start_day).strftime('%d.%m.%Y')
        selectSQL = f'SELECT * FROM (SELECT ID_DI, T1, T2, DI_DATE, DI_TIME FROM HOUR_TABLE WHERE DI_KOT = {boller_id} AND ' \
                    f'DI_DATE <= \'{day}\' ORDER BY ID_DI DESC ROWS 1 TO 31) ORDER BY ID_DI'
        cursor.execute(selectSQL)
        tmp = cursor.fetchall()
        lenght_of_SQL = len(tmp)
        correction_set = 31 - lenght_of_SQL
        for i in range(31):
            if lenght_of_SQL >= 31 or (lenght_of_SQL + i) >= 31:
                count_correction = i - correction_set
                list_avr_t1.append(tmp[count_correction][1])
                list_avr_t2.append(tmp[count_correction][2])
                list_of_date.append(str(tmp[count_correction][4])[0:3] + '00') if i > 0 else list_of_date.append('')
            else:
                list_avr_t1.append(0)
                list_avr_t2.append(0)
                list_of_date.append('нет данных') if i > 0 else list_of_date.append('')
    cursor.close()
    return list_avr_t1, list_avr_t2, list_of_date


def do_graph(tips, db, id_item=0, on_day=datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")):
    if tips == 'daily':
        header = 'Суточный график на: '
    else:
        header = 'Часовой график на:'
    items = []
    id_of_items = {}
    not_empty = False
    def_value = ''

    if len(ReqQuery.catalog_bollers) > 0:
        not_empty = True
        for item in ReqQuery.catalog_bollers:
            items.append(item['Properties'][0].strip())
            id_of_items[item['Properties'][0].strip()] = item['Id']
            if item['Id'] == id_item and id_item != 0:
                def_value = item['Properties'][0].strip()
        if id_item == 0:
            def_value = items[0]

    layout = [[psg.Text(header, font=MainForm.mainFont), psg.Text(on_day[0:10], key='-show_date-'),
               psg.InputText(on_day, key='-choosen_date-', visible=False, enable_events=True),
               psg.CalendarButton('Выбрать дату', target='-choosen_date-', format='%d.%m.%Y 23:50:00'),
               psg.Text('Объект', font=('Segoe UI', 10, 'bold')),
               psg.Combo(items, key='-object-', size=(20, 1), default_value=def_value),
               psg.Button('Применить', key='-apply-')],
              [psg.Canvas(size=(800, 600), key='-canvas-')],
              [psg.Push(), psg.Button('Закрыть', key='-close-')]]

    graph_form = psg.Window('График', layout, finalize=True, modal=True)
    if not_empty:
        t1, t2, x = get_data(db, on_day, tips, id_of_items[def_value])
    else:
        t1, t2, x = get_data(db, on_day, tips, -1)
    make_graph(graph_form['-canvas-'].TKCanvas, t1, t2, x)
    reopen = False

    while True:
        event, value = graph_form.Read()
        if event in (psg.WINDOW_CLOSED, '-close-'):
            break
        if event == '-choosen_date-':
            graph_form['-show_date-'].Update(value['-choosen_date-'][0:10])
        if event == '-apply-':
            reopen = True
            id_item = id_of_items[value['-object-']]
            if value['-choosen_date-'][0:10] == datetime.datetime.today().strftime("%d.%m.%Y"):
                new_date = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
            else:
                new_date = value['-choosen_date-']
            break
    graph_form.close()
    if reopen:
        do_graph(tips, db, id_item, new_date)
