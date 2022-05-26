import threading

import PySimpleGUI as Psg
import IconsList
import RefreshForm
import ReqQuery
import RequestTimer

main_form = Psg.Window('')
radio_btn_key = '-radio-'
mode_key = '-mode-'
bollerON_key = '-ON-'
secutrity_key = '-security-'
power_key = '-power-'
status_key = '-status-'
led_t1_key = '-t1-'
led_t2_key = '-t2-'
gazAlert_key = '-gaz-'
fireAlert_key = '-fire-'
pressure_key = '-p-'
boller_error_key = '-error-'
mainFont = ('Segoe UI', 10, 'bold')

status_of_image = {
                    'status_object': [],
                    'mode': [],
                    'boller': [],
                    'security': [],
                    'power': [],
                    'pressure': [],
                    'GAZ': [],
                    'fire': [],
                    'error': [],
                    'all': ['g']
                    }
for i in range(10):
    status_of_image['status_object'].append('g')
    status_of_image['mode'].append('s')
    status_of_image['boller'].append('on')
    status_of_image['error'].append('ok')
    status_of_image['security'].append('ok')
    status_of_image['power'].append('ok')
    status_of_image['pressure'].append('ok')
    status_of_image['GAZ'].append('ok')
    status_of_image['fire'].append('ok')


def mainform():
    global main_form
    indicators = []
    for i in range(10):
        name_dict = RefreshForm.name_of_object(i)
        indicators.append(
            [Psg.Radio(name_dict['name_object'] + '\n' + name_dict['city_object'] + name_dict['pnt'] +
                       name_dict['street_object'] + name_dict['pnt'] + name_dict['build_object'],
                       group_id=0, pad=(0, 0), size=(25, 2), font=mainFont, key=radio_btn_key + str(i),
                       disabled=name_dict['not_active']),
             Psg.Image(data=IconsList.statusGreen, key=status_key + str(i), size=(10, 60)),
             Psg.T('', size=(1, 1)),
             Psg.Image(data=IconsList.ledNo, key=led_t1_key + '0' + str(i)),
             Psg.Image(data=IconsList.led0, key=led_t1_key + '1' + str(i)),
             Psg.Image(data=IconsList.led0, key=led_t1_key + '2' + str(i)),
             Psg.T('', size=(1, 1)),
             Psg.Image(data=IconsList.ledNo, key=led_t2_key + '0' + str(i)),
             Psg.Image(data=IconsList.led0r, key=led_t2_key + '1' + str(i)),
             Psg.Image(data=IconsList.led0r, key=led_t2_key + '2' + str(i)),
             Psg.T('', size=(1, 1)),
             Psg.Image(data=IconsList.summer, key=mode_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.powerON, key=bollerON_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=boller_error_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=secutrity_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=power_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=pressure_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=gazAlert_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=fireAlert_key + str(i), enable_events=True)
             ])

    left_column_var = [[Psg.T('Наименование объекта:', font=mainFont, size=(33, 1)),  # Левый столбец элементов
                        Psg.T('T-воздуха:', font=mainFont, size=(15, 1)),
                        Psg.T('T-Подачи:', font=mainFont, size=(13, 1)),
                        Psg.T('Режим:', font=mainFont, size=(8, 1)),
                        Psg.T('Котел:', font=mainFont, size=(7, 1)),
                        Psg.T('Работа:', font=mainFont, size=(7, 1)),
                        Psg.T('Охрана:', font=mainFont, size=(7, 1)),
                        Psg.T('Питание:', font=mainFont, size=(7, 1)),
                        Psg.T('Давление:', font=mainFont, size=(10, 1)),
                        Psg.T('ГАЗ:', font=mainFont, size=(5, 1)),
                        Psg.T('Пож Сигн:', font=mainFont, size=(8, 1))]
                       ]
    left_column_var.extend(indicators)
    heads_on_table = ['Объект: ', 'Событие']
    items_in_table = [['Каменнозерское СОШ', 'Отсутствует эл. питание']]
    right_column_var = [[Psg.Image('', size=(35, 22))],                    # Правый столбец элементов
                        [Psg.Image('', size=(10, 1)), Psg.Image(data=IconsList.allStatusYellow, size=(395, 30),
                                                                key='-state-')],
                        [Psg.Image('', size=(10, 1)),
                         Psg.Table(items_in_table, headings=heads_on_table, col_widths=[16, 18], key='-table_error-',
                                   auto_size_columns=False, num_rows=18, selected_row_colors=('black', '#5babd4'),
                                   alternating_row_color='#91f5fa')]
                        ]
    mainmenu = [['Файл', ['Журнал событий']]]
    main_form_var = [
        [Psg.Menu(mainmenu)],
        [Psg.Column(left_column_var), Psg.Column(right_column_var, vertical_alignment="top")]
    ]

    main_form = Psg.Window('OmniVision', main_form_var, size=(1360, 680), icon=IconsList.iconMainForm,
                           element_padding=0, finalize=True)

    for element in main_form.element_list():  # Принудительно выравнять текст у радиокнопки по левому краю
        if isinstance(element, Psg.Radio):
            element.Widget.configure(justify='left', wraplength=300, height=2, anchor='w')

    RefreshForm.refresh_form()
    daemon_request = RequestTimer.timer
    AutomaticRequest = threading.Thread(target=daemon_request)
    AutomaticRequest.setDaemon(True)
    AutomaticRequest.start()
    AutomaticRequest.join(0.5)
    while True:
        main_form_event, main_form_value = main_form.read()
        if main_form_event == Psg.WINDOW_CLOSED:
            break

    main_form.close()
