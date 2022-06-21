import IconsList
import MainForm
import ReqQuery
import correction_factor
import playsound


lcd__b = {'0': IconsList.led0, '1': IconsList.led1, '2': IconsList.led2, '3': IconsList.led3, '4': IconsList.led4,
          '5': IconsList.led5, '6': IconsList.led6, '7': IconsList.led7, '8': IconsList.led8, '9': IconsList.led9,
          '-': IconsList.led_, ' ': IconsList.ledNo}
lcd__r = {'0': IconsList.led0r, '1': IconsList.led1r, '2': IconsList.led2r, '3': IconsList.led3r, '4': IconsList.led4r,
          '5': IconsList.led5r, '6': IconsList.led6r, '7': IconsList.led7r, '8': IconsList.led8r, '9': IconsList.led9r,
          '-': IconsList.led_r, ' ': IconsList.ledNo}
type_of_error = {0: 'Отсутсвует связь', 1: 'Отклонение от графика', 2: 'Низкая температура подачи',
                 3: 'Ошибка давления', 5: 'Пожарная тревога', 6: 'Ошибка котла', 7: 'Отсутствие напряжения',
                 8: 'Загазованность в помещении', 9: 'Котел отключен', 10: 'Проникновение', 14: 'Снят с охраны'}
registers_of_answer = {
                        3: ['pressure', 'pressure_key', 'error', 'ok', 1, IconsList.errorIcon, IconsList.okIcon],
                        5: ['fire', 'fireAlert_key', 'error', 'ok', 0, IconsList.errorIcon, IconsList.okIcon],
                        6: ['error', 'boller_error_key', 'error', 'ok', 1, IconsList.errorIcon, IconsList.okIcon],
                        7: ['power', 'power_key', 'error', 'ok', 0, IconsList.errorIcon, IconsList.okIcon],
                        8: ['GAZ', 'gazAlert_key', 'error', 'ok', 0, IconsList.errorIcon, IconsList.okIcon],
                       13: ['mode', 'mode_key', 's', 'w', 0, IconsList.summer, IconsList.winter]
                        }

active_error = set()


