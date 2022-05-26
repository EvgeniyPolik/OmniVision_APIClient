import IconsList
import MainForm
import ReqQuery
import correction_factor

lcd__b = {'0': IconsList.led0, '1': IconsList.led1, '2': IconsList.led2, '3': IconsList.led3, '4': IconsList.led4,
          '5': IconsList.led5, '6': IconsList.led6, '7': IconsList.led7, '8': IconsList.led8, '9': IconsList.led9,
          '-': IconsList.led_, ' ': IconsList.ledNo}
lcd__r = {'0': IconsList.led0r, '1': IconsList.led1r, '2': IconsList.led2r, '3': IconsList.led3r, '4': IconsList.led4r,
          '5': IconsList.led5r, '6': IconsList.led6r, '7': IconsList.led7r, '8': IconsList.led8r, '9': IconsList.led9r,
          '-': IconsList.led_r, ' ': IconsList.ledNo}
type_of_error = {0: 'Отсутсвует связь', 1: 'Отклонение от графика', 2: 'Низкая температура подачи',
                 3: 'Ошибка давления', 5: 'Пожарная тревога', 6: 'Ошибка котла', 7: 'Отсутствие напряжения',
                 8: 'Загазованность в помещении', 9: 'Котел отключен', 10: 'Проникновение', 14: 'Снят с охраны'}

active_error = set()


def name_of_object(position, offset: int = 0):
    print(position, len(ReqQuery.catalog_bollers))
    if position < len(ReqQuery.catalog_bollers):
        return {
            'id_odject': ReqQuery.catalog_bollers[position + offset]['Id'],
            'name_object': str(ReqQuery.catalog_bollers[position + offset]['Properties'][0]),
            'city_object': ReqQuery.catalog_bollers[position + offset]['Properties'][1],
            'street_object': ReqQuery.catalog_bollers[position + offset]['Properties'][2],
            'build_object': ReqQuery.catalog_bollers[position + offset]['Properties'][3],
            'pnt': ', ',
            'not_active': False
        }
    else:
        return {
            'id_odject': -1,
            'name_object': 'Объект № ' + str(position),
            'city_object': '',
            'street_object': '',
            'build_object': '',
            'pnt': ' ',
            'not_active': True
        }


