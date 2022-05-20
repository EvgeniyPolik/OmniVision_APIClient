import PySimpleGUI as Psg
import IconsList


def MainFrom():
    mainMenu = [['Файл', ['Журнал событий']]]
    mainFormVar = [
        [Psg.Menu(mainMenu)],
        [Psg.Radio('', group_id=0, background_color='lightblue', pad=(0, 0), size=(0, 130)),
         Psg.Text('Волковское СОШ \nс. Волково, Рабочая, 35', background_color='lightblue', pad=(0, 0), size=(25, 2))]
    ]

    main_form = Psg.Window('OmniVision', mainFormVar, size=(1360, 680), icon=IconsList.iconMainForm, element_padding=0)

    while True:
        main_event, main_value = main_form.read()

        if main_event == Psg.WINDOW_CLOSED:
            break
        if main_event == 'theme':
            Psg.theme_previewer()

    main_form.close()