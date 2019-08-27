import telebot
import config

bot = telebot.TeleBot(config.telegramBotToken)
outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
outputFilename = "CSV selected values Visa DK 2 31.07.2019.csv"

def send_file(outputFilePath, outputFilename):
	bot = telebot.TeleBot(config.telegramBotToken)
	doc = open(outputFilePath + outputFilename, 'rb')
	send = bot.send_document(config.chat_id, doc)
	return send


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
	text = message.text.lower()
	chat_id = message.chat.id
	bot.send_message(chat_id, 'trest')
	if text == "getchatid":
		bot.send_message(chat_id, 'chat_id: {chat_id}')


bot.polling()

objectMessage = send_file(outputFilePath, outputFilename)
print(objectMessage.date)