def refresh_form(offset: int = 0):
    global active_error
    new_error = set()
    max_position = len(ReqQuery.catalog_bollers) if len(ReqQuery.catalog_bollers) < 11 else 10
    global_status = 'g'
    new_attention = False
    for position in range(max_position):  # Сначала обновим отображенные на форме
        new_status = 'g'  # Значение по умолчанию
        if offset <= position < offset + 10:
            item_on_form = True
        else:
            item_on_form = False
        current_state = ReqQuery.health_bollers[ReqQuery.catalog_bollers[position]["Id"]]
        current_id = ReqQuery.catalog_bollers[position]["Id"]
        if current_state[0] == 0:  # Первое значение - наличие связи
            global_status = 'y'
            new_error.add((position, type_of_error[0]))
            if (position, type_of_error[0]) not in active_error:
                new_attention = True
            if item_on_form:
                new_status = 'y'
        else:
            for n in range(3):  # температура ввиде лсд цифр
                MainForm.main_form[MainForm.led_t1_key + str(n) +
                                   str(position)].Update(data=lcd__b[str(current_state[1]).rjust(3, ' ')[n]])
                MainForm.main_form[MainForm.led_t2_key + str(n) +
                                   str(position)].Update(data=lcd__r[str(current_state[2]).rjust(3, ' ')[n]])

            # Проверка температуры подачи
            k = correction_factor.get_correction(current_state[1])
            if (((10 - current_state[1]) * 1.2 + 40.4 + k) > 3) and new_status != 'r' and current_state[13] == 1:
                global_status = 'y'
                new_error.add((position, type_of_error[1]))
                if (position, type_of_error[1]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'y'

            if current_state[1] < 11 and current_state[2] < 35 and current_state[13] == 1:
                global_status = 'r'
                new_error.add((position, type_of_error[2]))
                if (position, type_of_error[2]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'

            if current_state[3] == 1:  # Ошибка давления
                global_status = 'r'
                new_error.add((position, type_of_error[3]))
                if (position, type_of_error[3]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'
                if MainForm.status_of_image['pressure'][position] != 'error':
                    MainForm.status_of_image['pressure'][position] = 'error'
                    MainForm.main_form[MainForm.pressure_key + str(position)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['pressure'][position] != 'ok':
                    MainForm.status_of_image['pressure'][position] = 'ok'
                    MainForm.main_form[MainForm.pressure_key + str(position)].Update(data=IconsList.okIcon)

            if current_state[5] == 0:  # Пожарный датчик
                global_status = 'r'
                new_error.add((position, type_of_error[5]))
                if (position, type_of_error[5]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'
                if MainForm.status_of_image['fire'][position] != 'error':
                    MainForm.status_of_image['fire'][position] = 'error'
                    MainForm.main_form[MainForm.fireAlert_key + str(position)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['fire'][position] != 'ok':
                    MainForm.status_of_image['fire'][position] = 'ok'
                    MainForm.main_form[MainForm.fireAlert_key + str(position)].Update(data=IconsList.okIcon)

            if current_state[6] == 1:  # Авария котла
                global_status = 'r'
                new_error.add((position, type_of_error[5]))
                if (position, type_of_error[5]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'
                if MainForm.status_of_image['error'][position] != 'error':
                    MainForm.status_of_image['error'][position] = 'error'
                    MainForm.main_form[MainForm.boller_error_key + str(position)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['error'][position] != 'ok':
                    MainForm.status_of_image['error'][position] = 'ok'
                    MainForm.main_form[MainForm.boller_error_key + str(position)].Update(data=IconsList.okIcon)

            if current_state[7] == 0:  # Наличие напряжения
                global_status = 'r'
                new_error.add((position, type_of_error[7]))
                if (position, type_of_error[7]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'
                if MainForm.status_of_image['power'][position] != 'error':
                    MainForm.status_of_image['power'][position] = 'error'
                    MainForm.main_form[MainForm.power_key + str(position)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['power'][position] != 'ok':
                    MainForm.status_of_image['power'][position] = 'ok'
                    MainForm.main_form[MainForm.power_key + str(position)].Update(data=IconsList.okIcon)

            if current_state[8] == 0:  # Загазованность
                global_status = 'r'
                new_error.add((position, type_of_error[8]))
                if (position, type_of_error[8]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'
                if MainForm.status_of_image['GAZ'][position] != 'error':
                    MainForm.status_of_image['GAZ'][position] = 'error'
                    MainForm.main_form[MainForm.gazAlert_key+str(position)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['GAZ'][position] != 'ok':
                    MainForm.status_of_image['GAZ'][position] = 'ok'
                    MainForm.main_form[MainForm.gazAlert_key + str(position)].Update(data=IconsList.okIcon)

            if current_state[9] == 0:  # Включение котла
                if current_state[13] == 1:
                    global_status = 'r'
                    new_error.add((position, type_of_error[9]))
                    if (position, type_of_error[9]) not in active_error:
                        new_attention = True
                    if item_on_form:
                        new_status = 'r'
                if MainForm.status_of_image['boller'][position] != 'off':
                    MainForm.status_of_image['boller'][position] = 'off'
                    MainForm.main_form[MainForm.bollerON_key + str(position)].Update(data=IconsList.powerOFF)
            else:
                if MainForm.status_of_image['boller'][position] != 'on':
                    MainForm.status_of_image['boller'][position] = 'on'
                    MainForm.main_form[MainForm.bollerON_key + str(position)].Update(data=IconsList.powerON)

            if current_state[10] == 1:  # Проникновение, нарушение периметра
                global_status = 'r'
                new_error.add((position, type_of_error[10]))
                if (position, type_of_error[10]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'
                if MainForm.status_of_image['security'][position] != 'error':
                    MainForm.status_of_image['security'][position] = 'error'
                    MainForm.main_form[MainForm.secutrity_key + str(position)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['security'][position] != 'ok' and current_state[14] == 1:
                    MainForm.status_of_image['security'][position] = 'ok'
                    MainForm.main_form[MainForm.secutrity_key + str(position)].Update(data=IconsList.okIcon)
                elif MainForm.status_of_image['security'][position] != 'off' and current_state[14] == 0:
                    if global_status != 'r':
                        global_status = 'y'
                    new_error.add((position, type_of_error[14]))
                    if (position, type_of_error[14]) not in active_error:
                        new_attention = True
                    if item_on_form and new_status != 'r':
                        new_status = 'y'
                    MainForm.status_of_image['security'][position] = 'off'
                    MainForm.main_form[MainForm.secutrity_key + str(position)].Update(data=IconsList.attentionIcon)

            if current_state[13] == 0:  # Режим зима/лето
                if MainForm.status_of_image['mode'][position] != 's':
                    MainForm.status_of_image['mode'][position] = 's'
                    MainForm.main_form[MainForm.mode_key + str(position)].Update(data=IconsList.summer)
            else:
                if MainForm.status_of_image['mode'][position] != 'w':
                    MainForm.status_of_image['mode'][position] = 'w'
                    MainForm.main_form[MainForm.mode_key + str(position)].Update(data=IconsList.winter)

        if MainForm.status_of_image['status_object'][position] != new_status:
            if new_status == 'g':
                MainForm.main_form[MainForm.status_key + str(position)].Update(data=IconsList.statusGreen)
            elif new_status == 'y':
                MainForm.main_form[MainForm.status_key + str(position)].Update(data=IconsList.statusYellow)
            else:
                MainForm.main_form[MainForm.status_key + str(position)].Update(data=IconsList.statusRed)
            MainForm.status_of_image['status_object'][position] = new_status
    active_error = new_error.copy()
    if new_attention:
        pass
    if global_status == 'g':
        MainForm.main_form['-state-'].Update(data=IconsList.allStatusGreen)
    elif global_status == 'y':
        MainForm.main_form['-state-'].Update(data=IconsList.allStatusYellow)
    else:
        MainForm.main_form['-state-'].Update(data=IconsList.allStatusRed)
    list_error_for_table = []
    for item in sorted(active_error):
        list_error_for_table.append([ReqQuery.catalog_bollers[item[0]]['Properties'][0], item[1]])
    MainForm.main_form['-table_error-'].Update(list_error_for_table)
