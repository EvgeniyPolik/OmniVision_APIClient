import PySimpleGUI as Psg

import IconsList

defaultFont = ('Segoe UI', 10)
defaultFontBold = ('Segoe UI', 10, 'bold')

def NewConfigForm():
    layout1 = [[Psg.Push(), Psg.Text('Введите параметры подключения к БД:', font=defaultFontBold), Psg.Push()],
               [Psg.Text('Адрес сервера:', font=defaultFont, size=(15, 1)),
                Psg.InputText('', size=(25, 1), key='-server-')],
               [Psg.Text('Путь до БД:', font=defaultFont, size=(15, 1)),
                Psg.InputText('', size=(25, 1), key='-pathBd-')],
               [Psg.Push(), Psg.Button('Ok', key='-ok-', size=(15, 1)),
                Psg.Button('Cancel', key='-cancel-', size=(15, 1)), Psg.Push()]
               ]

    newConfigForm = Psg.Window('Параметры', layout1,
                               finalize=True)

    while True:
        event, value = newConfigForm.Read()

        if event in (Psg.WINDOW_CLOSED, '-cancel-'):
            server, pathBd = (None, None)
            break
        if event == '-ok-':
            server = value['-server-']
            pathBd = value['-pathBd-']
            break

    newConfigForm.Close()
    return server, pathBd