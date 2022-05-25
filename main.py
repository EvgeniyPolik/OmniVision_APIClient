# Установлены PySimpleGUI, requests
import PySimpleGUI as Psg
import locale

import IconsList
import MainForm
import fdb

import RegQuery
import UserDialog

locale.setlocale(locale.LC_ALL, '')  # Локализация согласно ОС
Psg.theme('Default1')
Psg.SetOptions(text_justification='l')
Psg.SetOptions(icon=IconsList.iconMainForm)

while True:  # Первичный запуск, ошибка подключения к БД
    try:
        with open('config.cfg', 'r') as paramfile:
            configApp = paramfile.readlines()
        host = configApp[0].strip('\n')
        pathDb = configApp[1].strip('\n')
        db = fdb.connect(host=host, database=pathDb, user='SYSDBA', password='masterkey')
        break
    except (FileNotFoundError, IndexError, fdb.fbcore.DatabaseError):
        UserDialog.popup('Ошибка параметров приложения')
        NewConfig = UserDialog.ask_param_or_user_name(True)
        if NewConfig[0] is None:
            exit(0)
        with open('config.cfg', 'w') as paramfile:
            for u in range(len(NewConfig)):
                paramfile.writelines(NewConfig[u] + '\n')

fb_cursor = db.cursor()

while True:  # Проверка пользователя
    user_name = UserDialog.ask_param_or_user_name(False)
    if user_name[0] is None:
        exit(0)
    select_query = f'SELECT COUNT(*) FROM US WHERE NAM_US = \'{user_name[0]}\' AND PASS = \'{user_name[1]}\''
    fb_cursor.execute(select_query)
    if fb_cursor.fetchall()[0][0] >= 1:
        break
    else:
        UserDialog.popup('Указанные имя пользователь и пароль не найдены!')
select_query = f'SELECT PRIV FROM US WHERE NAM_US = \'{user_name[0]}\' AND PASS = \'{user_name[1]}\''
user_privilege = fb_cursor.execute(select_query).fetchall()[0][0]

RegQuery.get_catalog()
RegQuery.update_status()
MainForm.mainform()

