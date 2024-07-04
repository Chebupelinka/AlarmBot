import telebot
import json

# Ваш токен бота
TOKEN = '6794810148:AAFQileW8K-qLqPeprh4bn7H1uKImvWq74Y'

# Загружаем данные из файла people.json
with open('people.json', 'r', encoding='utf-8') as file:
    people_data = json.load(file)
    people_list = people_data['users']

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for person in people_list:
        markup.add(telebot.types.KeyboardButton(person['name']))
    bot.send_message(message.chat.id, "Выберите человека:", reply_markup=markup)


# Обработчик выбора пользователя
@bot.message_handler(func=lambda message: message.text in [person['name'] for person in people_list])
def send_notification(message):
    chosen_person_name = message.text
    chosen_person = next(person for person in people_list if person['name'] == chosen_person_name)
    if chosen_person['urgent']:
        bot.send_message(message.chat.id, f"Отправлено уведомление '{chosen_person_name}': Срочно!")
        bot.send_message(chosen_person['id'], f"Alarm! From id:{message.from_user.id}")
    else:
        bot.send_message(message.chat.id, f"{chosen_person_name} не в списке срочно.")


# Запускаем бота
bot.polling()