def name_of_object(position):
    offset = MainForm.offset
    if position < len(ReqQuery.catalog_bollers):
        return {
            'id_odject': ReqQuery.catalog_bollers[position + offset]['Id'],
            'name_object': ReqQuery.catalog_bollers[position + offset]['Properties'][0],
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


def update_info_form():  # Обновление списка
    for i in range(10):
        name_dict = name_of_object(i)
        MainForm.main_form[MainForm.name_of_elements['radio_btn_key'] + str(i)].update(text=name_dict['name_object'] +
            '\n' + name_dict['city_object'] + name_dict['pnt'] + name_dict['street_object'] + name_dict['pnt'] +
            name_dict['build_object'], disabled=name_dict['not_active'])
        if name_dict['not_active']:
            for n in range(3):
                MainForm.main_form[MainForm.name_of_elements['led_t1_key'] +
                                   str(n) + str(i)].Update(data=lcd__b[' 00'[n]])
                MainForm.main_form[MainForm.name_of_elements['led_t2_key'] +
                                   str(n) + str(i)].Update(data=lcd__r[' 00'[n]])
            MainForm.main_form[MainForm.name_of_elements['status_key'] + str(i)].Update(data=IconsList.statusGreen)


def refresh_form():
    offset = MainForm.offset
    global active_error
    new_error = set()
    max_position = len(ReqQuery.catalog_bollers)
    # max_position = len(ReqQuery.catalog_bollers) if len(ReqQuery.catalog_bollers) < 11 else 10
    global_status = 'g'  # Значение по умолчанию
    new_attention = False
    for position in range(max_position):  # Обновим сведения
        offset_position = position - offset
        if offset <= position < offset + 10:  # отображен ли объект на форме
            new_status = 'g'  # Значение по умолчанию
            item_on_form = True
        else:
            item_on_form = False
        current_state = ReqQuery.health_bollers.get(ReqQuery.catalog_bollers[position]["Id"],
                                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        if current_state[0] == 0:  # Первое значение - наличие связи
            if global_status != 'r':
                global_status = 'y'
            new_error.add((position, type_of_error[0]))
            if (position, type_of_error[0]) not in active_error:
                new_error.add((position, type_of_error[0] + '-first-'))
            else:
                if (position, type_of_error[0] + '-first-') in active_error:
                    new_attention = True
            if item_on_form:
                new_status = 'y'
                if MainForm.status_of_image['mode'][offset_position] != 'unknow':
                    for key in MainForm.status_of_image:
                        MainForm.status_of_image[key][offset_position] = 'unknow'
                    for key in MainForm.name_of_elements:
                        if key == 'led_t1_key':
                            for n in range(3):
                                MainForm.main_form[MainForm.name_of_elements['led_t1_key'] + str(n) +
                                                   str(offset_position)].Update(data=lcd__b['00'.rjust(3, ' ')[n]])
                        elif key == 'led_t2_key':
                            for n in range(3):
                                MainForm.main_form[MainForm.name_of_elements['led_t2_key'] + str(n) +
                                               str(offset_position)].Update(data=lcd__r['00'.rjust(3, ' ')[n]])
                        elif key != 'radio_btn_key':
                            MainForm.main_form[MainForm.name_of_elements[key] +
                                               str(offset_position)].Update(data=IconsList.unknow)
        else:
            if item_on_form:
                for n in range(3):  # температура ввиде лсд цифр
                    MainForm.main_form[MainForm.name_of_elements['led_t1_key'] + str(n) +
                                       str(offset_position)].Update(data=lcd__b[str(current_state[1]).rjust(3, ' ')[n]])
                    MainForm.main_form[MainForm.name_of_elements['led_t2_key'] + str(n) +
                                       str(offset_position)].Update(data=lcd__r[str(current_state[2]).rjust(3, ' ')[n]])

            # Проверка температуры подачи
            k = correction_factor.get_correction(current_state[1])
            if (((10 - current_state[1]) * 1.2 + 40.4 + k) > 3) and new_status != 'r' and current_state[13] == 1:
                global_status = 'y'
                new_error.add((position, type_of_error[1]))
                if (position, type_of_error[1]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'y'

            # Предельно низкая температура подачи
            if current_state[1] < 11 and current_state[2] < 35 and current_state[13] == 1:
                global_status = 'r'
                new_error.add((position, type_of_error[2]))
                if (position, type_of_error[2]) not in active_error:
                    new_attention = True
                if item_on_form:
                    new_status = 'r'

            if current_state[9] == 0:  # Включение котла
                if current_state[13] == 1:
                    global_status = 'r'
                    new_status = 'r'
                    new_error.add((position, type_of_error[9]))
                    if (position, type_of_error[9]) not in active_error:
                        new_attention = True
                if MainForm.status_of_image['boller'][offset_position] != 'off' and item_on_form:
                    MainForm.status_of_image['boller'][offset_position] = 'off'
                    MainForm.main_form[MainForm.name_of_elements['bollerON_key'] +
                                       str(offset_position)].Update(data=IconsList.powerOFF)
            else:
                if MainForm.status_of_image['boller'][offset_position] != 'on' and item_on_form:
                    MainForm.status_of_image['boller'][offset_position] = 'on'
                    MainForm.main_form[MainForm.name_of_elements['bollerON_key'] +
                                       str(offset_position)].Update(data=IconsList.powerON)

            for key, value in registers_of_answer.items():
                if current_state[key] == value[4]:
                    if key != 13:
                        global_status = 'r'
                        new_status = 'r'
                        new_error.add((position, type_of_error[key]))
                        if (position, type_of_error[key]) not in active_error:
                            new_attention = True
                    if MainForm.status_of_image[value[0]][offset_position] != value[2] and item_on_form:
                        MainForm.status_of_image[value[0]][offset_position] = value[2]
                        MainForm.main_form[MainForm.name_of_elements[value[1]] +
                                           str(offset_position)].Update(data=value[5])
                else:
                    if MainForm.status_of_image[value[0]][offset_position] != value[3] and item_on_form:
                        MainForm.status_of_image[value[0]][offset_position] = value[3]
                        MainForm.main_form[MainForm.name_of_elements[value[1]] +
                                           str(offset_position)].Update(data=value[6])

            if current_state[10] == 1:  # Проникновение, нарушение периметра
                global_status = 'r'
                new_status = 'r'
                new_error.add((position, type_of_error[10]))
                if (position, type_of_error[10]) not in active_error:
                    new_attention = True
                if MainForm.status_of_image['security'][position - offset] != 'error' and item_on_form:
                    MainForm.status_of_image['security'][position - offset] = 'error'
                    MainForm.main_form[MainForm.name_of_elements['secutrity_key'] +
                                       str(position - offset)].Update(data=IconsList.errorIcon)
            else:
                if MainForm.status_of_image['security'][position - offset] != 'ok' and current_state[14] == 1 \
                        and item_on_form:
                    MainForm.status_of_image['security'][position - offset] = 'ok'
                    MainForm.main_form[MainForm.name_of_elements['secutrity_key'] +
                                       str(position - offset)].Update(data=IconsList.okIcon)
                elif current_state[14] == 0:
                    if global_status != 'r':
                        global_status = 'y'
                    new_error.add((position, type_of_error[14]))
                    if (position, type_of_error[14]) not in active_error:
                        new_attention = True
                    if item_on_form and new_status != 'r':
                        new_status = 'y'
                    if MainForm.status_of_image['security'][position - offset] != 'off':
                        MainForm.status_of_image['security'][position - offset] = 'off'
                        MainForm.main_form[MainForm.name_of_elements['secutrity_key'] +
                                           str(position - offset)].Update(data=IconsList.attentionIcon)

        if item_on_form and MainForm.status_of_image['status_object'][position - offset] != new_status:
            if new_status == 'g':
                MainForm.main_form[MainForm.name_of_elements['status_key']
                                   + str(offset_position)].Update(data=IconsList.statusGreen)
            elif new_status == 'y':
                MainForm.main_form[MainForm.name_of_elements['status_key']
                                   + str(offset_position)].Update(data=IconsList.statusYellow)
            else:
                MainForm.main_form[MainForm.name_of_elements['status_key']
                                   + str(offset_position)].Update(data=IconsList.statusRed)
            MainForm.status_of_image['status_object'][offset_position] = new_status
    active_error = new_error.copy()
    if global_status == 'g':
        MainForm.main_form['-state-'].Update(data=IconsList.allStatusGreen)
    elif global_status == 'y':
        MainForm.main_form['-state-'].Update(data=IconsList.allStatusYellow)
    else:
        MainForm.main_form['-state-'].Update(data=IconsList.allStatusRed)

    list_error_for_table = []
    for item in sorted(active_error):
        if item[1][-7:] != '-first-':
            list_error_for_table.append([ReqQuery.catalog_bollers[item[0]]['Properties'][0], item[1]])
    MainForm.main_form['-table_error-'].Update(list_error_for_table)
    if new_attention:
        playsound.playsound('anamlia.mp3')
