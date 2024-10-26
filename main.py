import telebot
import time
from guide import commands_help
from telebot import types

bot = telebot.TeleBot("CENSORED")
users_last_request_time = {}



# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ПОРАЖЕНИЕ БОТА И НАЧАЛЬНЫЕ КОМАНДЫ ===================
@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn_info = types.InlineKeyboardButton('D&D Инструкция', url='https://telegra.ph/DD-Instruction-10-01')
    btn_get_id = types.InlineKeyboardButton('Получить свой ID', callback_data='info_button')
    btn_commands = types.InlineKeyboardButton('Зачем нужна Анкета?', callback_data='commands')
    markup.add(btn_info)
    markup.add(btn_commands, btn_get_id)
    bot.send_message(message.chat.id, f"<b>Добро пожаловать в D&D, {message.from_user.first_name}!</b>", parse_mode='html', reply_markup=markup)

# ================================================================================================



# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА НАСТРОЙКИ ИГРЫ ===================
@bot.message_handler(commands=['game_setting'])
def starting_game(message):
    markup = types.InlineKeyboardMarkup()
    btn_join = types.InlineKeyboardButton('Добавить бота в чат', url='https://t.me/jaspblck_reminder_bot?startgroup=true')
    btn_done = types.InlineKeyboardButton('Следующий шаг', callback_data='done')
    markup.add(btn_join, btn_done)
    bot.send_message(message.chat.id, "<b>Для начала создайте или просто добавьте бота в вашу существующую группу:</b>", parse_mode='html', reply_markup=markup)

# ================================================================================================



# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ПОКАЗ КОМАНД БОТА ===================
@bot.callback_query_handler(func=lambda call: call.data == 'commands')
def helper_commands(call):
    bot.send_message(call.message.chat.id, f"<b>{commands_help}</b>", parse_mode='html')

# ================================================================================================



# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ОТВЕТ НА ЗАПРОС ИДЕНТИФИКАТОРА ===================
@bot.callback_query_handler(func=lambda call: call.data == 'info_button')
def id_query(call):
    user_info = (
        f"ID: {call.from_user.id}\n"
        f"Name: {call.from_user.first_name}\n"
        f"Username: {call.from_user.username or 'не указан'}"
    )
    bot.send_message(call.message.chat.id, user_info)

# ================================================================================================



# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ВЫБОР КАРТЫ ========================================
@bot.callback_query_handler(func=lambda call: call.data == 'maps')
def choose_maps(call):
    map1_path = 'C:/Users/jasper/Desktop/telegram-bot/maps/map1.png'
    with open(map1_path, 'rb') as mp1:
        bot.send_photo(call.message.chat.id, mp1)

    markup = types.InlineKeyboardMarkup()
    btn_plus = types.InlineKeyboardButton('➕', callback_data='choise1')
    btn_minus = types.InlineKeyboardButton('➖', callback_data='choise2')
    markup.add(btn_plus, btn_minus)
    bot.reply_to(call.message, "Если понравилась карта + / Если нет -")
    bot.send_message(call.message.chat.id, "Выбирай", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'choise1')
def handle_plus(call):
    bot.send_message(call.message.chat.id, "Рад, что тебе понравилась карта! Отправляй теперь эту карту в группу 😊")

@bot.callback_query_handler(func=lambda call: call.data == 'choise2')
def handle_minus(call):
    bot.send_message(call.message.chat.id, "Жаль, что карта не понравилась. 😞")

# ================================================================================================


# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ПОЛУЧЕНИЕ АНКЕТЫ ===================
@bot.callback_query_handler(func=lambda call: call.data == 'done')
def send_file_to_user(call):
    current_time = time.time()
    cooldown_period = 5 * 60  
    if call.message.chat.id in users_last_request_time:
        last_request_time = users_last_request_time[call.message.chat.id]
        if current_time < last_request_time + cooldown_period:
            time_left = int((last_request_time + cooldown_period - current_time) / 60)
            bot.send_message(call.message.chat.id, f"Пожалуйста, подождите еще {time_left} минут(ы) перед повторным запросом анкеты. ⏳")
            return

    file_path = 'C:/Users/jasper/Desktop/telegram-bot/file.txt'
    with open(file_path, 'rb') as file:
        bot.send_document(call.message.chat.id, file)
    bot.send_message(call.message.chat.id, "<b>Пожалуйста, заполните анкету в этом текстовом файле и отправьте обратно!</b>", parse_mode='html')

    users_last_request_time[call.message.chat.id] = current_time

# ================================================================================================



# =================== ЭТОТ БЛОК ОТВЕЧАЕТ ЗА ОТПРАВКУ ВАШЕЙ АНКЕТЫ В ГРУППУ ===================
try:
    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        if message.document.mime_type == 'text/plain':
            chat_id = '@jasrblck_dnd'
            markup = types.InlineKeyboardMarkup()
            btn_map = types.InlineKeyboardButton('Выбрать Карту', callback_data='maps')
            markup.add(btn_map)
            bot.send_message(message.chat.id, "Файл принят! 📄 Осталось выбрать карту:", reply_markup=markup)
            bot.forward_message(chat_id, message.chat.id, message.message_id)
        else:
            bot.reply_to(message, "Пожалуйста, отправьте файл в формате .txt. ❌")
except Exception as e:
    print(f"Ошибка: {e}")

# ================================================================================================

bot.polling(none_stop=True)
