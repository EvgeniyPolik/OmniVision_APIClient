# Установлены PySimpleGUI, requests, playsound==1.2.2, matplotlib
import PySimpleGUI as Psg
import locale
import IconsList
import MainForm
import fdb
import ReqQuery
import UserDialog
import ctypes
import platform


def make_dpi_aware():
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)

if ctypes.windll.user32.GetSystemMetrics(0) <= 1366:
    font_size = 10
else:
    font_size = 8
    make_dpi_aware()

MainForm.mainFont = ('Segoe UI', font_size, 'bold')
Psg.SetOptions(font=('Segoe UI', font_size))
locale.setlocale(locale.LC_ALL, '')  # Локализация согласно ОС
Psg.theme('Default1')
Psg.SetOptions(text_justification='l')
Psg.SetOptions(icon=IconsList.iconMainForm)


while True:  # Первичный запуск, ошибка подключения к БД
    try:
        with open('config.cfg', 'r') as paramfile:
            configApp = paramfile.readlines()
        ReqQuery.host = configApp[0].strip('\n')
        pathDb = configApp[1].strip('\n')
        db = fdb.connect(host=ReqQuery.host, database=pathDb, user='SYSDBA', password='masterkey')
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
auth_ok = False
while True:  # Проверка пользователя
    user_name = UserDialog.ask_param_or_user_name(False)
    if user_name[0] is None:
        break
    select_query = f'SELECT COUNT(*) FROM US WHERE NAM_US = \'{user_name[0]}\' AND PASS = \'{user_name[1]}\''
    fb_cursor.execute(select_query)
    if fb_cursor.fetchall()[0][0] >= 1:
        auth_ok = True
        break
    else:
        UserDialog.popup('Указанные имя пользователь и пароль не найдены!')
if auth_ok:
    select_query = f'SELECT PRIV FROM US WHERE NAM_US = \'{user_name[0]}\' AND PASS = \'{user_name[1]}\''
    user_privilege = fb_cursor.execute(select_query).fetchall()[0][0]
    ReqQuery.get_catalog()
    ReqQuery.update_status()
    fb_cursor.close()
    MainForm.mainform(db)

