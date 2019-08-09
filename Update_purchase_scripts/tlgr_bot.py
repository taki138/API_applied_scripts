import telebot
import config

outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
outputFilename = "CSV selected values Visa DK 2 31.07.2019.csv"

def send_file(outputFilePath, outputFilename):
    bot = telebot.TeleBot(config.telegramBotToken)
    doc = open(outputFilePath + outputFilename, 'rb')
    send = bot.send_document(config.chat_id, doc, disable_notification=True)
    return send

objectMessage = send_file(outputFilePath, outputFilename)
print(objectMessage.date)
