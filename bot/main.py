import telebot

# Bot token
BOT_TOKEN = "8294189105:AAHNetFIEPE5E4i3WV5wFd4QZbbhn3VGJGU"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Assalomu alaykum! Men Toshkent Metro Lost & Found botman.")

# Botni ishga tushirish
bot.polling()
