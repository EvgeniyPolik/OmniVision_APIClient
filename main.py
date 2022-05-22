# Установлены PySimpleGUI
import PySimpleGUI as Psg
import locale
import MainForm

locale.setlocale(locale.LC_ALL, '')  # Локализация согласно ОС
Psg.theme('Default1')
Psg.SetOptions(text_justification='l')
Psg.SetOptions(border_width=0)

MainForm.mainfrom()


