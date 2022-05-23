# Установлены PySimpleGUI
import PySimpleGUI as Psg
import locale
import MainForm
import fdb

import NewConfigForm

locale.setlocale(locale.LC_ALL, '')  # Локализация согласно ОС
Psg.theme('Default1')
Psg.SetOptions(text_justification='l')

while True:
    try:
        with open('config.cfg', 'r') as paramfile:
            configApp = paramfile.readlines()
        host = configApp[0]
        pathDb = configApp[1]
        db = fdb.connect(host=host, database=pathDb, user='SYSDBA', password='masterkey')
        break
    except (FileNotFoundError, IndexError):
        Psg.Popup('Ошибка параметров приложения')
        NewConfig = NewConfigForm.NewConfigForm()
        if NewConfig[0] is None:
            exit(0)
        with open('config.cfg', 'w') as paramfile:
            for u in range(len(NewConfig)):
                paramfile.writelines(NewConfig[u])


MainForm.mainform()


