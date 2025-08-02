import telebot
token='8492891888:AAG71VfL8tnLBmu_1lsOji_JZmqkzwq8xOo'
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Здравствуйте,  вы написали в поддержку компании ООО _Тмыв бабла_ для того чтобы получить помощь, напишите /help")
@bot.message_handler(commands=['help'])
def sms(message):
    bot.send_message(message.chat.id,
                     '❗ПРЕДУПРЕЖДЕНИЕ:❗\nПри спаме вы навсегда потеряете доступ к боту на данном аккаунте!')
    bot.send_message(message.chat.id, 'Напишите, что произошло при взаимодействии с сайтом, с вами свяжется свободный администратор в личных сообщениях.')
    bot.register_next_step_handler(message, sms_global)

def sms_global(message):
     user_guess = message.text
     print('Кто-то отправил вам смс')
     bot.send_message('-4681080381', user_guess)
     print(user_guess)
bot.infinity_polling()