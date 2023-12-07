import telebot

BOT_TOKEN = "6888803888:AAH_a7FrxsjICL1DcGX2nh_s4jUXSZaQllc"

bot = telebot.TeleBot(BOT_TOKEN)

button = telebot.types.InlineKeyboardButton("YouTube ->", url="https://youtu.be/jNQXAC9IVRw?si=ZIQRXC4q9Ns3a4_S")
markup = telebot.types.InlineKeyboardMarkup().add(button)

button_2 = telebot.types.KeyboardButton("/yes")
button_3 = telebot.types.KeyboardButton('/no')
markup_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row(button_2 , button_3)

bot_questions = [
    {"q": "Who created YouTube?", "answers": ["Steve Jobs", "Chad Hurley", "Elon Musk"], "correct_answer": "Chad Hurley"},
    {"q": "When YouTube was created? ", "answers": ["2005", "2008", "2003"], "correct_answer": "2005"}, 
    {"q": "What was the duration of the first video on YouTube? ", "answers": ["18-second", "20-minute", "3-second"], "correct_answer": "18-second"},
    {"q": "Where was the video filmed? ", "answers": ["KFC", "Zoo", "Park"], "correct_answer": "Zoo"},
    {"q": "How many views did it get? ", "answers": ["227m views", "120m views", "50m views"], "correct_answer": "227m views"},
]

user_answers = {}

def send_question(chat_id, user_id):
    question_data = bot_questions[user_answers[user_id]["current_question"]]
    question_text = question_data["q"]
    answers = question_data["answers"]

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)


    for answer in answers:
        markup.add(telebot.types.KeyboardButton(answer))
    bot.send_message(chat_id, question_text, reply_markup=markup)

@bot.message_handler(commands=['start'])
def go(message):
    bot.send_message(message.chat.id , "Are you ready for out YouTube test?" , reply_markup=markup_2)

@bot.message_handler(commands=['no'])
def go(message):
    bot.send_message(message.chat.id , text="Well , see you later:(")

@bot.message_handler(commands=['yes'])
def handle_start(message):
    user_id = message.from_user.id
    user_answers[user_id] = {"current_question": 0, "score": 0}
    send_question(message.chat.id, user_id)


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    current_question = user_answers[user_id]["current_question"]
    correct_answer = bot_questions[current_question]["correct_answer"]

    if message.text == correct_answer:
        user_answers[user_id]["score"] += 1
    user_answers[user_id]["current_question"] += 1

    if user_answers[user_id]["current_question"] < len(bot_questions):
        send_question(message.chat.id, user_id)
    
    
    else:
        score = user_answers[user_id]["score"]
        if score >= 4:   
            bot.send_message(message.chat.id, f"You've passed our test!\nYour excellent points: {score}/{len(bot_questions)}")
            bot.send_message(message.chat.id , "Now you can go , and enjoy watching YouTube!" , reply_markup=markup)
            del user_answers[user_id]  
        else:  
           bot.send_message(message.chat.id, f"Test is over!\nYour points: {score}/{len(bot_questions)}")
           bot.send_message(message.chat.id , "Try again next time , see you later:)")
           del user_answers[user_id]





    


bot.polling()
