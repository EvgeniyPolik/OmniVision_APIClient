import threading
import PySimpleGUI as psg
import EventLog
import Graph
import IconsList
import RefreshForm
import ReqQuery
import RequestTimer

main_form = psg.Window('')
name_of_elements = {
                    'radio_btn_key': '-radio-',
                    'mode_key': '-mode-',
                    'bollerON_key': '-ON-',
                    'secutrity_key': '-security-',
                    'power_key': '-power-',
                    'status_key': '-status-',
                    'led_t1_key': '-t1-',
                    'led_t2_key': '-t2-',
                    'gazAlert_key': '-gaz-',
                    'fireAlert_key': '-fire-',
                    'pressure_key': '-p-',
                    'boller_error_key': '-error-'
                    }
mainFont = ()
offset = 0

status_of_image = {
                    'status_object': [],
                    'mode': [],
                    'boller': [],
                    'security': [],
                    'power': [],
                    'pressure': [],
                    'GAZ': [],
                    'fire': [],
                    'error': []
                    }
for i in range(10):  # Статусы объектов
    status_of_image['status_object'].append('g')
    status_of_image['mode'].append('s')
    status_of_image['boller'].append('on')
    status_of_image['error'].append('ok')
    status_of_image['security'].append('ok')
    status_of_image['power'].append('ok')
    status_of_image['pressure'].append('ok')
    status_of_image['GAZ'].append('ok')
    status_of_image['fire'].append('ok')


