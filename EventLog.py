import PySimpleGUI as psg
import datetime


def get_catalog_event(on_date, db):
    fb_cursor = db.cursor()
    selectSQL = f'SELECT E_TIME, NAM_K, E_TEXT FROM EVENET_LOG LEFT JOIN KOT ON ID_K = E_KOT WHERE E_DATE = \'{on_date}\''
    fb_cursor.execute(selectSQL)
    result_list = []
    for row in fb_cursor.itermap():
        tmp = []
        tmp.append(row['E_TIME'])
        tmp.append(row['NAM_K'])
        tmp.append(row['E_TEXT'])
        result_list.append(tmp)
    if len(result_list) == 0:
        result_list.append(['', '', 'Нет событий на выбранную дату'])
    fb_cursor.close()
    return result_list

def show_event_log(db):
    today = datetime.datetime.today().strftime("%d.%m.%Y")
    catalog_event = get_catalog_event(today,db)
    layout = [[psg.Text('Журнал событий на: '),
               psg.Text(str(today), key='-on_date-'),
               psg.CalendarButton('Выбрать', target='-choosen_date-', format="%d.%m.%Y"),
               psg.InputText(str(today), key='-choosen_date-', enable_events=True, visible=False)],
              [psg.Table(catalog_event, headings=['Время', 'Объект', 'Событие'], col_widths=[7, 18, 43],
                         size=(495, 630), selected_row_colors=('black', '#D3C4C4'), num_rows=32, key='-event_table-',
                         auto_size_columns=False, justification='l')],
              [psg.Push(), psg.Button('Закрыть', key='-close-', size=(15, 1)), psg.Push()]
              ]

    event_log_form = psg.Window('Журнал событий', layout, modal=True, size=(590, 650), finalize=True)

    while True:
        event, value = event_log_form.read()

        if event == psg.WINDOW_CLOSED or event == '-close-':
            break

        if event == '-choosen_date-':
            event_log_form['-on_date-'].Update(value['-choosen_date-'])
            catalog_event = get_catalog_event(value['-choosen_date-'], db)
            event_log_form['-event_table-'].Update(catalog_event)

    event_log_form.close()