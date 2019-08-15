import socket
from timeit import default_timer as timer
from time import sleep
from timeit import default_timer as timer

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

start = timer()


# TODO: в корфункшинс вынгести функцию проверки наличия БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию проверки БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию Импорт Ордер
# TODO: в корфункшинс вынгести функцию Рефанда транзакции
# TODO: провести проверку, если БИН, на котором прошла последняя транза не из списка, вызвать ф-ю Рефанда транзакции
# TODO: отправка итогового репорта в телеграм чат

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
		'connection_timeout': 3
		}

	resultSQLList = []
	nextBillDate = core_functions.tomorrow_date()

	try:
		with vertica_python.connect(**conn_info) as connection:
			cur = connection.cursor()
			SQLRequest = """SELECT bi.konn_customerId, bi.konn_cardBin
			FROM konn.bill_info AS bi
			WHERE bi.konn_nextBillDate= :propA
			AND (bi.konn_status='ACTIVE' OR bi.konn_status='TRIAL' OR bi.konn_status='RECYCLE_BILLING')
			AND bi.konn_merchant LIKE '%Check%' LIMIT 20;"""
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

				if status == 'ACTIVE' or status == 'TRIAL':
					row = x[0], x[1], status, cancelReason
					resultFilteredList.append(row)
			elif result == 'ERROR':
				print(requestResponce['message'])
			else:
				print(requestResponce)
		except Exception as excpt:
			print(f'Function error occurred: {excpt}')

	print(f'Function {this_function_name} fulfilled')
	return resultFilteredList


resultFilteredCostumerList = list_costumers_from_DB()

fp = core_functions.browser_init()
browser = core_functions.browser_open(fp)
core_functions.login_Konnektive(browser, config.seleniumUserName, config.seleniumPassword)

brows_URL = f'{konnektiveAdminPannelURL}merchants/binmapping/'
browser.get(brows_URL)
core_functions.wait_until_element_visible(browser, By.CSS_SELECTOR, '#-row-1 > td:nth-child(1)')

RowsCount = len(browser.find_elements_by_tag_name('tr'))
binList = []

for counter in range(RowsCount - 1):
	CyclePathStartRange = f'#-row-{str(counter + 1)} > td:nth-child(3)'
	StartRangeValue = browser.find_element_by_css_selector(CyclePathStartRange).text
	binList.append(StartRangeValue)
print(binList)

print(len(resultFilteredCostumerList))

for resultFilteredList in range(len(resultFilteredCostumerList) - 1):
	cardBinListCross = StartRangeValue in binList
# if cardBinListCross:
#     CyclePathEditButton = '#-row-' + str(counter + 1) + ' > td:nth-child(8) > span:nth-child(1)'
#     browser.find_element_by_css_selector(CyclePathEditButton).click()
#     core_functions.wait_until_element_visible(
#         By.CSS_SELECTOR, '.checkbox > label:nth-child(1) > input:nth-child(1')
#     browser.find_element_by_css_selector('.checkbox > label:nth-child(1) > input:nth-child(1)').click()
#     browser.find_element_by_css_selector('input.btn').click()
#     sleep(30)


end = timer()
print(f'Script execution time: {end - start}')
