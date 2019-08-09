import telebot
import config


def send_file(outputFilePath, outputFilename):
    bot = telebot.TeleBot(config.telegramBotToken)
    doc = open(outputFilePath + outputFilename, 'rb')
    send = bot.send_document(config.chat_id, doc, disable_notification=True)
    return send



