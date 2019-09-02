import vertica_python
from dateutil import relativedelta
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from f import pcall_wraps
# import vertica_python
import requests
import telebot
import config
import os
import csv
import json
from requests import HTTPError
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from time import sleep
import config
import logging
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.firefox.options import Options
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# import psycopg2

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

# loginId = config.loginId
# password = config.password
# orderId = ''
# purchaseId = ''
# customerId = '765725'
# txnType = ''
# paySource = ''
# responseType = ''
# merchantTxnId = ''
# clientTxnId = ''
# merchantId = ''
# cardLast4 = ''
# cardBin = ''
# achAccountNumber = ''
# achRoutingNumber = ''
# isChargedback = ''
# firstName = ''
# lastName = ''
# companyName = ''
# address1 = ''
# address2 = ''
# postalCode = ''
# city = ''
# state = ''
# country = ''
# emailAddress = ''
# phoneNumber = ''
# affId = ''
# showExternal = ''
# dateRangeType = ''
# startDate = ''
# endDate = ''
# startTime = ''
# endTime = ''
# sortDir = ''
# resultsPerPage = ''
# page = ''


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


# list functions fo
def konnektiveTransactionsQuery(PARAMS):
	PARAMS = {
		'loginId': PARAMS['loginId'],
		'password': PARAMS['password'],
		'customerId': PARAMS['customerId'],
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


def konnektiveTransactionsRefund(PARAMS):
	PARAMS = {
		'loginId': PARAMS['loginId'],
		'password': PARAMS['password'],
		'customerId': PARAMS['customerId'],
		}
	URL = konnektiveApiEndpoint + 'transactions/refund/'

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


def konnektivePurchaseQuery(PARAMS):
	PARAMS = {
		'loginId': PARAMS['loginId'],
		'password': PARAMS['password'],
		'customerId': PARAMS['customerId'],
		}
	URL = konnektiveApiEndpoint + 'purchase/query/'

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


def konnektiveImportOrder(PARAMS):
	PARAMS = {
		'loginId': PARAMS['loginId'],
		'password': PARAMS['password'],
		'customerId': PARAMS['customerId'],
		'paySource': PARAMS['paySource'],
		'campaignId': PARAMS['campaignId'],
		'product1_qty': PARAMS['product1_qty'],
		'product1_id': PARAMS['product1_id'],
		}
	URL = konnektiveApiEndpoint + 'order/import/'

	try:
		responseUrl = session.post(URL, PARAMS, timeout=(10, 10))
		parseResponseUrlJSON = responseUrl.json()
		parseResponseUrlString = json.dumps(parseResponseUrlJSON, indent=4)
		# parseResponseUrlDict = json.loads(responseUrl.text)
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
		return parseResponseUrlJSON, parseResponseUrlString


# Selenium webbrowser scripts
# TODO: вынести параметры set_preference как аргумент в формате списка
def postgres_DB_connector():
	this_function_name = sys._getframe().f_code.co_name
	try:
		conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
	except Exception as err:
		print(f'Function {this_function_name} error occurred: {err}')


# скрипты для работы с БД

def SQL_SELECT_from_vertica(SQLRequest, conn_info):
	this_function_name = sys._getframe().f_code.co_name
	print(f"{this_function_name} started")
	conn_info = {
		'host': conn_info['host'],
		'port': conn_info['port'],
		'user': conn_info['user'],
		'password': conn_info['password'],
		'database': conn_info['database'],
		# autogenerated session label by default,
		# 'session_label': 'some_label',
		# default throw error on invalid UTF-8 results
		'unicode_error': conn_info['unicode_error'],
		# SSL is disabled by default
		'ssl': conn_info['ssl'],
		# using server-side prepared statements is disabled by default
		'use_prepared_statements': conn_info['use_prepared_statements'],
		# connection timeout is not enabled by default
		'connection_timeout': conn_info['connection_timeout']
		}

	resultSQLList = []

	with vertica_python.connect(**conn_info) as connection:
		cur = connection.cursor()
		resultSQLExecution = cur.execute(SQLRequest)
		for row in cur.iterate():
			resultSQLList.append(row)
		cur.close()
		connection.close()
	connection.close()
	return resultSQLExecution
	print(f"{this_function_name} fullfilled")


def wait_until_element_visible(browser, position_id, position_value):
	element = WebDriverWait(browser, 60).until(
		EC.visibility_of_element_located((position_id, position_value)))


def browser_init():
	this_function_name = sys._getframe().f_code.co_name
	try:
		fp = webdriver.FirefoxProfile()
		fp.set_preference("browser.download.dir", r"C:\\Users\\GuestUser\\Downloads\\ChO ChB")
		fp.set_preference("browser.download.folderList", 2)
		fp.set_preference("browser.download.manager.showWhenStarting", False)
		fp.set_preference("browser.helperApps.alwaysAsk.force", False)
		fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
		fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
		                  "application/msword, application/csv, application/ris, text/csv, text/css, image/png, application/pdf,"
		                  "text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed,"
		                  "application/download, application/octet-stream, application/csvm+json, 	text/csv-schema, application/vnd.ms-excel,"
		                  "application/vnd.ms-excel.addin.macroEnabled.12, application/vnd.ms-excel.sheet.binary.macroEnabled.12,"
		                  "application/vnd.ms-excel.sheet.macroEnabled.12, 	application/vnd.ms-excel.template.macroEnabled.12, text/csv-schema,"
		                  "application/x-download; =")
		fp.set_preference("browser.download.manager.focusWhenStarting", False)
		fp.set_preference("browser.download.useDownloadDir", True)
		fp.set_preference("browser.helperApps.alwaysAsk.force", False)
		fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
		fp.set_preference("browser.download.manager.closeWhenDone", True)
		fp.set_preference("browser.download.manager.showAlertOnComplete", False)
		fp.set_preference("browser.download.manager.useWindow", False)
		fp.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
		fp.set_preference("browser.download.panel.shown", False)
		fp.set_preference("javascript.enabled", False)
	except Exception as err:
		print(f'Function {this_function_name} error occurred: {err}')
	else:
		print(f'Function {this_function_name} fulfilled')
	return fp


