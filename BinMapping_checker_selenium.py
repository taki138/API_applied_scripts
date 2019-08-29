import os
import socket
from timeit import default_timer as timer
from time import sleep
from timeit import default_timer as timer
from typing import List, Any

import vertica_python
import datetime

from vertica_python import errors

import config
from config import konnektiveAdminPannelURL
import logging
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.firefox.options import Options
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import core_functions
scriptName = os.path.basename(__file__)
print(f'{scriptName} started')
start = timer()
PARAMS = {
	'loginId': config.loginId,
	'password': config.password,
	'sortDir': '0',
	}

outputFilename = f'verification_charge_results_{datetime.date.today().strftime("%d.%m.%Y")}.csv'
outputFilePath = f'{config.outputCoreFilePath}verification_charge_results\\'
core_functions.check_directory_existence(outputFilePath)


# TODO: в корфункшинс вынгести функцию проверки наличия БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию проверки БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию Рефанда транзакции
# TODO: провести проверку, если БИН, на котором прошла последняя транза не из списка, вызвать ф-ю Рефанда транзакции


def list_costumers_from_DB():
	this_function_name = sys._getframe().f_code.co_name
	conn_info = {
		'host': config.vertica_DB_host,
		'port': config.vertica_DB_port,
		'user': config.vertica_DB_login,
		'password': config.vertica_DB_password,
		'database': config.vertica_DB_dbname,
		# autogenerated session label by default,
		# 'session_label': 'some_label',
		# default throw error on invalid UTF-8 results
		'unicode_error': 'strict',
		# SSL is disabled by default
		'ssl': False,
		# using server-side prepared statements is disabled by default
		'use_prepared_statements': False,
		# connection timeout is not enabled by default
		'connection_timeout': 10
		}

	resultSQLList = []
	nextBillDate = core_functions.tomorrow_date()

	try:
		with vertica_python.connect(**conn_info) as connection:
			cur = connection.cursor()
			SQLRequest = """SELECT distinct(bi.konn_customerId), bi.konn_cardBin, bi.konn_cardType
			FROM konn.bill_info AS bi
			WHERE bi.konn_nextBillDate= :propA
			AND (bi.konn_status='ACTIVE' OR bi.konn_status='TRIAL' OR bi.konn_status='RECYCLE_BILLING')
			AND bi.konn_merchant LIKE '%Check%' AND bi.konn_customerId NOT IN ('1618333', '1680061', '1638349', '1604194', '1833585', '1833481') LIMIT 10;"""
			cur.execute(SQLRequest, {'propA': nextBillDate})
			for row in cur.iterate():
				resultSQLList.append(row)
			cur.close()
			connection.close()
	except socket.error as socketerror:
		print("{this_function_name}: Error: ", socketerror)
	except socket.timeout:
		print(f"{this_function_name}: NO RESPONSE")
	except errors.ConnectionError as err:
		print(f'{this_function_name}: Error occurred: {err}')
	finally:
		connection.close()

	# resultFilteredList лист с бинами кл которые будут чарджиться завтра
	resultFilteredList = []
	for x in resultSQLList:
		try:
			PARAMS = {
				'loginId': config.loginId,
				'password': config.password,
				'customerId': x[0],
				}
			requestResponce = core_functions.konnektivePurchaseQuery(PARAMS)[0]
			result = requestResponce['result']
			status = requestResponce['message']['data'][0]['status']
			cancelReason = requestResponce['message']['data'][0]['cancelReason']
			if result == 'SUCCESS':

				if status == 'ACTIVE' or status == 'TRIAL' or status == 'RECYCLE_BILLING':
					row = x[0], x[1], status, cancelReason, x[2]
					resultFilteredList.append(row)
			elif result == 'ERROR':
				print(requestResponce['message'])
			else:
				print(requestResponce)
		except Exception as excpt:
			print(f'Function error occurred: {excpt}')

	print(f'Function {this_function_name} fulfilled')
	return resultFilteredList

# resultFilteredList - получаем список кл., которые будут чарджиться завтра
resultFilteredList = list_costumers_from_DB()
print(resultFilteredList)
# fp инициализация браузера в Селениум c заданием параметров для firefox_profile
fp = core_functions.browser_init()

# browser открытиен браузера в headless = True
browser = core_functions.browser_open(fp)

core_functions.login_Konnektive(browser, config.seleniumUserName, config.seleniumPassword)

brows_URL = f'{konnektiveAdminPannelURL}merchants/binmapping/'
browser.get(brows_URL)
core_functions.wait_until_element_visible(browser, By.CSS_SELECTOR, '#-row-1 > td:nth-child(1)')
RowsCount = len(browser.find_elements_by_tag_name('tr'))

# binList лист с БИНами в БИНмаппинге
binList: List[str] = []
for counter in range(RowsCount - 1):
	CyclePathStartRange = f'#-row-{str(counter + 1)} > td:nth-child(3)'
	StartRangeValue = browser.find_element_by_css_selector(CyclePathStartRange).text
	binList.append(StartRangeValue)

PARAMS['paySource'] = 'ACCTONFILE'
PARAMS['campaignId'] = '61'
PARAMS['product1_qty'] = '1'
for i in range(len(resultFilteredList)):
	if resultFilteredList[i][1] in binList:
		writedWalues = 'customerId', str(resultFilteredList[i][0]), 'Have Binmapping'
		core_functions.csv_result_writer(outputFilename, outputFilePath, writedWalues)
	else:
		customerId = resultFilteredList[i][0]
		PARAMS['customerId'] = customerId

		if resultFilteredList[i][4] == 'MASTERCARD':
			PARAMS['product1_id'] = '1209'
		else:
			PARAMS['product1_id'] = '1210'

		result = core_functions.konnektiveImportOrder(PARAMS)
		if result[1]['result'] == 'SUCCESS':
			writedWalues = 'customerId', str(customerId), 'SUCCESS'
			core_functions.csv_result_writer(outputFilename, outputFilePath, writedWalues)
		elif result[1]['result'] == 'ERROR':
			writedWalues = 'customerId', str(customerId), 'ERROR', result[1]['message']
			core_functions.csv_result_writer(outputFilename, outputFilePath, writedWalues)
		else:
			writedWalues = 'customerId', str(customerId), result
			core_functions.csv_result_writer(outputFilename, outputFilePath, writedWalues)


# core_functions.send_file_by_bot(outputFilePath, outputFilename)

#############################################################
# for i in range(len(resultFilteredList)):
# 	customerId = resultFilteredList[i][0]
# 	PARAMS['customerId'] = customerId
# 	merchant = core_functions.konnektiveTransactionsQuery(PARAMS)[1]['message']['data'][0]['merchant']
# 	if "Checkout" not in merchant:
# 		pass
	# TODO: функцию авторефанда при выполнении условия


end = timer()
print(f'{scriptName} execution time: {end - start}')
