import telebot
import json

# Ваш токен бота
TOKEN = '6794810148:AAFQileW8K-qLqPeprh4bn7H1uKImvWq74Y'

# Загружаем данные из файла people.json
with open('people.json', 'r+', encoding='utf-8') as file:
    people_data = json.load(file)
    people_list = people_data['users']


def check_is_user_was_there(user_id):
    for person in people_list:
        if user_id == person['id']:
            return True
    return False


def update_json(new_data):
    people_data['users'].append(new_data)
    file.seek(0)
    json.dump(people_data, file)

# Создаем объект бота


bot = telebot.TeleBot(TOKEN)

# Вводим глобальные поля на случай, если человек ещё не зарегистрирован
name = ""
group = 0
is_correct = False


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    if not check_is_user_was_there(message.from_user.id):

        new_msg = bot.send_message(message.chat.id, "Приветсвую тебя, давай знакомиться! Меня зовут FKIT_ALARM bot. А тебя? "
                                               "\n\n\nP.S. Напиши своё настоящее ФИО, чтобы тебя было проще найти!")
        bot.register_next_step_handler(new_msg, get_text(new_msg))

        bot.send_message(message.chat.id, f"Приятно познаомиться, {name}!")

        new_msg = bot.send_message(message.chat.id, "А из какой ты группы?")
        bot.register_next_step_handler(new_msg, get_text)

        while True:
            try:
                group = int(new_msg.text)
                break
            except ValueError:
                bot.send_message(message.chat.id, "Упс, похоже кто-то ввёл неправильно группу, попробуй ещё раз)))"
                                                  "\n\n\nЧисло должно быть формата int!")
                new_msg = bot.send_message(message.chat.id, "Напиши ещё раз - из какой ты группы")
                bot.register_next_step_handler(new_msg, get_text)
        new_person = {"id": message.from_user.id,
            "name": name,
            "group": group,
            "urgent": False,
            "admin": False}
        update_json(new_person)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for person in people_list:
        markup.add(telebot.types.KeyboardButton(person['name']))
    bot.send_message(message.chat.id, "Выберите человека:", reply_markup=markup)


def get_text(message):
    if name == "":
        text = message.text
        validate_msg = bot.send_message(message.chat.id, "Проверьте, верно ли вы ввели свои данные?")
        bot.register_next_step_handler(validate_msg, is_data_correct(validate_msg))
        if (is_correct == False):
            other_msg = bot.send_message(message.chat.id, "Напиши своё настоящее ФИО, чтобы тебя было проще найти!")


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


# Проверка корректности ввода

def is_data_correct(message):
        correct_marcup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        correct_marcup.add(telebot.types.KeyboardButton("Да, всё верно!"))
        correct_marcup.add(telebot.types.KeyboardButton("Нет, дайте я исправлю!"))
        bot.send_message(message.chat.id, "Выберите пункт из меню клавиатуры:", reply_markup=correct_marcup)


@bot.message_handler(func=lambda message: message.text == "Да, всё верно!")
def correct(message):
    is_correct = True


@bot.message_handler(func=lambda message: message.text == "Да, всё верно!")
def correct(message):
    is_correct = False

# Запускаем бота
bot.polling()
