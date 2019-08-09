import telebot
import config
import os
import csv
import json

csvFirstLineWriter = [
	'costumerEmail', 'customerPhone', 'merchantId', 'purchaseId', 'cardBin',
	'resultApiCall1', 'messageApiCall1'
	]


# list functions to manipulate with CSV files
def csv_first_line_writer(outputFilePath, outputFilename, csvFirstLineWriter):
	with open(outputFilePath + outputFilename, "a", newline="") as file:
		stringWriter = csvFirstLineWriter
		writer = csv.writer(file)
		writer.writerow(stringWriter)
		print(f'First line to csv added: {csvFirstLineWriter}')
	file.close()


def csv_result_writer(outputFilename, outputFilePath, writedWalues):
	with open(outputFilePath + outputFilename, "a", newline="") as file:
		stringWriter = writedWalues
		writer = csv.writer(file)
		writer.writerow(stringWriter)
	print(writedWalues)
	file.close()


def reader_csv_to_dictionary(inputFilePath, inputFilename):
	with open(inputFilePath + inputFilename, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(f'reader_csv_to_dictionary: Column names are {", ".join(row)}')
				line_count += 1
			line_count += 1
		print(f'reader_csv_to_dictionary: processed {line_count} lines.')
		return csv_reader
	file.close()


# def writer_dictonary_to_csv(outputFilePath, outputFilename, csv_reader):
# 	pass



# list functions to work with Telegram Bot
def send_file_by_bot(outputFilePath, outputFilename):
	bot = telebot.TeleBot(config.telegramBotToken)
	doc = open(outputFilePath + outputFilename, 'rb')
	send = bot.send_document(config.chat_id, doc, disable_notification=True)
	print(f'Filename: {outputFilename} sended to Telegram')
	return send


def check_directory_existence(filePath):
	try:
		os.makedirs(filePath)
	except Exception as err:
		print(f'Other error occurred: {err}')
		return f'Other error occurred: {err}'


# outputFilename = "billNow test1" + ".csv"
# outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\BillNow Results\\"
# inputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\BillNow Results\\"
# inputFilename = 'billNow 06.08.2019.csv'
# csv_first_line_writer(outputFilePath, outputFilename, csvFirstLineWriter)
# tmp = reader_csv_to_dictionary(inputFilePath, inputFilename)

