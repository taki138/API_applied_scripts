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


def reader_csv_to_list(inputFilePath, inputFilename):
	with open(inputFilePath + inputFilename, 'r') as f:
		csv_reader = csv.reader(f, delimiter=';')
		output_list = list(csv_reader)
		print(output_list)
		f.close()
		return output_list


def csv_result_writer(outputFilename, outputFilePath, writedWalues):
	with open(outputFilePath + outputFilename, "a", newline="") as file:
		stringWriter = writedWalues
		writer = csv.writer(file)
		writer.writerow(stringWriter)
	print(writedWalues)
	file.close()


# TODO: допилить импорт CSV в словарь
# def reader_csv_to_dictionary(inputFilePath, inputFilename):
# 	with open(inputFilePath + inputFilename, mode='r') as csv_file:
# 		input_file = csv.DictReader(csv_file, delimiter=';')
# 		headers = input_file.fieldnames
# 		result = {}
# 		for row in map(dict, input_file):
# 			# print(row)
# 			print(f"{row['fam_wilen@hotmail.com']}")
#
# 		# 	for column, value in row.iteritems():
# 		# 		result.setdefault(column, []).append(value)
# 		# 		print(f'reader_csv_to_dictionary: Column names are {", ".join(row)}')
# 		# 		line_count += 1
# 		# 	line_count += 1
# 		# print(f'reader_csv_to_dictionary: processed {line_count} lines.')
# 		return csv_file


# def writer_dictonary_to_csv(outputFilePath, outputFilename, csv_reader):
# 	pass


# list functions to work with Telegram Bot
def send_file_by_bot(outputFilePath, outputFilename):
	# TODO: допилить перевод даты из таймстамп в норм формат
	bot = telebot.TeleBot(config.telegramBotToken)
	doc = open(outputFilePath + outputFilename, 'rb')
	send = bot.send_document(config.group_chat_id, doc, disable_notification=True)
	objectMessage = send.date
	print(f'Filename: {outputFilename} sended to Telegram')
	return send


def check_directory_existence(filePath):
	try:
		os.makedirs(filePath)
	except Exception as err:
		print(f'Other error occurred: {err}')
		return f'Other error occurred: {err}'


outputFilename = "billNow test1" + ".csv"
outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\BillNow Results\\"
inputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\BillNow Results\\"
inputFilename = 'billNow 06.08.2019.csv'

reader_csv_to_list(inputFilePath, inputFilename)
