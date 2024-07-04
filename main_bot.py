import telebot

# Ваш токен бота
TOKEN = '6794810148:AAFQileW8K-qLqPeprh4bn7H1uKImvWq74Y'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Заполняем список людей (можно загрузить из файла или базы данных)
people_list = ['Иван', 'Мария', 'Петр']

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for person in people_list:
        markup.add(telebot.types.KeyboardButton(person))
    bot.send_message(message.chat.id, "Выберите человека:", reply_markup=markup)

# Обработчик выбора пользователя
@bot.message_handler(func=lambda message: message.text in people_list)
def send_notification(message):
    chosen_person = message.text
    bot.send_message(message.chat.id, f"Отправлено уведомление '{chosen_person}': Срочно!")

# Запускаем бота
bot.polling()
