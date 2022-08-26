# -*- coding: utf-8 -*-
import telebot
from telebot import types
from crconfig import TOKEN, emoji, MONGO_TOKEN
from requests import exceptions
from pymongo import MongoClient
from random import randint
from telebot.apihelper import ApiTelegramException
from datetime import datetime
bot = telebot.TeleBot(TOKEN)

mongo = MongoClient(MONGO_TOKEN, port=27017)
#mongo=MongoClient('localhost', port=27017)
telebot = mongo["Telegrambot"]
usrs = telebot["Users"]
admins = telebot["Admins"]
sponsors = telebot["Sponsors"]
#check_ref = telebot["Checking refs"]
out_req = telebot['Withdraw']
spons_users = telebot['Sponsors Users']
settings=telebot['Settings']
bans = telebot['Bans']
comp = telebot['Completed Withdraws']

@bot.message_handler(commands=["start"])
def start_command_handler(message):
    FOUND = True
    user_id = message.chat.id
    ref_st = message.text
    for p in usrs.find({}, {'tgid': 1}):
        if p['tgid'] == message.chat.id:
            FOUND = False
            break
    if FOUND:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Надіслати номер телефону", request_contact=True)
        keyboard.add(button_phone)
        s = bot.send_message(message.chat.id, 'Для продовження поділіться своїм номером телефону',
                             reply_markup=keyboard)
        def login(message):
            try:
                if int(message.contact.phone_number[1:4]) == 380 or int(message.contact.phone_number[0:3]) == 380:
                    bot.send_message(message.chat.id, 'Чудово! Пройдемо далі')
                    captcha(message)
                else:
                    bot.send_message(message.chat.id, 'На жаль, ми працюємо лише з українськими номерами')
            except Exception:
                bot.send_message(message.chat.id, emoji['vosk'] + ' Натисніть на кнопку нижче')
                start_command_handler(message)
        bot.register_next_step_handler(s, login)
        def check_captcha(message, k):
            if k == 1:
                if message.text == '102':
                    res = usrs.insert_one({'tgid': message.chat.id, 'bal': 0, 'ref': 0,'bet':0.1,'get':0,'kon':0})
                    ref(message, ref_st)
                else:
                    bot.send_message(message.chat.id, 'Невірна капча!')
                    captcha(message)
            elif k == 2:
                if message.text == '54':
                    res = usrs.insert_one({'tgid': message.chat.id, 'bal': 0, 'ref': 0,'bet':0.1,'get':0,'kon':0})
                    ref(message, ref_st)
                else:
                    bot.send_message(message.chat.id, 'Невірна капча!')
                    captcha(message)
            elif k == 3:
                if message.text == '56':
                    res = usrs.insert_one({'tgid': message.chat.id, 'bal': 0, 'ref': 0,'bet':0.1,'get':0,'kon':0})
                    ref(message, ref_st)
                else:
                    bot.send_message(message.chat.id, 'Невірна капча!')
                    captcha(message)
            elif k == 4:
                if message.text == '82':
                    res = usrs.insert_one({'tgid': message.chat.id, 'bal': 0, 'ref': 0,'bet':0.1,'get':0,'kon':0})
                    ref(message, ref_st)
                else:
                    bot.send_message(message.chat.id, 'Невірна капча!')
                    captcha(message)
        def captcha(message):
            k = randint(1, 4)
            ex = ''
            if k == 1:
                ex = f"{emoji['5']}{emoji['1']}*{emoji['2']}"  # 102
                b1 = 102
                b2 = 88
                b3 = 110
            elif k == 2:
                ex = f"{emoji['8']}{emoji['4']}-{emoji['3']}{emoji['0']}"  # 54
                b1 = 20
                b2 = 59
                b3 = 54
            elif k == 3:
                ex = f"{emoji['7']}*{emoji['8']}"  # 56
                b1 = 48
                b2 = 3
                b3 = 56
            else:
                ex = f"{emoji['6']}{emoji['7']}+{emoji['1']}{emoji['5']}"  # 82
                b1 = 82
                b2 = 136
                b3 = 40
            mu_c = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            mu_c.add(str(b1), str(b2), str(b3))
            l = bot.send_message(message.chat.id, f'Необходимо пройти капчу\n\n{ex}', reply_markup=mu_c)
            bot.register_next_step_handler(l, check_captcha, k)
        def ref(message, ref_st):
            if " " in ref_st:
                ref_candidate = ref_st.split()[1]
            try:
                ref_candidate = int(ref_candidate)
                if message.chat.id != ref_candidate:
                    link = f'<a href="tg://user?id={ref_candidate}">USER</a>'
                    bot.send_message(message.chat.id, f'Ви були запрошені {link}', parse_mode='HTML')
                    for n in settings.find({}, {'ref': 1}):
                        ref_rew = float(n['ref'])
                        break

                    for i in usrs.find({}, {'tgid': 1,'bal':1,'ref':1}):
                        if i['tgid']==ref_candidate:
                            usrs.update_one({'tgid': message.chat.id},
                                            {"$set": {'pr': ref_candidate}})
                            break
                else:
                    bot.send_message(message.chat.id, 'Неможна запрошувати самого себе :)')
            except ValueError and UnboundLocalError:
                pass

            def check_ch(message):
                def ch(message):
                    tr = True
                    trsp = True
                    for i in sponsors.find({}, {'_id': 1, 'id': 1, 'nick': 1, 'sub': 1}):
                        try:
                            if i['id'] != 5527613532:
                                st = bot.get_chat_member(i['id'], message.chat.id).status
                                if st == 'member' or st == 'creator' or st == 'administrator':
                                    tr = True
                                else:
                                    tr = False
                                    return False
                                    break
                        except Exception as e:
                            bot.send_message(871076127, e)
                            if message.chat.id == 5288413290 or message.chat.id == 871076127:
                                bot.send_message(5288413290, e)
                                return True
                            else:
                                return False
                            break
                    if tr:
                        return True

                if ch(message):
                    for l in usrs.find({}, {'tgid': 1, 'bal': 1, 'pr': 1, 'get': 1}):
                        if l['tgid'] == message.chat.id:
                            if l['get'] == 0:
                                try:
                                    for n in settings.find({}, {'ref': 1}):
                                        ref_rew = float(n['ref'])
                                        break
                                    usrs.update_one({'tgid': message.chat.id},
                                                    {"$set": {'get': 1}})
                                    for u in usrs.find({}, {'tgid': 1, 'bal': 1, 'pr': 1, 'ref': 1,'kon':1}):
                                        if l['pr'] == u['tgid']:
                                            usrs.update_one({'tgid': l['pr']},
                                                            {"$set": {'ref': u['ref'] + 1,
                                                                      'bal': round(u['bal'] + ref_rew, 3)}})
                                            try:
                                                kn=u['kon']
                                                usrs.update_one({'tgid': l['pr']},
                                                            {"$set": {'kon': kn + 1}})
                                            except Exception as e:
                                                usrs.update_one({'tgid': l['pr']},
                                                            {"$set": {'kon':1}})
                                                print(e)
                                            break
                                    bot.send_message(ref_candidate, emoji['inf'] + f'@{message.from_user.username} підписався на спонсорів, Вам додано на баланс {ref_rew} USDT')
                                except Exception as e:
                                    print(e)
                            break
                    b = [emoji["monbag"] + ' Мій кабінет', emoji['party'] + ' Конкурс', emoji["fl"] + ' Вивід',
                         emoji['peop'] + ' Підтримка', emoji['joy'] + ' Ігри', emoji['monbag'] + ' Виплати', emoji['vosk'] + ' Як заробити']
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(b[0])
                    markup.add(b[1], b[2])
                    markup.add(b[3], b[4])
                    markup.add(b[5], b[6])
                    send = bot.send_message(message.chat.id, "Оберіть пункт меню:", reply_markup=markup)
                else:
                    inline_k = types.InlineKeyboardMarkup()
                    c = 1
                    for i in sponsors.find({}, {'nick': 1}):
                        if i['nick'][len(i['nick']) - 3:len(i['nick'])] == 'bot' or i['nick'][
                                                                                    len(i['nick']) - 3:len(
                                                                                        i['nick'])] == 'Bot':
                            inline_bt = types.InlineKeyboardButton(f'Бот #{c} (натисніть /start)', callback_data='vip',
                                                                   url=f'https://t.me/{i["nick"]}')
                            inline_k.add(inline_bt)
                            c += 1
                        else:
                            inline_bt = types.InlineKeyboardButton(f'Канал #{c}', callback_data='vip',
                                                                   url=f'https://t.me/{i["nick"]}')
                            inline_k.add(inline_bt)
                            c += 1
                    mu_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    mu_check.add('Підписався ' + emoji['yep'])
                    o = bot.send_message(message.chat.id,
                                         f'{emoji["redcr"]}', reply_markup=mu_check)
                    bot.send_message(message.chat.id, f'Канали:', reply_markup=inline_k)
                    bot.register_next_step_handler(o, check_ch)

            check_ch(message)

    else:
        b = [emoji["monbag"] + ' Мій кабінет', emoji['party'] + ' Конкурс', emoji["fl"] + ' Вивід',
                         emoji['peop'] + ' Підтримка', emoji['joy'] + ' Ігри', emoji['monbag'] + ' Виплати', emoji['vosk'] + ' Як заробити']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(b[0])
        markup.add(b[1], b[2])
        markup.add(b[3], b[4])
        markup.add(b[5], b[6])
        send = bot.send_message(message.chat.id, "Оберіть пункт меню:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start_command_handler(message):
    # global ref_st
    user_id = message.from_user.id
    # ref = None
    FOUND = True
    def mu(message):
        b = [emoji["monbag"] + ' Мій кабінет', emoji['party'] + ' Конкурс', emoji["fl"] + ' Вивід',
                         emoji['peop'] + ' Підтримка', emoji['joy'] + ' Ігри', emoji['monbag'] + ' Виплати', emoji['vosk'] + ' Як заробити']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(b[0])
        markup.add(b[1], b[2])
        markup.add(b[3], b[4])
        markup.add(b[5], b[6])
        send = bot.send_message(message.chat.id, "Оберіть пункт меню:", reply_markup=markup)
    def admink(message):
        def adding(message):
            if message.text == emoji['back'] + ' Назад':
                admin_panel(message)
            elif len(message.text) == 9 or len(message.text) == 10:
                try:
                    if isinstance(int(message.text), int):
                        tr = True
                        for i in admins.find({}, {'tgid': 1}):
                            if i['tgid'] == message.text:
                                bot.send_message(message.chat.id, 'Цей користувач вже є адміном!')
                                tr = False
                                break
                        if tr:
                            res = admins.insert_one({'tgid': int(message.text)})
                            bot.send_message(message.chat.id, 'Користувач є адміном ' + emoji['yep'])
                            bot.send_message(int(message.text), f'Ви теперь админ {emoji["yep"]}\n\nДля використання введіть admin або /admin')
                        admin_panel(message)
                except TypeError:
                    pass

        def deleting(message):
            if message.text == emoji['back'] + ' Назад':
                admin_panel(message)
            elif len(message.text) == 9 or len(message.text) == 10:
                try:
                    if isinstance(int(message.text), int):
                        tr = True
                        for i in admins.find({}, {'tgid': 1}):
                            if i['tgid'] == message.text:
                                tr = False
                                admins.delete_one(i)
                                bot.send_message(message.chat.id, 'Користувач більше не є адміном ' + emoji['yep'])
                                break
                        if tr:
                            bot.send_message(message.chat.id, 'Користувач не є адміном!')
                        admin_panel(message)
                except TypeError:
                    pass
        def nick_sp(message, tgid):
            if message.text == emoji['back'] + ' Назад':
                admin_panel(message)
            else:
                res = sponsors.insert_one({'id': tgid, 'nick': message.text, 'sub': ['871076127']})
                bot.send_message(message.chat.id, 'Канал є спонсором ' + emoji['yep'])
                admin_panel(message)
        def add_sp(message):
            if message.text == emoji['back'] + ' Назад':
                admin_panel(message)
            else:
                try:
                    if isinstance(int(message.text), int):
                        tr = True
                        try:
                            for i in sponsors.find({}, {'id': 1}):
                                if int(i['id']) == int(message.text):
                                    bot.send_message(message.chat.id, 'Цей канал вже є спонсором!')
                                    tr = False
                                    break
                        except Exception:
                            pass
                        if tr:
                            tgid = int(message.text)
                            markup_add = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            markup_add.add(emoji['back'] + ' Назад')
                            k = bot.send_message(message.chat.id, 'Введіть nickname каналу (без @)',
                                                 reply_markup=markup_add)
                            bot.register_next_step_handler(k, nick_sp, tgid)
                except Exception as e:
                    pass
        def del_sp(message):
            if message.text == emoji['back'] + ' Назад':
                admin_panel(message)
            else:
                try:
                    if isinstance(int(message.text), int):
                        tru = True
                        for i in sponsors.find({}, {'id': 1}):
                            if int(i['id']) == int(message.text):
                                sponsors.delete_one(i)
                                bot.send_message(message.chat.id, 'Канал більше не є спонсором ' + emoji['yep'])
                                tru = False
                                #bot.send_message(871076127, 'del1')
                                break
                        if tru:
                            bot.send_message(message.chat.id, 'Цей канал не є спонсором!')
                        admin_panel(message)
                except Exception:
                    pass

        def bck(message):
            admin_panel(message)

        def add_spk(message):
            if message.text == emoji["back"] + " Назад":
                admin_panel(message)
            else:
                try:
                    if isinstance(int(message.text), int):
                        tr = True
                        try:
                            for i in spons_users.find({}, {'id': 1}):
                                if int(i['id']) == int(message.text):
                                    bot.send_message(message.chat.id, 'Цей користувач вже є спонсором!')
                                    tr = False
                                    break
                        except Exception:
                            pass
                        if tr:
                            tgid = int(message.text)
                            markup_add = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            markup_add.add(emoji['back'] + ' Назад')
                            bot.send_message(message.chat.id, 'Користувач є спонсором ' + emoji['yep'],
                                             reply_markup=markup_add)
                            res = spons_users.insert_one({'id': int(message.text)})
                        admin_panel(message)
                except Exception as e:
                    pass

        def del_spk(message):
            if message.text == emoji["back"] + " Назад":
                admin_panel(message)
            else:
                try:
                    if isinstance(int(message.text), int):
                        tru = True
                        for i in spons_users.find({}, {'id': 1}):
                            if int(i['id']) == int(message.text):
                                spons_users.delete_one(i)
                                bot.send_message(message.chat.id, 'Користувач більше не є спонсором ' + emoji['yep'])
                                tru = False
                                break
                        if tru:
                            bot.send_message(message.chat.id, 'Цей користувач не є спонсором!')
                        admin_panel(message)
                except Exception:
                    pass

        def mail_end(message, txt):
            if message.text == 'ПІДТВЕРДИТИ':
                for i in usrs.find({}, {'tgid': 1}):
                    try:
                        bot.send_message(i['tgid'], txt)
                    except Exception:
                        pass
                bot.send_message(message.chat.id, 'Розсилання закінчено ' + emoji['yep'])
                admin_panel(message)
            elif message.text == emoji["back"] + " Назад":
                admin_panel(message)
            else:
                bot.send_message(message.chat.id, 'Відхилено')
                admin_panel(message)
        def mailing(message):
            markup_add = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup_add.add(emoji['back'] + ' Назад')
            if message.text == emoji["back"] + " Назад":
                admin_panel(message)
            else:
                txt = str(message.text)
                k = bot.send_message(message.chat.id, 'Введіть ПІДТВЕРДИТИ, щоб продовжити розсилання',
                                     reply_markup=markup_add)
                bot.register_next_step_handler(k, mail_end, txt)
        def out_new(message):
            try:
                if isinstance(float(message.text), float):
                    for l in settings.find({}, {'out': 1}):
                        settings.update_one({'out': l['out']}, {"$set": {'out':float(message.text)}})
                        bot.send_message(message.chat.id,'Успішно відновлено '+emoji['yep'])
                        sett(message)
                        break

                    #for l in settings.find({}, {'out': 1}):
                        #min_out = float(i['out'])
                        #ref_rew = float(i['ref'])
            except Exception:
                sett(message)
        def ref_new(message):
            try:
                if isinstance(float(message.text), float):
                    for l in settings.find({}, {'ref': 1}):
                        settings.update_one({'ref': l['ref']}, {"$set": {'ref':float(message.text)}})
                        bot.send_message(message.chat.id,'Успішно відновлено '+emoji['yep'])
                        sett(message)
                        break
            except Exception:
                sett(message)
        def sett_ch(message):
            if message.text==emoji['back'] + ' Назад':
                admin_panel(message)
            elif message.text=='Мін. вивід':
                k=bot.send_message(message.chat.id,'Введіть нову мінімальну суму для виведення')
                bot.register_next_step_handler(k, out_new)
            elif message.text=='Нагорода за реф.':
                k=bot.send_message(message.chat.id,'Введіть нову нагороду за реферала')
                bot.register_next_step_handler(k, ref_new)
            else:
                bot.send_message(message.chat.id,'Не розумію Вас '+emoji['bor'])
                sett(message)
        def ban(message):
            try:
                if message.text == emoji["back"] + ' Назад':
                    admin_panel(message)
                else:
                    tr = False
                    for i in bans.find({}, {'tgid': 1}):
                        if i['tgid'] == int(message.text):
                            tr = True
                            break
                    if tr:
                        bot.send_message(message.chat.id, 'Користувач вже в бані')
                    else:
                        bans.insert_one({'tgid': int(message.text)})
                        bot.send_message(message.chat.id, f'Користувача забанено {emoji["yep"]}')
                        admin_panel(message)
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, 'Невірний формат')
                admin_panel(message)

        def unban(message):
            try:
                if message.text == emoji["back"] + ' Назад':
                    admin_panel(message)
                else:
                    tr = True
                    for i in bans.find({}, {'tgid': 1}):
                        if i['tgid'] == int(message.text):
                            tr = False
                            break
                    if tr:
                        bot.send_message(message.chat.id, 'Користувач не знаходиться в бані')
                    else:
                        bans.delete_one({'tgid': int(message.text)})
                        bot.send_message(message.chat.id, f'Користувача розбанено {emoji["yep"]}')
                        admin_panel(message)
            except Exception:
                bot.send_message(message.chat.id, 'Невірний формат')
                admin_panel(message)

        def banun(message):
            if message.text == emoji["back"] + ' Назад':
                admin_panel(message)
            elif message.text == emoji["red"] + ' Забанити':
                k = bot.send_message(message.chat.id, 'Введіть Telegram ID', reply_markup=markup_add)
                bot.register_next_step_handler(k, ban)
            elif message.text == emoji["green"] + ' Розбанити':
                k = bot.send_message(message.chat.id, 'Введіть Telegram ID', reply_markup=markup_add)
                bot.register_next_step_handler(k, unban)
        def sett(message):
            markup_set = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup_set.add('Мін. вивід','Нагорода за реф.')
            markup_set.add(emoji['back'] + ' Назад')
            k=bot.send_message(message.chat.id,'Оберіть:',reply_markup=markup_set)
            bot.register_next_step_handler(k,sett_ch)
        def ref_zero(message):
            if message.text=='Продовжити':
                bot.send_message(message.chat.id,'Очікуйте...')
                for i in usrs.find({}, {'tgid': 1}):
                    usrs.update_one({'tgid': i['tgid']}, {"$set": {'kon': 0}})
                bot.send_message(message.chat.id,'Анульовано '+emoji['yep'])
                sett(message)
            else:
                sett(message)
        def adding_bal(message, balan, tgid):
            try:
                if message.text == emoji['back'] + ' Назад':
                    admin_panel(message)
                elif isinstance(float(message.text), float):
                    usrs.update_one({'tgid': tgid}, {"$set": {'bal': balan + float(message.text)}})
                    bot.send_message(message.chat.id, 'Баланс поповнено ' + emoji['yep'])
                    bot.send_message(tgid, f'Ваш баланс поповнено на {message.text} USDT {emoji["star"]}')
                    admin_panel(message)
                else:
                    admin_panel(message)
            except Exception as e:
                admin_panel(message)
        def add_bal(message):
            try:
                if message.text == emoji['back'] + ' Назад':
                    admin_panel(message)
                elif isinstance(int(message.text), int):
                    for u in usrs.find({}, {'tgid': 1, 'bal': 1}):
                        if u['tgid'] == int(message.text):
                            balan = float(u['bal'])
                            tgid = int(u['tgid'])
                            k = bot.send_message(message.chat.id,
                                                 f'{emoji["man"]} Користувач - <a href="tg://user?id={tgid}">USER</a>\n{emoji["monbag"]} Баланс - {balan} USDT\n\n{emoji["tri"]}Введіть сумму, яку хочете додати до баланса',
                                                 parse_mode="HTML", reply_markup=markup_add)
                            bot.register_next_step_handler(k, adding_bal, balan, tgid)
                            break
                else:
                    admin_panel(message)
            except Exception:
                bot.send_message(message.chat.id, 'Невірний TelegramID ' + emoji['red'])
                admin_panel(message)
        def maorbis(message):
            if message.text == emoji["back"] + ' Назад':
                admin_panel(message)
            elif message.text == 'Основний':
                k = bot.send_message(message.chat.id, 'Введіть TgID користувача', reply_markup=markup_add)
                bot.register_next_step_handler(k, add_bal)
            else:
                admin_panel(message)
        markup_add = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_add.add(emoji['back'] + ' Назад')
        if message.text == emoji['green'] + ' Додати адміна':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID користувача', reply_markup=markup_add)
            bot.register_next_step_handler(k, adding)
        elif message.text == emoji['red'] + ' Видалити адміна':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID користувача', reply_markup=markup_add)
            bot.register_next_step_handler(k, deleting)
        elif message.text == emoji['fl'] + ' Виведення':
            approving_out_admin(message)
        elif message.text == emoji['green'] + ' Додати спонсора':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID спонсора (каналу)', reply_markup=markup_add)
            bot.register_next_step_handler(k, add_sp)
        elif message.text == emoji['paper'] + ' Всі спонсори':
            txt = ''
            c = 1
            for i in sponsors.find({}, {'id': 1, 'nick': 1}):
                txt += f"{c}. <a href='https://t.me/{i['nick']}'>Channel №{c}</a>\nID = {i['id']}\n"
                c += 1
            try:
                k = bot.send_message(message.chat.id, txt, parse_mode='HTML', reply_markup=markup_add)
            except Exception:
                k = bot.send_message(message.chat.id, 'Спонсорів немає!', parse_mode='HTML', reply_markup=markup_add)
            bot.register_next_step_handler(k, bck)
        elif message.text == emoji['red'] + ' Видалити спонсора':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID спонсора (каналу)', reply_markup=markup_add)
            bot.register_next_step_handler(k, del_sp)
        elif message.text == emoji['green'] + ' Додати користувача-спонсора':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID спонсора (користувача)', reply_markup=markup_add)
            bot.register_next_step_handler(k, add_spk)
        elif message.text == emoji['red'] + ' Видалити користувача-спонсора':
            k = bot.send_message(message.chat.id, 'Введіть TelegramID спонсора (користувача)', reply_markup=markup_add)
            bot.register_next_step_handler(k, del_spk)
        elif message.text == emoji['paper'] + ' Всі користувачі-спонсори':
            txt = ''
            c = 1
            for i in spons_users.find({}, {'id': 1}):
                link = f"<a href='tg://user?id={int(i['id'])}'>USER #{c}</a> - {i['id']}\n"
                txt += link
                c += 1
            k = bot.send_message(message.chat.id, txt, parse_mode='HTML', reply_markup=markup_add)
            bot.register_next_step_handler(k, bck)
        elif message.text == emoji["mai"] + ' Розсилання':
            k = bot.send_message(message.chat.id, 'Напишіть текст для розсилки користувачам ' + emoji['mai'],
                                 reply_markup=markup_add)
            bot.register_next_step_handler(k, mailing)
        elif message.text==emoji['gear']+' Налаштування':
            sett(message)
        elif message.text==emoji['stat']+' Статистика':
            k=bot.send_message(message.chat.id, f'Статистика {emoji["stat"]}\n\n{emoji["fire"]} Користувачів в боті - {len(list(usrs.find({}, {"_id": 1})))}')
            bot.register_next_step_handler(k,admink)
        elif message.text == emoji["redc"] + ' Бан':
            muban = types.ReplyKeyboardMarkup(resize_keyboard=True)
            muban.add(emoji["red"] + ' Забанити', emoji["green"] + ' Розбанити')
            muban.add(emoji['back'] + ' Назад')
            k = bot.send_message(message.chat.id, 'Забанити чи розбанити користувача?', reply_markup=muban)
            bot.register_next_step_handler(k, banun)
        elif message.text=='Ануляція рефералів':
            markup_se = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup_se.add('Продовжити')
            markup_se.add('Назад')
            k = bot.send_message(message.chat.id, 'Впевнені, що хочете анулювати к-сть рефералів?',
                                 reply_markup=markup_se)
            bot.register_next_step_handler(k, ref_zero)
        elif message.text==emoji['monbag'] + ' Баланс':
            markup_ad = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup_ad.add('Основний')
            markup_ad.add(emoji['back'] + ' Назад')
            k = bot.send_message(message.chat.id, 'Який баланс хочете поповнити?', reply_markup=markup_ad)
            bot.register_next_step_handler(k, maorbis)
        elif message.text == emoji['back'] + ' Головне меню':
            mu(message)
        else:
            bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
            admin_panel(message)
    def admin_panel(message):
        markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_admin.add(emoji['fl'] + ' Виведення','Ануляція рефералів',emoji['monbag'] + ' Баланс')
        markup_admin.add(emoji["mai"] + ' Розсилання',emoji['gear']+' Налаштування',emoji['redc']+' Бан')
        markup_admin.add(emoji['green'] + ' Додати адміна', emoji['red'] + ' Видалити адміна')
        markup_admin.add(emoji['green'] + ' Додати спонсора', emoji['paper'] + ' Всі спонсори',
                         emoji['red'] + ' Видалити спонсора')
        markup_admin.add(emoji['back'] + ' Головне меню')
        t = bot.send_message(message.chat.id, 'Оберіть пункт меню', reply_markup=markup_admin)
        bot.register_next_step_handler(t, admink)

    def sponsk(message):
        if message.text == emoji['back'] + ' Головне меню':
            mu(message)
        elif message.text == emoji['paper'] + ' Переглянути статистику':
            txt = f'Усього перейшло з бота до каналу:\n\n'
            for i in sponsors.find({}, {'nick': 1, 'sub': 1}):
                us_res = []
                users_li = i['sub']
                for k in users_li:
                    if k not in us_res:
                        us_res.append(k)
                txt += f"@{i['nick']} - {len(us_res)} subs\n"
            l = bot.send_message(message.chat.id, txt)
            bot.register_next_step_handler(l, sponsk)
        else:
            bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
            spons_panel(message)

    def spons_panel(message):
        markup_spons = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_spons.add(emoji['paper'] + ' Переглянути статистику')
        markup_spons.add(emoji['back'] + ' Головне меню')
        t = bot.send_message(message.chat.id, 'Оберіть пункт меню:', reply_markup=markup_spons)
        bot.register_next_step_handler(t, sponsk)

    def choosing_admin(message):
        out_req_comp = telebot['Completed Withdraws']
        req = list(out_req.find({}, {"tgid": 1, 'Adress': 1, 'Sum': 1}))
        if message.text == emoji["yep"] + " Підтвердити":
            now = datetime.now()
            current_time1 = int(now.strftime("%H")) + 3
            current_time2 = int(now.strftime("%M"))
            dt=f'{current_time1}:{current_time2}'
            completed_req = {"tgid": req[0]["tgid"], 'Adress': req[0]["Adress"],"Sum": req[0]["Sum"]}
            completed_req1 = {"tgid": req[0]["tgid"], 'Adress': req[0]["Adress"], "Sum": req[0]["Sum"], 'Time': dt}
            out_req.delete_one(completed_req)
            res = out_req_comp.insert_one(completed_req1)
            bot.send_message(message.chat.id, "Запит підтверждено")
            bot.send_message(completed_req['tgid'],
                             f"{emoji['rocket']} Ваш запит підтверждено. \nОчікуйте на надходження коштів {emoji['star']}")
            approving_out_admin(message)
        elif message.text == emoji['redc'] + " Відхилити":
            completed_req = {"tgid": req[0]["tgid"], 'Adress': req[0]["Adress"],
                             "Sum": req[0]["Sum"]}
            out_req.delete_one(completed_req)
            bot.send_message(message.chat.id, "Запит відхилено")
            for us in usrs.find({}, {'_id': 1, 'tgid': 1, "bal": 1, 'ref': 1}):
                if us['tgid'] == message.chat.id:
                    suma = us['bal']
                    # new_us = {'_id': us['_id'], 'tgid': us['tgid'], 'bal': req[0]['Sum'], 'ref': us['ref']}
                    # usrs.delete_one(us)
                    # res = usrs.insert_one(new_us)
                    usrs.update_one({'_id': us['_id']}, {"$set": {'bal': round(us['bal'] + req[0]['Sum'],2)}})
            bot.send_message(completed_req['tgid'],
                             f"Ваш  запит відхилено :(\nМожливо, Ви надали хибну інформацію або порушили правила нашого бота\nДля більш детальної інформації звертайтесь до адміністратора")
            approving_out_admin(message)
        elif message.text == emoji['back'] + " Назад":
            admin_panel(message)

    def approving_out_admin(message):
        req = list(out_req.find({}, {"tgid": 1, 'Adress': 1, 'Sum': 1, 'Refs': 1}))
        markup_ap = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_ap.add(emoji["yep"] + ' Підтвердити', emoji['redc'] + " Відхилити", emoji["back"] + " Назад")
        def backm(message):
            if message.text == emoji["back"] + " Назад":
                admin_panel(message)
        try:
            if len(req) == 1:
                bot.send_message(message.chat.id, f"У вас 1 новий запит")
            elif len(req) > 1:
                bot.send_message(message.chat.id, f"У вас {len(req)} нових запитів")
            link = f'<a href="tg://user?id={req[0]["tgid"]}">USER</a>'
            req_txt = f'User ID: {req[0]["tgid"]}\nUser: {link}\nГаманець: {req[0]["Adress"]}\nЗапросив: {req[0]["Refs"]}\nСума: {req[0]["Sum"]}'
            s = bot.send_message(message.chat.id, req_txt, reply_markup=markup_ap, parse_mode='HTML')
            bot.register_next_step_handler(s, choosing_admin)
        except IndexError:
            bot.send_message(message.chat.id, "Запитів немає!")
            admin_panel(message)

    def ask_mon(message):
        if message.text == emoji['back'] + ' Назад':
            mu(message)
        else:
            user_adress = str(message.text)
            for us in usrs.find({}, {'tgid': 1, "bal": 1}):
                if us['tgid'] == message.chat.id:
                    for l in settings.find({}, {'out': 1}):
                        min_out=l['out']
                        break
                    user_bal = us['bal']
                    m = bot.send_message(message.chat.id,
                                         f'{emoji["vosk"]} Введіть суму яку хочете вивести\n\n [Від {min_out} USDT]\n\n{emoji["dol"]} Ваш баланс {us["bal"]} USDT')
                    bot.register_next_step_handler(m, approving_out, user_adress, user_bal)
                    break
    def approving_out(message, user_adress, user_bal):
        try:
            if message.text == emoji['back'] + ' Назад':
                mu(message)
            elif isinstance(float(message.text), float):
                for i in settings.find({}, {'out': 1, 'ref': 1}):
                    min_out = float(i['out'])
                if user_bal >= float(message.text):
                    if float(message.text) >= min_out:
                        mb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        mb.add(emoji['back'] + ' Головне меню')
                        for us in usrs.find({}, {'_id': 1, 'tgid': 1, "bal": 1, 'ref': 1}):
                            if us['tgid'] == message.chat.id:
                                suma = float(message.text)
                                usrs.update_one({'_id': us['_id']}, {"$set": {'bal': round(us['bal'] - suma,2)}})
                                out_request = {'tgid': message.chat.id, 'Adress': user_adress, 'Refs': us['ref'],
                                               'Sum': suma}
                                res = out_req.insert_one(out_request)
                                break
                        p = bot.send_message(message.chat.id,
                                             'Ваша заявка успішно прийнята, та йде на обробку адміністратору ' + emoji[
                                                 'party'], reply_markup=mb)
                        bot.register_next_step_handler(p, back)
                    else:
                        bot.send_message(message.chat.id, emoji['vosk'] + f' Мінімальна сума для виведення - {min_out} USDT')
                        mu(message)
                else:
                    bot.send_message(message.chat.id, 'Недостатньо коштів ' + emoji['bor'])
                    mu(message)
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, emoji['vosk'] + ' Невірні данні!')
            mu(message)

    def back(message):
        if message.text == emoji['back'] + ' Назад':
            mu(message)
        elif message.text == emoji['back'] + ' Головне меню':
            mu(message)
        else:
            bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
            mu(message)
    def card(message):
        mb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mb.add(emoji['back'] + ' Назад')
        l = bot.send_message(message.chat.id, emoji['card'] + f'Введіть адресу Вашого електронного гаманця USDT\n\n{emoji["vosk"]} Мережа TRC - 20\n\n{emoji["monbag"]} Приклад:\n\nTRTa6jHTxhr47RdjolhNi7oYGLAxza3uT\n\n{emoji["sh"]} Гаманець можна знайти на крипто біржах, де і продати USDT',parse_mode='Markdown',reply_markup=mb)
        bot.register_next_step_handler(l, ask_mon)
    def coin_obr(message):
        if message.text==emoji['cas'] + ' До гри':
            casino_lobby(message)
        elif message.text==emoji['green'] + ' Зрозуміло!':
            casino_lobby(message)
    def bask_play(message):
        if message.text==emoji['back']+' Назад':
            casino_lobby(message)
        else:
            nxt = False
            for i in usrs.find({}, {'tgid': 1, 'bal': 1,'bet':1}):
                if i['tgid'] == message.chat.id:
                    if i['bal'] >= 0.1 and i['bal']>=i['bet']:
                        nxt = True
                    break
            try:
                for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                    try:
                        if n['tgid'] == message.chat.id:
                            bet = n['bet']
                            balance = n['bal']
                            break
                    except Exception as e:
                        pass
            except Exception as e:
                print(e)
                pass
            if nxt:
                try:
                    if message.forward_from == None:
                        if message.dice.emoji=='🏀':
                            bask = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            bask.add(emoji['bas'])
                            bask.add(emoji['back'] + ' Назад')
                            if message.dice.value == 4 or message.dice.value == 5:
                                u = bot.send_message(message.chat.id,
                                                     f'{emoji["sm"]}Перемога!\nСума виграшу - {round(bet * 1.8,2)} USDT\n\n{emoji["monbag"]} Баланс - {round(balance + bet*0.8,2)} USDT',
                                                     reply_markup=bask)
                                usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance + float(bet)*0.8,2)}})
                                # bot.send_message(message.chat.id, '')
                            else:
                                u = bot.send_message(message.chat.id,
                                                     f'{emoji["pain"]} Ви програли\n\n{emoji["monbag"]} Баланс - {round(balance - bet,2)} USDT',
                                                     reply_markup=bask)
                                usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance - float(bet),2)}})
                            bot.register_next_step_handler(u, bask_play)
                        else:
                            bot.send_message(message.chat.id, 'Не розумію Вас '+emoji['bor'])
                            casino_lobby(message)
                    else:
                        bot.send_message(message.chat.id,
                                         'Nice cheats!\n\nОтримуй свою нагороду за абуз ' + emoji['sm'])
                        usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': balance - 6.66}})
                        mu(message)
                except Exception:
                    #@bot.message_handler(content_types=['dice'])
                    bot.send_message(message.chat.id,'Не розумію Вас '+emoji['bor'])
                    casino_lobby(message)
            else:
                bot.send_message(message.chat.id, f'{emoji["vosk"]} На балансі недостатньо коштів, для продовження гри змініть суму ставки, або запросіть друзів {emoji["peop"]}')
                mu(message)
    def slots_play(message):
        if message.text==emoji['back']+' Назад':
            casino_lobby(message)
        else:
            nxt = False
            for i in usrs.find({}, {'tgid': 1, 'bal': 1,'bet':1}):
                if i['tgid'] == message.chat.id and i['bal']>=i['bet']:
                    if i['bal'] >= 0.1:
                        nxt = True
                    break
            try:
                for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                    try:
                        if n['tgid'] == message.chat.id:
                            bet = n['bet']
                            balance = n['bal']
                            break
                    except Exception as e:
                        pass
            except Exception as e:
                print(e)
                pass
            if nxt:
                try:
                    if message.forward_from == None:
                        if message.dice.emoji=='🎰':
                            sl = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            sl.add(emoji['cas'])
                            sl.add(emoji['back'] + ' Назад')
                            if message.dice.value == 22 or message.dice.value == 43 or message.dice.value == 1 or message.dice.value == 64:
                                u = bot.send_message(message.chat.id,
                                                     f'{emoji["sm"]}Перемога!\nСума виграшу - {round(bet * 6,2)} USDT\n\n{emoji["monbag"]} Баланс - {round(bet*5+balance,2)} USDT',
                                                     reply_markup=sl)
                                usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance + float(bet*5),2)}})
                                # bot.send_message(message.chat.id, '')
                            else:
                                u = bot.send_message(message.chat.id,
                                                     f'{emoji["pain"]} Ви програли\n\n{emoji["monbag"]} Баланс - {round(balance - bet,2)} USDT',
                                                     reply_markup=sl)
                                usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance - float(bet),2)}})
                            bot.register_next_step_handler(u, slots_play)
                        else:
                            bot.send_message(message.chat.id, 'Не розумію Вас '+emoji['bor'])
                            casino_lobby(message)
                    else:
                        bot.send_message(message.chat.id,
                                         'Nice cheats!\n\nОтримуй свою нагороду за абуз ' + emoji['sm'])
                        usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance - 6.66,2)}})
                        mu(message)
                except Exception:
                    #@bot.message_handler(content_types=['dice'])
                    bot.send_message(message.chat.id,'Не розумію Вас '+emoji['bor'])
                    casino_lobby(message)
            else:
                bot.send_message(message.chat.id, f'{emoji["vosk"]} На балансі недостатньо коштів, для продовження гри змініть суму ставки, або запросіть друзів {emoji["peop"]}')
                mu(message)
    def dice_res(message,val):
        if message.text==emoji['back']+' Назад':
            casino_lobby(message)
        else:
            nxt = False
            for i in usrs.find({}, {'tgid': 1, 'bal': 1,'bet':1}):
                if i['tgid'] == message.chat.id:
                    if i['bal'] >= 0.1 and i['bal']>=i['bet']:
                        nxt = True
                    break
            try:
                for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                    try:
                        if n['tgid'] == message.chat.id:
                            bet = n['bet']
                            balance = n['bal']
                            break
                    except Exception as e:
                        pass
            except Exception as e:
                print(e)
                pass
            if nxt:
                try:
                    if message.forward_from == None:
                        if message.dice.emoji=='🎲':
                            diceb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            diceb.add('1-3','4-6')
                            diceb.add(emoji['back'] + ' Назад')
                            if val=='1-3':
                                if message.dice.value==1 or message.dice.value==2 or message.dice.value==3:
                                    u = bot.send_message(message.chat.id,
                                                         f'{emoji["sm"]}Перемога!\nСума виграшу - {round(bet * 1.8,2)} USDT\n\n{emoji["monbag"]} Баланс - {round(bet * 0.8,2) + balance} USDT',
                                                         reply_markup=diceb)
                                    usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance + bet * 0.8,2)}})
                                else:
                                    u = bot.send_message(message.chat.id,
                                                         f'{emoji["pain"]} Ви програли\n\n{emoji["monbag"]} Баланс - {balance - bet} USDT',
                                                         reply_markup=diceb)
                                    usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance - float(bet),2)}})
                            elif val=='4-6':
                                if message.dice.value==4 or message.dice.value==5 or message.dice.value==6:
                                    u = bot.send_message(message.chat.id,
                                                         f'{emoji["sm"]}Перемога!\nСума виграшу - {round(bet * 1.8,2)} USDT\n\n{emoji["monbag"]} Баланс - {round(bet * 0.8,2) + balance} USDT',
                                                         reply_markup=diceb)
                                    usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': balance + round(bet * 0.8,2)}})
                                else:
                                    u = bot.send_message(message.chat.id,
                                                         f'{emoji["pain"]} Ви програли\n\n{emoji["monbag"]} Баланс - {balance - bet} USDT',
                                                         reply_markup=diceb)
                                    usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance - float(bet),2)}})
                            bot.register_next_step_handler(u, dice_play)
                        else:
                            #bot.send_message(message.chat.id, 'Не розумію Вас '+emoji['bor'])
                            casino_lobby(message)
                    else:
                        bot.send_message(message.chat.id,
                                         'Nice cheats!\n\nОтримуй свою нагороду за абуз ' + emoji['sm'])
                        usrs.update_one({'tgid': message.chat.id}, {"$set": {'bal': round(balance - 6.66, 2)}})
                        mu(message)
                except Exception as e:
                    print(e)
                    bot.send_message(message.chat.id,'Не розумію Вас '+emoji['bor'])
                    casino_lobby(message)
            else:
                bot.send_message(message.chat.id, f'{emoji["vosk"]} На балансі недостатньо коштів, для продовження гри змініть суму ставки, або запросіть друзів {emoji["peop"]}')
                mu(message)
    def dice_play(message):
        #if message.text==emoji['back']+' Назад':
        #    casino_lobby(message)
        nxt = False
        for i in usrs.find({}, {'tgid':1,'bal': 1,'bet':1}):
            if i['tgid']==message.chat.id:
                if i['bal'] >= 0.1 and i['bal']>=i['bet']:
                    nxt = True
                break
        if nxt:
            if message.text=='1-3':
                val = '1-3'
                try:
                    for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                        try:
                            if n['tgid'] == message.chat.id:
                                bet = n['bet']
                                balance = n['bal']
                                break
                        except Exception as e:
                            pass
                except Exception as e:
                    print(e)
                    pass
                diceb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                diceb.add(emoji['dice'])
                diceb.add(emoji['back'] + ' Назад')
                u = bot.send_message(message.chat.id, f'Натисніть "{emoji["dice"]}"', reply_markup=diceb)
                bot.register_next_step_handler(u, dice_res, val)
            elif message.text == '4-6':
                val = '4-6'
                try:
                    for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                        try:
                            if n['tgid'] == message.chat.id:
                                bet = n['bet']
                                balance = n['bal']
                                break
                        except Exception as e:
                            pass
                except Exception as e:
                    print(e)
                    pass
                diceb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                diceb.add(emoji['dice'])
                diceb.add(emoji['back'] + ' Назад')
                u = bot.send_message(message.chat.id, f'Натисніть "{emoji["dice"]}"', reply_markup=diceb)
                bot.register_next_step_handler(u, dice_res, val)
            elif message.text == emoji['back'] + ' Назад':
                casino_lobby(message)
            else:
                bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
                casino_lobby(message)
        else:
            bot.send_message(message.chat.id, f'{emoji["vosk"]} На балансі недостатньо коштів, для продовження гри змініть суму ставки, або запросіть друзів {emoji["peop"]}')
            mu(message)
    def casino(message):
        nxt=False
        for i in usrs.find({}, {'tgid':1,'bet':1,'bal': 1}):
            if i['tgid'] == message.chat.id:
                if i['bal'] >= 0.1 and i['bal']>=i['bet']:
                    nxt = True
                break
        if message.text==emoji['back']+' Назад':
            mu(message)
        elif message.text==emoji['monbag']+' Ставка':
            inline_kb = types.InlineKeyboardMarkup()
            inline_btn1 = types.InlineKeyboardButton('0.1', callback_data='0.1')
            inline_btn2 = types.InlineKeyboardButton('0.15', callback_data='0.15')
            inline_btn3 = types.InlineKeyboardButton('0.2', callback_data='0.2')
            inline_btn15 = types.InlineKeyboardButton('0.25', callback_data='0.25')
            inline_btn4 = types.InlineKeyboardButton('0.3', callback_data='0.3')
            inline_btn5 = types.InlineKeyboardButton('0.4', callback_data='0.4')
            inline_btn6 = types.InlineKeyboardButton('0.5', callback_data='0.5')
            inline_btn7 = types.InlineKeyboardButton('0.6', callback_data='0.6')
            inline_btn8 = types.InlineKeyboardButton('0.8', callback_data='0.8')
            inline_btn9 = types.InlineKeyboardButton('1', callback_data='1')
            inline_btn10 = types.InlineKeyboardButton('1.5', callback_data='1.5')
            inline_btn11 = types.InlineKeyboardButton('2', callback_data='2')
            inline_kb.add(inline_btn1, inline_btn2,inline_btn3)
            inline_kb.add(inline_btn15, inline_btn4, inline_btn5)
            inline_kb.add(inline_btn6, inline_btn7, inline_btn8)
            inline_kb.add(inline_btn9, inline_btn10, inline_btn11)
            u=bot.send_message(message.chat.id,'Оберіть суму, на яку хочете зіграти:',reply_markup=inline_kb)
            bot.register_next_step_handler(u, coin_obr)
        else:
            if nxt:
                if message.text==emoji['bas'] + ' Баскетбол':
                    try:
                        for n in usrs.find({}, {'tgid': 1, 'bet':1,'bal':1}):
                            if n['tgid'] == message.chat.id:
                                bet=n['bet']
                                balance=n['bal']
                        bask=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        bask.add(emoji['bas'])
                        bask.add(emoji['back']+' Назад')
                        k=bot.send_message(message.chat.id, f'{emoji["fire"]}Сума ставки [{bet} USDT]\n{emoji["monbag"]} Баланс - {balance} USDT\n{emoji["joy"]} Коефіцієнт 1.8x\n\nЩоб почати грати натисніть "{emoji["bas"]}"', reply_markup=bask)
                        bot.register_next_step_handler(k,bask_play)
                    except Exception as e:
                        zr = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        zr.add(emoji['green'] + ' Зрозуміло!')
                        print(e)
                        z=bot.send_message(message.chat.id, f'{emoji["vosk"]}Для початку гри потрібно обрати суму ставки в меню\n"{emoji["cas"]}Казино"', reply_markup=zr)
                        bot.register_next_step_handler(z,coin_obr)
                elif message.text==emoji['cas']+' Слоти':
                    try:
                        for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                            if n['tgid'] == message.chat.id:
                                bet = n['bet']
                                balance = n['bal']
                        slots = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        slots.add(emoji['cas'])
                        slots.add(emoji['back'] + ' Назад')
                        k = bot.send_message(message.chat.id,
                                             f'{emoji["fire"]}Сума ставки [{bet} USDT]\n{emoji["monbag"]} Баланс - {balance} USDT\n{emoji["joy"]} Коефіцієнт 6x\n\nЩоб почати грати натисніть "{emoji["cas"]}"',
                                             reply_markup=slots)
                        bot.register_next_step_handler(k, slots_play)
                    except Exception as e:
                        zr = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        zr.add(emoji['green'] + ' Зрозуміло!')
                        print(e)
                        z=bot.send_message(message.chat.id, f'{emoji["vosk"]}Для початку гри потрібно обрати суму ставки в меню\n"{emoji["cas"]}Казино"', reply_markup=zr)
                        bot.register_next_step_handler(z,coin_obr)
                elif message.text==emoji['dice']+' Кубики':
                    try:
                        for n in usrs.find({}, {'tgid': 1, 'bet': 1, 'bal': 1}):
                            if n['tgid'] == message.chat.id:
                                bet = n['bet']
                                balance = n['bal']
                        dice = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        dice.add('1-3','4-6')
                        dice.add(emoji['back'] + ' Назад')
                        k = bot.send_message(message.chat.id,
                                             f'{emoji["fire"]}Сума ставки [{bet} USDT]\n{emoji["monbag"]} Баланс - {balance} USDT (~{round(balance*40,3)})\n{emoji["joy"]} Коефіцієнт 1.8x\n\nЩоб почати грати оберіть яке значення випаде на кубиках',
                                             reply_markup=dice)
                        bot.register_next_step_handler(k, dice_play)
                    except Exception as e:
                        zr = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        zr.add(emoji['green'] + ' Зрозуміло!')
                        print(e)
                        z = bot.send_message(message.chat.id,
                                             f'{emoji["vosk"]}Для початку гри потрібно обрати суму ставки в меню\n"{emoji["cas"]}Казино"',
                                             reply_markup=zr)
                        bot.register_next_step_handler(z, coin_obr)

                else:
                    bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
                    casino_lobby(message)
            else:
                bot.send_message(message.chat.id, f'{emoji["vosk"]} На балансі недостатньо коштів, для продовження гри змініть суму ставки, або запросіть друзів {emoji["peop"]}\n\n{emoji["tri"]} Мінімальна сума ставки 0.1 USDT')
                mu(message)
    def casino_lobby(message):
        mc = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mc.add(emoji['monbag'] + ' Ставка')
        mc.add(emoji['bas'] + ' Баскетбол', emoji['dice']+' Кубики')
        mc.add(emoji['cas'] + ' Слоти')
        mc.add(emoji['back'] + ' Назад')
        k = bot.send_message(message.chat.id, 'Оберіть режим гри:',
                             reply_markup=mc)
        bot.register_next_step_handler(k,casino)
    def menu(message):
        def mu(message):
            b = [emoji["monbag"] + ' Мій кабінет', emoji['party'] + ' Конкурс', emoji["fl"] + ' Вивід',
                         emoji['peop'] + ' Підтримка', emoji['joy'] + ' Ігри', emoji['monbag'] + ' Виплати', emoji['vosk'] + ' Як заробити']
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(b[0])
            markup.add(b[1], b[2])
            markup.add(b[3], b[4])
            markup.add(b[5],b[6])
            send = bot.send_message(message.chat.id, "Оберіть пункт меню:", reply_markup=markup)
        FOUND = True
        for p in usrs.find({}, {'tgid': 1}):
            if p['tgid'] == message.chat.id:
                FOUND = False
                break
        mb = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mb.add(emoji['back'] + ' Назад')
        def ch(message):
            tr = True
            trsp = True
            for i in sponsors.find({}, {'_id': 1, 'id': 1, 'nick': 1, 'sub': 1}):
                try:
                    if i['id'] != 5527613532:
                        st = bot.get_chat_member(i['id'], message.chat.id).status
                        if st == 'member' or st == 'creator' or st == 'administrator':
                            tr = True
                        else:
                            tr = False
                            return False
                            break
                except Exception as e:
                    bot.send_message(871076127, e)
                    if message.chat.id==5288413290 or message.chat.id==871076127:
                        bot.send_message(5288413290, e)
                        return True
                    else:
                        return False
                    break
            if tr:
                return True
        FOUND = False
        for p in usrs.find({}, {'tgid': 1}):
            if p['tgid'] == user_id:
                FOUND = True
                break
        isban = True
        for g in bans.find({}, {'tgid': 1}):
            if g['tgid'] == message.chat.id:
                isban = False
                break
        if ch(message):
            try:
                for l in usrs.find({}, {'tgid': 1, 'bal': 1, 'pr': 1, 'get': 1}):
                    if l['tgid'] == message.chat.id:
                        if l['get'] == 0:
                            for n in settings.find({}, {'ref': 1}):
                                ref_rew = float(n['ref'])
                                break
                            usrs.update_one({'tgid': message.chat.id},
                                            {"$set": {'get': 1}})
                            xu = usrs.find_one({'tgid': l['pr']})
                            usrs.update_one({'tgid': int(l['pr'])},
                                            {"$set": {'bal': round(xu['bal'] + ref_rew/2, 3)}})
                            # break
                        break
            except Exception as e:
                print(e)
            if FOUND:
                if isban:
                    if message.text == emoji["fl"] + ' Вивід':
                        for i in settings.find({}, {'out': 1, 'ref': 1}):
                            min_out = float(i['out'])
                        for us in usrs.find({}, {'tgid': 1, "bal": 1, 'ref': 1}):
                            if us['tgid'] == message.chat.id:
                                if us['bal'] < min_out:
                                    bot.send_message(message.chat.id, emoji[
                                        'redno'] + f' Недостатньо коштів для виведення\n\nМінімальна сума для виведення - {min_out} USDT')
                                else:
                                    card(message)
                    elif message.text == emoji['peop'] + ' Підтримка':
                        bot.send_message(message.chat.id,
                                             'З будь-яких питань звертайтесь до @Helper_bot_ua ' + emoji['smile'])
                    elif message.text == emoji['joy'] + ' Ігри':
                        casino_lobby(message)
                    elif message.text==emoji['party'] + ' Конкурс':
                        try:
                            li = []
                            for i in list(usrs.find({}, {"kon": 1})):
                                try:
                                    li.append(i['kon'])
                                except Exception:
                                    pass
                            st = ''
                            nd = ''
                            rd = ''
                            th = ''
                            fv = ''
                            allw = 0
                            for i in list(usrs.find({}, {'tgid': 1, 'kon': 1})):
                                try:
                                    if i['kon'] == sorted(li)[-1]:
                                        st = i['tgid']
                                    elif i['kon'] == sorted(li)[-2]:
                                        nd = i['tgid']
                                    elif i['kon'] == sorted(li)[-3]:
                                        rd = i['tgid']
                                    elif i['kon'] == sorted(li)[-4]:
                                        th = i['tgid']
                                    elif i['kon'] == sorted(li)[-4]:
                                        fv = i['tgid']
                                    if len(str(st)) > 3 and len(str(nd)) > 5 and len(str(rd)) > 5:
                                        break
                                except Exception:
                                    pass
                            try:
                                r1=sorted(li)[-1]
                            except Exception:
                                r1=0
                            try:
                                r2=sorted(li)[-2]
                            except Exception:
                                r2=0
                            try:
                                r3=sorted(li)[-3]
                            except Exception:
                                r3=0
                            try:
                                r4=sorted(li)[-4]
                            except Exception:
                                r4=0
                            try:
                                r5=sorted(li)[-5]
                            except Exception:
                                r5=0
                            bot.send_message(message.chat.id,f'{emoji["ana"]} Конкурс найкращих рефералів\n\n{emoji["stat"]} Топ рефералів\n\n{emoji["1"]} <a href="tg://user?id={st}">USER #1</a> - {r1} реф.\n{emoji["2"]} <a href="tg://user?id={nd}">USER #2</a> - {r2} реф.\n{emoji["3"]} <a href="tg://user?id={rd}">USER #3</a> - {r3} реф.\n{emoji["4"]} <a href="tg://user?id={th}">USER #4</a> - {r4} реф.\n{emoji["5"]} <a href="tg://user?id={fv}">USER #5</a> - {r5} реф.\n\n{emoji["party"]} Призи\n\n{emoji["1"]} - 3 USDT\n{emoji["2"]} - 2 USDT\n{emoji["3"]} - 1 USDT\n\n{emoji["rekst"]} Початок 25.08\n{emoji["rekst"]} Закінчення  31.08',parse_mode='HTML')
                        except Exception:
                            bot.send_message(message.chat.id,'Тимчасово недоступно')
                    elif message.text==emoji['monbag'] + ' Виплати':
                        txt = ''
                        for t in range(10):
                            try:
                                tgid = list(comp.find({}, {'Adress': 1, 'Sum': 1, 'tgid': 1,'Time':1}))[-t - 1]['tgid']
                                suma = list(comp.find({}, {'Adress': 1, 'Sum': 1, 'tgid': 1,'Time':1}))[-t - 1]['Sum']
                                time = list(comp.find({}, {'Adress': 1, 'Sum': 1, 'tgid': 1,'Time':1}))[-t - 1]['Time']
                                txt += f"{t + 1}. {emoji['man']} <a href='tg://user?id={tgid}'>USER #{t+1}</a>|{emoji['monbag']} {suma} USDT|{emoji['clock']} {time}\n"
                            except Exception:
                                break
                        bot.send_message(message.chat.id, txt, parse_mode='HTML')
                    elif message.text == emoji['vosk'] + ' Як заробити':
                        for i in settings.find({}, {'out': 1, 'ref': 1}):
                            ref_rew=float(i['ref'])
                            break
                        bot.send_message(message.chat.id,
                                             f'{emoji["vop"]} Як заробити\n\n{emoji["vosk"]}За одного друга ви отримаєте {ref_rew} USDT (~3₴)\n\n{emoji["vosk"]} Букси, завдання, боти дорівнює бан та відмова у виплаті\n\n{emoji["vosk"]} Продати USDT можна на біржах, або обміняти на будь яку криптовалюту\n\n{emoji["vosk"]} Оплату {ref_rew} USDT ви отримаєте тільки після підписки запрошених на всі канали\n\n{emoji["vosk"]} За відписку запрошеного від спонсорів --- штраф 0.035 USDT\n\n{emoji["vosk"]} Виплата приходить протягом 24 годин',
                                             parse_mode='HTML')
                    elif message.text == emoji["monbag"] + ' Мій кабінет':
                        c = 1
                        for i in settings.find({}, {'out': 1, 'ref': 1}):
                            ref_rew=float(i['ref'])
                            break
                        for us in usrs.find({}, {'tgid': 1, "bal": 1, 'ref': 1}):
                            if us['tgid'] == message.chat.id:
                                balance = us['bal']
                                refs = us['ref']
                                break
                        j = bot.send_message(message.chat.id,
                                             f'{emoji["man"]} Користувач - {message.from_user.first_name}\n{emoji["monbag"]} Баланс - {balance} USDT (~{round(balance*30,3)}₴)\n{emoji["coup"]} Запросив - {refs}\n\n{emoji["link"]} Твоє реферальне посилання - https://t.me/UsdtUABot?start={message.chat.id}\n\n{emoji["man"]} За одного запрошеного друга, який перейде по вашому посиланню, та підпишеться на спонсорів ви отримаєте +{ref_rew} (~3₴) USDT',
                                             parse_mode='HTML')
                    elif message.text == '/admin' or message.text == 'admin':
                        k = True
                        for i in admins.find({}, {'tgid': 1}):
                            if int(i['tgid']) == message.chat.id:
                                t = bot.send_message(message.chat.id, 'Welcome back!')
                                admin_panel(message)
                                k = False
                                break
                        if k:
                            bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
                            mu(message)
                    elif message.text == 'Підписався ' + emoji['yep']:
                        mu(message)
                    else:
                        bot.send_message(message.chat.id, 'Не розумію Вас ' + emoji['bor'])
                        mu(message)
                else:
                    bot.send_message(message.chat.id, emoji['redc'] + ' Ви були заблоковані в боті')
            else:
                mu(message)
        else:
            try:
                for l in usrs.find({}, {'tgid': 1, 'bal': 1, 'pr': 1, 'get': 1}):
                    if l['tgid'] == message.chat.id:
                        if l['get'] == 1:
                            for n in settings.find({}, {'ref': 1}):
                                ref_rew = float(n['ref'])
                                break
                            usrs.update_one({'tgid': message.chat.id},
                                            {"$set": {'get': 0}})
                            xu = usrs.find_one({'tgid': l['pr']})
                            usrs.update_one({'tgid': l['pr']}, {"$set": {'bal': round(xu['bal'] - 0.035, 3)}})
                            bot.send_message(l['pr'],f'{emoji["inf"]} @{message.from_user.username} відписався від спонсора, у вас знято 0.035 USDT')
                        break
            except Exception as e:
                print(e)
            inline_k = types.InlineKeyboardMarkup()
            c=1
            for i in sponsors.find({}, {'nick': 1}):
                if i['nick'][len(i['nick']) - 3:len(i['nick'])] == 'bot' or i['nick'][
                                                                            len(i['nick']) - 3:len(
                                                                                i['nick'])] == 'Bot':
                    inline_bt = types.InlineKeyboardButton(f'Бот #{c} (натисніть /start)', callback_data='vip',
                                                           url=f'https://t.me/{i["nick"]}')
                    inline_k.add(inline_bt)
                    c += 1
                else:
                    inline_bt = types.InlineKeyboardButton(f'Канал #{c}', callback_data='vip',
                                                           url=f'https://t.me/{i["nick"]}')
                    inline_k.add(inline_bt)
                    c += 1
            mu_check = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mu_check.add('Підписався ' + emoji['yep'])
            o = bot.send_message(message.chat.id,
                                 f'Щоб продовжити роботу, потрібно підписатися на наступні канали\n', reply_markup=mu_check)
            bot.send_message(message.chat.id, f'Канали:', reply_markup=inline_k)
            bot.register_next_step_handler(o, menu)
    menu(message)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    mu_b = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mu_b.add(emoji['cas'] + ' До гри')
    inline_btn1 = types.InlineKeyboardButton('0.1', callback_data='0.1')
    inline_btn2 = types.InlineKeyboardButton('0.15', callback_data='0.15')
    inline_btn3 = types.InlineKeyboardButton('0.2', callback_data='0.2')
    inline_btn15 = types.InlineKeyboardButton('0.25', callback_data='0.25')
    inline_btn4 = types.InlineKeyboardButton('0.3', callback_data='0.3')
    inline_btn5 = types.InlineKeyboardButton('0.4', callback_data='0.4')
    inline_btn6 = types.InlineKeyboardButton('0.5', callback_data='0.5')
    inline_btn7 = types.InlineKeyboardButton('0.6', callback_data='0.6')
    inline_btn8 = types.InlineKeyboardButton('0.8', callback_data='0.8')
    inline_btn9 = types.InlineKeyboardButton('1', callback_data='1')
    inline_btn10 = types.InlineKeyboardButton('1.5', callback_data='1.5')
    inline_btn11 = types.InlineKeyboardButton('2', callback_data='2')
    if call.data == '0.1':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.1}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.1 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.15':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.15}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.15 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.2':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.2}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.2 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.25':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.25}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.25 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.3':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.3}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.3 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.4':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.4}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.4 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.5':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.5}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.5 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.6':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.6}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.6 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='0.8':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 0.8}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 0.8 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data == '1':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 1}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 1 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='1.5':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 1.5}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 1.5 USDT '+emoji['yep'], reply_markup=mu_b)
                break
    elif call.data=='2':
        for i in usrs.find({}, {'tgid': 1}):
            if i['tgid']==call.message.chat.id:
                usrs.update_one({'tgid': i['tgid']}, {"$set": {'bet': 2}})
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass
                bot.send_message(call.message.chat.id, 'Ставка змінена на 2 USDT '+emoji['yep'], reply_markup=mu_b)
                break

# ==Launching the bot==
if __name__ == '__main__':
    try:
        print('Telegram Bot is starting')
        bot.polling(none_stop=True)
    # except exceptions.ConnectionError as e:
    except Exception as e:
        bot.send_message(871076127, str(e))
        print(e)
        print('Network Issues with Telegram')