def browser_open(fp: object) -> object:
	this_function_name = sys._getframe().f_code.co_name
	try:
		opts = Options()
		opts.set_headless()
		assert opts.headless
		browser = Firefox(fp, options=opts)
		browser.maximize_window()
	except Exception as err:
		print(f'Function {this_function_name} error occurred: {err}')
		return f'Function {this_function_name} error occurred: {err}'
	else:
		print(f'Function {this_function_name} fulfilled')
		return browser


def login_Konnektive(browser: object, login: str, password: str) -> object:
	this_function_name = sys._getframe().f_code.co_name  # позволяет получить имя функции внутри самой функции
	try:
		WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located)
		browser.get(config.konnektiveAdminPannelURL)
		browser.find_element_by_name('userName').send_keys(login)
		browser.find_element_by_name('password').send_keys(password)
		browser.find_element_by_tag_name('button').submit()
		sleep(6)
	except Exception as err:
		print(f'Function {this_function_name} error occurred: {err}')
		return f'Function {this_function_name} error occurred: {err}'
	else:
		print(f'Function {this_function_name} fulfilled')
	return browser


def tomorrow_date() -> str:
	tomorrowNonFormat = datetime.datetime.today() + datetime.timedelta(1)
	tomorrowDate = datetime.datetime.strftime(tomorrowNonFormat, '%Y-%m-%d')
	return tomorrowDate


def next_month():
	nextmonth = datetime.date.today() + relativedelta.relativedelta(months=1)
	nextMonth = datetime.datetime.strftime(nextmonth, '%Y-%m-%d %X' + '.000000')
	return nextMonth

@pcall_wraps
def next_mont_first_date() -> tuple:
	today = date.today()
	d = today + relativedelta(months=1)
	firstDate = date(d.year, d.month, 1)
	return firstDate

