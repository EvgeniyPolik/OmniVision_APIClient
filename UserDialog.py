import PySimpleGUI as Psg

import IconsList

defaultFont = ('Segoe UI', 10)
defaultFontBold = ('Segoe UI', 10, 'bold')


def ask_param_or_user_name(windowcfg):
    if windowcfg:
        string_value = ['Введите параметры подключения к БД:', 'Адрес сервера:', 'Путь до БД:', 'Параметры']
        second_input = Psg.InputText('', size=(25, 1), key='-param_two-')
    else:
        string_value = ['Введите имя пользоателя и пароль', 'Пользователь:', 'Пароль:', 'Авторизация']
        second_input = Psg.InputText('', size=(25, 1), key='-param_two-', password_char='*')
    layout = [[Psg.Push(), Psg.Text(string_value[0], font=defaultFontBold), Psg.Push()],
              [Psg.Text(string_value[1], font=defaultFont, size=(15, 1)),
               Psg.InputText('', size=(25, 1), key='-param_one-')],
              [Psg.Text(string_value[2], font=defaultFont, size=(15, 1)),
               second_input],
              [Psg.Push(), Psg.Button('Ok', key='-ok-', size=(15, 1)),
               Psg.Button('Cancel', key='-cancel-', size=(15, 1)), Psg.Push()]
              ]
    new_config_form = Psg.Window(string_value[3], layout,
                                 finalize=True, icon=IconsList.iconMainForm)
    while True:
        event, value = new_config_form.Read()

        if event in (Psg.WINDOW_CLOSED, '-cancel-'):
            param_one, param_two = (None, None)
            break
        if event == '-ok-':
            param_one = value['-param_one-']
            param_two = value['-param_two-']
            break
    new_config_form.Close()
    return param_one, param_two


def popup(text: str):
    layout = [[Psg.Push(), Psg.Image(data=IconsList.warning_icon_for_dialog), Psg.Push(),
               Psg.T(text, font=defaultFont), Psg.Push()],
              [Psg.Push(), Psg.Button('Ok', size=(10, 1)), Psg.Push()]]
    popup_form = Psg.Window('Внимание!', layout, modal=True, icon=IconsList.iconMainForm)
    while True:
        event, value = popup_form.Read()
        if event in (Psg.WINDOW_CLOSED, 'Ok'):
            break
    popup_form.close()
