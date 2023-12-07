import telebot
from telebot import types

TOKEN = '6888803888:AAH_a7FrxsjICL1DcGX2nh_s4jUXSZaQllc'
bot = telebot.TeleBot(TOKEN)

questions = [
    {"text": "Сколько планет в Солнечной системе?", "options": ["8", "9", "10"], "correct_option": "8"}, # 0
    {"text": "Какой год основания Рима?", "options": ["753 до н. э.", "1 н. э.", "500 н. э."], "correct_option": "753 до н. э."}, # 1
]

user_answers = {}

def send_question(chat_id, user_id):
    question_data = questions[user_answers[user_id]["current_question"]]
    question_text = question_data["text"]
    options = question_data["options"]

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(option))

    bot.send_message(chat_id, question_text, reply_markup=markup)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_answers[user_id] = {"current_question": 0, "score": 0}
    send_question(message.chat.id, user_id)


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    current_question = user_answers[user_id]["current_question"]
    correct_option = questions[current_question]["correct_option"]

    if message.text == correct_option:
        user_answers[user_id]["score"] += 1

    user_answers[user_id]["current_question"] += 1

    if user_answers[user_id]["current_question"] < len(questions):
        send_question(message.chat.id, user_id)
    else:
        score = user_answers[user_id]["score"]
        bot.send_message(message.chat.id, f"Игра окончена! Ваш счет: {score}/{len(questions)}")
        del user_answers[user_id]

bot.polling()
