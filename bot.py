import time

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import async_dec

import data
import db_bot
import pars_lardi

bot = telebot.TeleBot(data.TOKEN)


class manage:
    on_off = {}
    on_off_search = {}
    list_delete_url_next = []
    list_delete_url_next_search = []
    list_open_info = []
    list_open_info_search = []
    list_open_url = []


@bot.message_handler(commands=['start'])
def message_handler(message):
    check = db_bot.get_id_tg_check(message.chat.id)
    if check is None or check['ids_tg'] != str(message.chat.id):
        bot.send_message(message.chat.id, 'У вас нет доступа.')
    else:
        kb = InlineKeyboardMarkup()
        start_search = InlineKeyboardButton('Начать мониторинг', callback_data='start_search')
        stop_search = InlineKeyboardButton('Закончить мониторинг', callback_data='stop_search')
        add_url_search = InlineKeyboardButton('Добавить ссылку', callback_data='add_url_search')
        remove_url_search = InlineKeyboardButton('Удалить ссылки', callback_data='remove_url_search')
        kb.add(add_url_search, remove_url_search)
        status = db_bot.get_id_tg_info(str(message.chat.id))
        if int(status['status_monit']) == 1:
            kb.add(start_search)
            bot.send_message(chat_id=message.chat.id, text='Меню '
                                                           'управлением '
                                                           'мониторингом ',
                             reply_markup=kb)
        if int(status['status_monit']) == 0:
            kb.add(stop_search)
            bot.send_message(chat_id=message.chat.id, text='Меню '
                                                           'управлением '
                                                           'мониторингом\n'
                                                           'Идёт '
                                                           'мониторинг.',
                             reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
@async_dec()
def callback_query(call):
    # Поиск груза
    if call.data == 'menu':
        kb = InlineKeyboardMarkup()
        start_search = InlineKeyboardButton('Начать мониторинг', callback_data='start_search')
        stop_search = InlineKeyboardButton('Закончить мониторинг', callback_data='stop_search')
        add_url_search = InlineKeyboardButton('Добавить ссылку', callback_data='add_url_search')
        remove_url_search = InlineKeyboardButton('Удалить ссылки', callback_data='remove_url_search')
        kb.add(add_url_search, remove_url_search)
        status = db_bot.get_id_tg_info(str(call.message.chat.id))
        if int(status['status_monit']) == 1:
            kb.add(start_search)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Меню '
                                                                                                         'управлением '
                                                                                                         'мониторингом '
                                                                                                         'поиска '
                                                                                                         'грузов',
                                  reply_markup=kb)
        if int(status['status_monit']) == 0:
            kb.add(stop_search)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Меню '
                                                                                                         'управлением '
                                                                                                         'мониторингом '
                                                                                                         'поиска '
                                                                                                         'грузов\n'
                                                                                                         'Идёт '
                                                                                                         'мониторинг.',
                                  reply_markup=kb)
    if call.data == 'remove_url_search':
        urls = db_bot.get_cargo_url_search(str(call.message.chat.id))
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
        for url in urls:
            delete_url = InlineKeyboardButton(url['name'], callback_data=str(url['id']) + '_re')
            manage.list_delete_url_next_search.append(str(url['id']) + '_re')
            kb.add(delete_url)
        kb.add(cargo_users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Нажмите для удаления',
                              reply_markup=kb)
    if call.data in manage.list_delete_url_next_search:
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
        kb.add(cargo_users)
        id_url = call.data.split('_')[0]
        db_bot.delete_cargo_url_search(id_url)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Успешно удалено.',
                              reply_markup=kb)
    if call.data == 'stop_search':
        db_bot.update_status('1', str(call.message.chat.id))
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
        kb.add(cargo_users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Мониторинг закончен.', reply_markup=kb)
    if call.data == 'add_url_search':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Введите ссылку(/start для отмены):')
        bot.register_next_step_handler(msg, add_url_step_search)
    if call.data == 'start_search':
        db_bot.update_status('0', str(call.message.chat.id))
        on_off = {}
        status = db_bot.get_id_tg_info(str(call.message.chat.id))
        on_off[str(status['ids_tg'])] = int(status['status_monit'])
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
        kb.add(cargo_users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Мониторинг начался.',
                              reply_markup=kb)
        while on_off[str(call.message.chat.id)] == 0:
            list_url = db_bot.get_cargo_url_search(str(call.message.chat.id))
            if list_url is None or str(list_url) == '()':
                kb = InlineKeyboardMarkup()
                add_url = InlineKeyboardButton('Добавить ссылку', callback_data='add_url_search')
                back = InlineKeyboardButton('Назад', callback_data='menu')
                kb.add(add_url)
                kb.add(back)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Добавте '
                                                                                                             'хоть одну '
                                                                                                             'ссылку.',
                                      reply_markup=kb)
            if list_url is not None and str(list_url) != '()':
                list_upload_url_gruz = []
                list_upload_url_truns = []
                for data in list_url:
                    if data['url'].split('/')[3] == 'gruz' or data['url'].split('/')[3] == 'trans':
                        list_upload_url_gruz.append(data['url'])
                    if data['url'].split('/')[3] == 'user':
                        list_upload_url_truns.append(data['url'])
                list_write_all = pars_lardi.get_cargo_search(list_upload_url_gruz, str(call.message.chat.id))
                for url in list_write_all:
                    list_check = db_bot.get_cargo_info_search(url)
                    data_url_info = db_bot.get_cargo_url_search_url(list_check['global_url'])
                    kb = InlineKeyboardMarkup()
                    open_full_info = InlineKeyboardButton('Подробнее',
                                                          callback_data=str(list_check['id']))
                    open_lardi = InlineKeyboardButton('Открыть', url=list_check['url'])
                    open_lardi_full = InlineKeyboardButton('Открыть весь фильтр', url=list_check['global_url'])
                    manage.list_open_info_search.append(str(list_check['id']))
                    kb.add(open_full_info, open_lardi)
                    kb.add(open_lardi_full)
                    bot.send_message(str(list_check['tg_id']), 'Новая заявка от ' + str(data_url_info['name']),
                                     reply_markup=kb)
                list_write_all = pars_lardi.get_cargo(list_upload_url_truns, str(call.message.chat.id))
                for URL in list_write_all:
                    kb = InlineKeyboardMarkup()
                    list_check = db_bot.get_cargo_info(URL)
                    open_full_info = InlineKeyboardButton('Подробнее',
                                                          callback_data=str(list_check['id']))
                    open_lardi = InlineKeyboardButton('Открыть', url=list_check['url'])
                    manage.list_open_info.append(str(list_check['id']))
                    kb.add(open_full_info, open_lardi)
                    try:
                        bot.send_message(list_check['tg_id'], list_check['name'], reply_markup=kb)
                    except:
                        pass
            print('круг')
            time.sleep(60)
            status = db_bot.get_id_tg_info(str(call.message.chat.id))
            on_off[str(status['ids_tg'])] = int(status['status_monit'])
    if call.data in manage.list_open_info_search:
        kb = InlineKeyboardMarkup()
        name = call.data
        list_check = db_bot.get_cargo_info_by_id_search(name)
        open_lardi = InlineKeyboardButton('Открыть на ларди', url=list_check['url'])
        kb.add(open_lardi)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Страны/Тип:\n%s'
                                                                                                     '\n\nДата:\n%s\n'
                                                                                                     '\nТранспорт:\n'
                                                                                                     '%s\n\nОткуда:\n'
                                                                                                     '%s\n\nКуда:\n%s'
                                                                                                     '\n\nГруз:\n%s\n '
                                                                                                     '\nОплата:\n%s\n'
                                                                                                     '\nКонтакты:\n%s' % (
                                                                                                         list_check[
                                                                                                             'country'],
                                                                                                         list_check[
                                                                                                             'date'],
                                                                                                         list_check[
                                                                                                             'transport'],
                                                                                                         list_check[
                                                                                                             'from_is'],
                                                                                                         list_check[
                                                                                                             'to_is'],
                                                                                                         list_check[
                                                                                                             'cargo'],
                                                                                                         list_check[
                                                                                                             'pay'],
                                                                                                         list_check[
                                                                                                             'contacts']),
                              reply_markup=kb)
    # Грузы партнеров
    if call.data == 'cargo_users':
        kb = InlineKeyboardMarkup()
        start = InlineKeyboardButton('Начать мониторинг', callback_data='start')
        stop = InlineKeyboardButton('Закончить мониторинг', callback_data='stop')
        add_url = InlineKeyboardButton('Добавить ссылку', callback_data='add_url')
        remove_url = InlineKeyboardButton('Удалить ссылки', callback_data='remove_url')
        menu = InlineKeyboardButton('Меню', callback_data='menu')
        kb.add(add_url, remove_url)
        status = db_bot.get_id_tg_info(str(call.message.chat.id))
        if int(status['status_monit_two']) == 1:
            kb.add(start)
            kb.add(menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Меню '
                                                                                                         'управлением '
                                                                                                         'мониторингом '
                                                                                                         'грузов '
                                                                                                         'пользователей',
                                  reply_markup=kb)
        if int(status['status_monit_two']) == 0:
            kb.add(stop)
            kb.add(menu)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Меню '
                                                                                                         'управлением '
                                                                                                         'мониторингом '
                                                                                                         'грузов '
                                                                                                         'пользователей\nИдёт мониторинг.',
                                  reply_markup=kb)
    if call.data == 'remove_url':
        urls = db_bot.get_cargo_url(str(call.message.chat.id))
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
        for url in urls:
            delete_url = InlineKeyboardButton(url['name'], callback_data=str(url['id']) + '_re')
            manage.list_delete_url_next.append(str(url['id']) + '_re')
            kb.add(delete_url)
        kb.add(cargo_users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Нажмите для удаления',
                              reply_markup=kb)
    if call.data in manage.list_delete_url_next:
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
        kb.add(cargo_users)
        id_url = call.data.split('_')[0]
        db_bot.delete_cargo_url(id_url)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Успешно удалено.',
                              reply_markup=kb)
    if call.data == 'stop':
        db_bot.update_status_two('1', str(call.message.chat.id))
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
        kb.add(cargo_users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Мониторинг закончен.', reply_markup=kb)
    if call.data == 'add_url':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Введите ссылку(Грузы партнеров):')
        bot.register_next_step_handler(msg, add_url_step)
    if call.data == 'start':
        on_off = {}
        db_bot.update_status_two('0', str(call.message.chat.id))
        status = db_bot.get_id_tg_info(str(call.message.chat.id))
        on_off[str(status['ids_tg'])] = int(status['status_monit_two'])
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
        kb.add(cargo_users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Мониторинг начался.',
                              reply_markup=kb)
        while on_off[str(call.message.chat.id)] == 0:
            list_url = db_bot.get_cargo_url(str(call.message.chat_id))
            if list_url is None or str(list_url) == '()':
                kb = InlineKeyboardMarkup()
                add_url = InlineKeyboardButton('Добавить ссылку', callback_data='add_url')
                kb.add(add_url)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Добавте '
                                                                                                             'хоть одну '
                                                                                                             'ссылку.',
                                      reply_markup=kb)
            if list_url is not None and str(list_url) != '()':
                list_upload_url = []
                for data in list_url:
                    list_upload_url.append(data['url'])
                list_write_all = pars_lardi.get_cargo(list_upload_url, str(call.message.chat.id))
                for URL in list_write_all:
                    kb = InlineKeyboardMarkup()
                    list_check = db_bot.get_cargo_info(URL)
                    open_full_info = InlineKeyboardButton('Подробнее',
                                                          callback_data=str(list_check['id']))
                    open_lardi = InlineKeyboardButton('Открыть', url=list_check['url'])
                    manage.list_open_info.append(str(list_check['id']))
                    kb.add(open_full_info, open_lardi)
                    try:
                        bot.send_message(list_check['tg_id'], list_check['name'], reply_markup=kb)
                    except:
                        pass
            print('круг')
            time.sleep(60)
    if str(call.data) in manage.list_open_info:
        kb = InlineKeyboardMarkup()
        name = call.data
        list_check = db_bot.get_cargo_info_by_id(name)
        open_lardi = InlineKeyboardButton('Открыть на ларди', url=list_check['url'])
        kb.add(open_lardi)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=list_check[
                                                                                                         'name'] + '\n\nСтраны/Тип:\n%s\n\nДата:\n%s\n\nТранспорт:\n%s\n\nОткуда:\n%s\n\nКуда:\n%s\n\nГруз:\n%s\n'
                                                                                                                   '\nОплата:\n%s\n\nКонтакты:\n%s' % (
                                                                                                         list_check[
                                                                                                             'country'],
                                                                                                         list_check[
                                                                                                             'date'],
                                                                                                         list_check[
                                                                                                             'transport'],
                                                                                                         list_check[
                                                                                                             'from_is'],
                                                                                                         list_check[
                                                                                                             'to_is'],
                                                                                                         list_check[
                                                                                                             'cargo'],
                                                                                                         list_check[
                                                                                                             'pay'],
                                                                                                         list_check[
                                                                                                             'contacts']),
                              reply_markup=kb)


