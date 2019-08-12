import requests
import telebot
import config
import os
import csv
import json
from requests import HTTPError
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter

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

# функция проверяет существование директорий по указанному пути, если директорий нет, они создаются
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
# reader_csv_to_list(inputFilePath, inputFilename)

#  Functions for API konnective requests
# API Documentation: https://api.konnektive.com/docs/transaction_update/

loginId = config.loginId
password = config.password
orderId = ''
purchaseId = ''
customerId = '765725'
txnType = ''
paySource = ''
responseType = ''
merchantTxnId = ''
clientTxnId = ''
merchantId = ''
cardLast4 = ''
cardBin = ''
achAccountNumber = ''
achRoutingNumber = ''
isChargedback = ''
firstName = ''
lastName = ''
companyName = ''
address1 = ''
address2 = ''
postalCode = ''
city = ''
state = ''
country = ''
emailAddress = ''
phoneNumber = ''
affId = ''
showExternal = ''
dateRangeType = ''
startDate = ''
endDate = ''
startTime = ''
endTime = ''
sortDir = ''
resultsPerPage = ''
page = ''


def responceStatusCodeValidation(responseUrl):
	if responseUrl.status_code == 200:
		pass
	else:
		print('status_code: ' + str(responseUrl.status_code), '; parseResponseUrl: ' + str(responseUrl))
		return responseUrl.status_code


konnektive_adapter = HTTPAdapter(max_retries=10)
session = requests.Session()
konnektiveApiEndpoint = 'https://api.konnektive.com/'
session.mount(konnektiveApiEndpoint, konnektive_adapter)


def konnektiveTransactionsQuery():
	PARAMS = {
		'loginId': loginId,
		'password': password,
		'orderId': orderId,
		'purchaseId': purchaseId,
		'customerId': customerId,
		'txnType': txnType,
		'paySource': paySource,
		'responseType': responseType,
		'merchantTxnId': merchantTxnId,
		'clientTxnId': clientTxnId,
		'merchantId': merchantId,
		'cardLast4': cardLast4,
		'cardBin': cardBin,
		'achAccountNumber': achAccountNumber,
		'achRoutingNumber': achRoutingNumber,
		'isChargedback': isChargedback,
		'firstName': firstName,
		'lastName': lastName,
		'companyName': companyName,
		'address1': address1,
		'address2': address2,
		'postalCode': postalCode,
		'city': city,
		'state': state,
		'country': country,
		'emailAddress': emailAddress,
		'phoneNumber': phoneNumber,
		'affId': affId,
		'showExternal': showExternal,
		'dateRangeType': dateRangeType,
		'startDate': startDate,
		'endDate': endDate,
		'startTime': startTime,
		'endTime': endTime,
		'sortDir': sortDir,
		'resultsPerPage': resultsPerPage,
		'page': page,
		}
	URL = konnektiveApiEndpoint + 'transactions/query/'

	try:
		responseUrl = session.post(URL, PARAMS, timeout=(10, 10))
		parseResponseUrlJSON = responseUrl.json()
		parseResponseUrlString = json.dumps(parseResponseUrlJSON, indent=4)
		parseResponseUrlDict = json.loads(responseUrl.text)
		responseUrl.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')
		return f'HTTP error occurred: {http_err}'
	except Exception as err:
		print(f'Other error occurred: {err}')
		return f'Other error occurred: {err}'
	except Timeout as timeout_err:
		print(f'Timeout error occurred: {timeout_err}')
		return f'Timeout error occurred: {timeout_err}'
	else:
		return parseResponseUrlDict, parseResponseUrlJSON, parseResponseUrlString
