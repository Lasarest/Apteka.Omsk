import telebot
from update import update_db
from search import search_in_file
from telebot import types

# Add your bot token in "token = "
def run_bot():
    token = ""
    bot = telebot.TeleBot(token)
    print("[INFO] Bot started!")
    # Send hello message
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        start_search = types.KeyboardButton('Начать поиск')
        send_full_info = types.KeyboardButton('Информация о боте')
        markup.add(start_search, send_full_info)
        bot.send_message(message.chat.id,
                         f"<b>Привет, {message.from_user.first_name}</b>✌️ \nДанный бот содержит базу данных "
                         f"препаратов аптек в Омске. \nНе знаешь в какой аптеке найти или ищешь минимальную "
                         f"стоимось?\nНажимай кнопку: 'Начать поиск'",
                         parse_mode='html', reply_markup=markup)
        #Adding user data to a file "User.txt"
        #If such a user has already been added, then do nothing
        try:
            count = 0
            file_user = open('User.txt', 'r+')
            for line in file_user:
                line = line.split(" : ")[1]
                if message.from_user.id == int(line):
                    count = count + 1
                    break
            if count == 0:
                file_user.write(
                    str(message.from_user.username) + " | " + str(message.from_user.first_name) + " | " + str(
                        message.from_user.last_name) + " : " + str(message.from_user.id) + '\n')
        except:
            print("[INFO] Error add user!")
# Update database command
    @bot.message_handler(commands=['update'])
    def update(message):
        # Checking for admin
        # Into a variable "admin_id" add your id
        admin_id = 
        if message.from_user.id == admin_id:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            yes_button = types.KeyboardButton('Да ✅')
            no_button = types.KeyboardButton('Нет ❌')
            markup.add(yes_button, no_button)
            # Action confirmation
            text = bot.send_message(message.chat.id, "Начать обновление базы?", reply_markup=markup)
            bot.register_next_step_handler(text, start_update)
        else:
            bot.send_message(message.chat.id, "У вас недостаточно прав! ❌")
            
    def start_update(message):
        if message.text == "Да ✅":
            bot.send_message(message.chat.id, "Обновление началось....")
            update_db()
            bot.send_message(message.chat.id, "База данных успешно обновлена! ✅")
            start(message)
        else:
            bot.send_message(message.chat.id, "Обновление отменено! ❌")
# Get list of pharmacies
    @bot.message_handler(commands=['info'])
    def info(message):
        bot.send_message(message.chat.id, "Список аптек: \nФармакопейка\nАптека от склада\nСемейная аптека")
# Searching drug from database "DB.txt"
    @bot.message_handler(commands=['search'])
    def search(message):
        text = bot.send_message(message.chat.id, "Введите название лекарственного препарата: ")
        bot.register_next_step_handler(text, report)

    def report(message):
        text_form_user = message.text
        sorted_db, count = search_in_file(text_form_user)
        if count != 0:
            bot.send_message(message.chat.id, "Вот что мне удалось найти:")
            for i in range(len(sorted_db)):
                try:
                    find_photo = open("Images/{}".format(sorted_db[i][0]), 'rb')
                    message_text = "\n" + sorted_db[i][1] + "\n" + sorted_db[i][2] + "\n" + sorted_db[i][3]
                    bot.send_photo(message.chat.id, find_photo, caption=message_text)
                except:
                    print("[INFO] Error search!")
            bot.send_message(message.chat.id, "Все найденные препараты по запросу! ✅")
        else:
            bot.send_message(message.chat.id, 'Препарат не найден! ❌')
# Message processing
    @bot.message_handler()
    def error_message(message):
        if message.text == "Начать поиск":
            search(message)
        elif message.text == "Информация о боте":
            info(message)
        else:
            bot.send_message(message.chat.id, "Я вас не понимаю! ❌")

    bot.polling(none_stop=True)


if __name__ == '__main__':
    run_bot()