def add_url_step(message):
    URL = message.text
    try:
        if URL == '/start':
            kb = InlineKeyboardMarkup()
            cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
            kb.add(cargo_users)
            bot.send_message(message.chat.id, 'Отмена ввода, нажмите кнопку', reply_markup=kb)
        else:
            msg = bot.send_message(message.chat.id, 'Введите названия:')
            bot.register_next_step_handler(msg, add_url_step_2, URL)
    except:
        bot.send_message(message.chat.id, 'Ошибка добавления URL')


def add_url_step_2(message, URL):
    name = message.text
    try:
        if name == '/start':
            kb = InlineKeyboardMarkup()
            cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
            kb.add(cargo_users)
            bot.send_message(message.chat.id, 'Отмена ввода, нажмите кнопку', reply_markup=kb)
        else:
            db_bot.insert_cargo_url(URL, str(message.chat.id), name)
            kb = InlineKeyboardMarkup()
            cargo_users = InlineKeyboardButton('Назад', callback_data='cargo_users')
            kb.add(cargo_users)
            bot.send_message(message.chat.id, 'URL добавлен.', reply_markup=kb)
    except:
        bot.send_message(message.chat.id, 'Ошибка добавления URL')


def add_url_step_search(message):
    URL = message.text
    try:
        if URL.lower() == 'хуй':
            bot.send_message(message.chat.id, 'Сам хуй')
        if URL == '/start':
            kb = InlineKeyboardMarkup()
            cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
            kb.add(cargo_users)
            bot.send_message(message.chat.id, 'Отмена ввода, нажмите кнопку', reply_markup=kb)
        if URL.split('/')[3] == 'gruz' or URL.split('/')[3] == 'user' or URL.split('/')[3] == 'trans':
            msg = bot.send_message(message.chat.id, 'Введите название:')
            bot.register_next_step_handler(msg, add_url_step_search_2, URL)
    except:
        kb = InlineKeyboardMarkup()
        cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
        kb.add(cargo_users)
        bot.send_message(message.chat.id, 'Ошибка добавления URL', reply_markup=kb)


def add_url_step_search_2(message, URL):
    name = message.text
    try:
        if name == '/start':
            kb = InlineKeyboardMarkup()
            cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
            kb.add(cargo_users)
            bot.send_message(message.chat.id, 'Отмена ввода, нажмите кнопку', reply_markup=kb)
        else:
            db_bot.insert_cargo_url_search(URL, str(message.chat.id), name)
            kb = InlineKeyboardMarkup()
            cargo_users = InlineKeyboardButton('Назад', callback_data='menu')
            kb.add(cargo_users)
            bot.send_message(message.chat.id, 'URL добавлен.', reply_markup=kb)
    except:
        bot.send_message(message.chat.id, 'Ошибка добавления URL')


bot.polling()