def mainform(db):
    global main_form, offset
    indicators = []
    right_mouse_menu = ['&Right',
                        ['Сброс аварии котла', 'Снятие/постановка на охрану', 'Переключение режима зима/лето']]
    for i in range(10):
        name_dict = RefreshForm.name_of_object(i)
        indicators.append(
            [psg.Radio(name_dict['name_object'] + '\n' + name_dict['city_object'] + name_dict['pnt'] +
                       name_dict['street_object'] + name_dict['pnt'] + name_dict['build_object'],
                       group_id=0, pad=(0, 0), size=(25, 2), font=mainFont,
                       key=name_of_elements['radio_btn_key'] + str(i),
                       disabled=name_dict['not_active'], right_click_menu=right_mouse_menu, enable_events=True),
             psg.Image(data=IconsList.statusGreen, key=name_of_elements['status_key'] + str(i), size=(10, 60)),
             psg.T('', size=(1, 1)),
             psg.Image(data=IconsList.ledNo, key=name_of_elements['led_t1_key'] + '0' + str(i)),
             psg.Image(data=IconsList.led0, key=name_of_elements['led_t1_key'] + '1' + str(i)),
             psg.Image(data=IconsList.led0, key=name_of_elements['led_t1_key'] + '2' + str(i)),
             psg.T('', size=(1, 1)),
             psg.Image(data=IconsList.ledNo, key=name_of_elements['led_t2_key'] + '0' + str(i)),
             psg.Image(data=IconsList.led0r, key=name_of_elements['led_t2_key'] + '1' + str(i)),
             psg.Image(data=IconsList.led0r, key=name_of_elements['led_t2_key'] + '2' + str(i)),
             psg.T('', size=(1, 1)),
             psg.Image(data=IconsList.summer, key=name_of_elements['mode_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.powerON, key=name_of_elements['bollerON_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.okIcon, key=name_of_elements['boller_error_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.okIcon, key=name_of_elements['secutrity_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.okIcon, key=name_of_elements['power_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.okIcon, key=name_of_elements['pressure_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.okIcon, key=name_of_elements['gazAlert_key'] + str(i), enable_events=True),
             psg.Image(data=IconsList.okIcon, key=name_of_elements['fireAlert_key'] + str(i), enable_events=True)
             ])
    # Левый столбец:
    left_column_var = [[psg.Button('', font=mainFont, size=(58, 1), key='-up-', image_data=IconsList.up),
                        psg.T('', font=mainFont, size=(5, 1)),
                        psg.T('T-воздуха:', font=mainFont, size=(15, 1)),
                        psg.T('T-Подачи:', font=mainFont, size=(13, 1)),
                        psg.T('Режим:', font=mainFont, size=(8, 1)),
                        psg.T('Котел:', font=mainFont, size=(7, 1)),
                        psg.T('Работа:', font=mainFont, size=(7, 1)),
                        psg.T('Охрана:', font=mainFont, size=(7, 1)),
                        psg.T('Питание:', font=mainFont, size=(7, 1)),
                        psg.T('Давление:', font=mainFont, size=(10, 1)),
                        psg.T('ГАЗ:', font=mainFont, size=(5, 1)),
                        psg.T('Пож Сигн:', font=mainFont, size=(8, 1))]
                       ]
    left_column_var.extend(indicators)
    left_column_var.extend([[psg.Button('', font=mainFont, size=(58, 1), key='-down-',
                                        image_data=IconsList.down)]])
    heads_on_table = ['Объект: ', 'Событие']
    items_in_table = [[]]
    right_column_var = [[psg.Image('', size=(35, 22))],  # Правый столбец элементов
                        [psg.Image('', size=(10, 1)), psg.Image(data=IconsList.allStatusYellow, size=(395, 30),
                                                                key='-state-')],
                        [psg.Image('', size=(10, 1)),
                         psg.Table(items_in_table, headings=heads_on_table, col_widths=[18, 21], key='-table_error-',
                                   auto_size_columns=False, num_rows=18, selected_row_colors=('black', '#5babd4'),
                                   alternating_row_color='#91f5fa', justification='l')]
                        ]
    mainmenu = [['Файл', ['Журнал событий', 'Графики', ['Часовой график', 'Суточный график']]]]

    main_form_var = [
        [psg.Menu(mainmenu)],
        [psg.Column(left_column_var), psg.Column(right_column_var, vertical_alignment="top")]
    ]

    main_form = psg.Window('OmniVision', main_form_var, size=(1360, 710), icon=IconsList.iconMainForm,
                           element_padding=0, finalize=True)

    for element in main_form.element_list():  # Принудительно выравнять текст у радиокнопки по левому краю
        if isinstance(element, psg.Radio):  # Если элемент принадлежит к радиокнопке
            element.bind('<Button-3>', ' +RIGHT CLICK+')  # Через Tkinter привязать ПКМ и Событие
            element.Widget.configure(justify='left', wraplength=300, height=2, anchor='w')

    RefreshForm.refresh_form()
    daemon_request = RequestTimer.timer
    automatic_request = threading.Thread(target=daemon_request)
    automatic_request.setDaemon(True)
    automatic_request.start()
    automatic_request.join(0.1)
    pos = None

    while True:
        main_form_event, main_form_value = main_form.read()
        if main_form_event == psg.WINDOW_CLOSED:
            break
        for i in range(10):
            if main_form_event == name_of_elements['radio_btn_key'] + str(i) + ' +RIGHT CLICK+':
                pos = i
        if main_form_event == 'Сброс аварии котла':
            ReqQuery.post_command(pos + offset, 2)

        if main_form_event == 'Снятие/постановка на охрану':
            ReqQuery.post_command(pos + offset, 1)

        if main_form_event == 'Переключение режима зима/лето':
            ReqQuery.post_command(pos + offset, 3)

        if main_form_event == '-up-':
            if offset > 0:
                offset -= 1
                RefreshForm.update_info_form()
                RefreshForm.refresh_form()

        if main_form_event == '-down-':
            if len(ReqQuery.catalog_bollers) > offset + 10:
                offset += 1
                RefreshForm.update_info_form()
                RefreshForm.refresh_form()

        if main_form_event == 'Журнал событий':
            EventLog.show_event_log(db)

        if main_form_event == 'Суточный график':
            Graph.do_graph('daily', db)

        if main_form_event == 'Часовой график':
            Graph.do_graph('horly', db)

    main_form.close()
