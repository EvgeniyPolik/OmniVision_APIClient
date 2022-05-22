import PySimpleGUI as Psg
import IconsList

radio_btn_key = '-radio-'
secutrity_btn_key = '-security-'
power_btn_key = '-power-'
status_btn_key = '-status-'
led_t1_key = '-t1-'
mainFont = ('Segoe UI', 10, 'bold')

def mainfrom():
    radio_btn = []
    for i in range(10):
        radio_btn.append(
            [Psg.Radio(f'Объект № {i+1} \n', group_id=0, pad=(0, 0), size=(25, 2),
                   font=mainFont, key=radio_btn_key + str(i)),
             Psg.Button('', button_color=("green", "green"), border_width=0, key=status_btn_key + str(i), size=(1, 3),
                        disabled=True),
             Psg.T('', size=(2, 1)),
             Psg.Image(data=IconsList.led_, key=led_t1_key + '0' + str(i)),
             Psg.Image(data=IconsList.led0, key=led_t1_key + '1' + str(i)),
             Psg.Image(data=IconsList.led0, key=led_t1_key + '2' + str(i)),
             Psg.Button('', image_data=IconsList.okIcon, key=secutrity_btn_key + str(i)),
             Psg.Button('', image_data=IconsList.okIcon, key=power_btn_key + str(i))])

    mainmenu = [['Файл', ['Журнал событий']]]
    main_form_var = [
                    [Psg.Menu(mainmenu)],
                    [Psg.Button('n', visible=False), Psg.T('Наименование объекта:', font=mainFont, size=(25, 1))]
                    ]
    main_form_var.extend(radio_btn)

    main_form = Psg.Window('OmniVision', main_form_var, size=(1360, 680), icon=IconsList.iconMainForm,
                           element_padding=0, finalize=True)

    for element in main_form.element_list():
        if isinstance(element, Psg.Radio):
            element.Widget.configure(justify='left', wraplength=300, height=2, anchor='w')

    while True:
        main_form_event, main_form_value = main_form.read()

        if main_form_event == Psg.WINDOW_CLOSED:
            break
        if main_form_event == secutrity_btn_key + '0':
            main_form[status_btn_key + '0'].Update(button_color=("yellow", "yellow"))
            main_form[secutrity_btn_key + '0'].Update(image_data=IconsList.attentionIcon)
        if main_form_event == power_btn_key + '0':
            main_form[status_btn_key + '0'].Update(button_color=("red", "red"))
            main_form[power_btn_key + '0'].Update(image_data=IconsList.errorIcon)

    main_form.close()
