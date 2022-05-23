import PySimpleGUI as Psg
import IconsList

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
mainFont = ('Segoe UI', 10, 'bold')

def mainform():
    indicators = []
    for i in range(10):
        indicators.append(
            [Psg.Radio(f'Объект № {i+1} \n', group_id=0, pad=(0, 0), size=(25, 2),
                   font=mainFont, key=radio_btn_key + str(i)),
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
             Psg.Image(data=IconsList.okIcon, key=secutrity_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=power_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=pressure_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=gazAlert_key + str(i), enable_events=True),
             Psg.Image(data=IconsList.okIcon, key=fireAlert_key + str(i), enable_events=True)
             ])

    leftColumn_var = [[Psg.T('Наименование объекта:', font=mainFont, size=(33, 1)),
                       Psg.T('T-воздуха:', font=mainFont, size=(15, 1)),
                       Psg.T('T-Подачи:', font=mainFont, size=(13, 1)),
                       Psg.T('Режим:', font=mainFont, size=(8, 1)),
                       Psg.T('Котел:', font=mainFont, size=(7, 1)),
                       Psg.T('Охрана:', font=mainFont, size=(7, 1)),
                       Psg.T('Питание:', font=mainFont, size=(8, 1)),
                       Psg.T('Давление:', font=mainFont, size=(10, 1)),
                       Psg.T('ГАЗ:', font=mainFont, size=(5, 1)),
                       Psg.T('Пож Сигн:', font=mainFont, size=(8, 1))
                       ]]
    leftColumn_var.extend(indicators)
    headsOnTable = ['Объект: ', 'Событие']
    itemsInTable = [['Каменнозерское СОШ', 'Отсутствует эл. питание']]
    rightColumn_var = [[Psg.Image('', size=(35, 22))],
                       [Psg.Image('', size=(10, 1)), Psg.Image(data=IconsList.allStatusGreen, size=(395, 30))],
                       [Psg.Image('', size=(10, 1)), Psg.Table(itemsInTable, headings=headsOnTable, col_widths=[16, 26],
                        auto_size_columns=False, num_rows=18, selected_row_colors=('black', '#5babd4'),
                                                               alternating_row_color='#91f5fa')]
                       ]
    mainmenu = [['Файл', ['Журнал событий']]]
    main_form_var = [
                    [Psg.Menu(mainmenu)],
                    [Psg.Column(leftColumn_var), Psg.Column(rightColumn_var, vertical_alignment="top")]
                    ]


    main_form = Psg.Window('OmniVision', main_form_var, size=(1360, 680), icon=IconsList.iconMainForm,
                           element_padding=0, finalize=True)

    for element in main_form.element_list():
        if isinstance(element, Psg.Radio):
            element.Widget.configure(justify='left', wraplength=300, height=2, anchor='w')

    while True:
        main_form_event, main_form_value = main_form.read()

        if main_form_event == Psg.WINDOW_CLOSED:
            break
        if main_form_event == mode_key + '0':
            main_form[status_key + '0'].Update(data=IconsList.statusYellow)
            main_form[mode_key + '0'].Update(data=IconsList.winter)
        if main_form_event == power_key + '0':
            main_form[status_key + '0'].Update(data=IconsList.statusRed)
            main_form[power_key + '0'].Update(data=IconsList.errorIcon)
        if main_form_event == secutrity_key + '0':
            main_form[status_key + '0'].Update(data=IconsList.statusGreen)
            main_form[secutrity_key + '0'].Update(data=IconsList.attentionIcon)
        if main_form_event == bollerON_key + '0':
            main_form[status_key + '0'].Update(data=IconsList.statusGreen)
            main_form[bollerON_key + '0'].Update(data=IconsList.powerOFF)

    main_form.close()