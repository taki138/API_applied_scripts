from time import sleep

import vertica_python

import config
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

# TODO: в корфункшинс вынгести функцию проверки наличия БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию выборку SQL из БД клиентов, котоые будут чарджиться завтра
# TODO: в корфункшинс вынгести функцию проверки БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию Импорт Ордер
# TODO: в корфункшинс вынгести функцию Рефанда транзакции
# TODO: провести проверку, если БИН, на котором прошла последняя транза не из списка, вызвать ф-ю Рефанда транзакции
# TODO: отправка итогового репорта в телеграм чат

# fp = core_functions.browser_init()
# browser = core_functions.browser_open(fp)
# core_functions.login_Konnektive(browser, config.seleniumUserName, config.seleniumPassword)
#
#
#
#
#
#
# brows_URL = 'https://crm.konnektive.com/merchants/binmapping/'
# browser.get(brows_URL)
# core_functions.wait_until_element_visible(browser, By.CSS_SELECTOR, '#-row-1 > td:nth-child(1)')
#
# RowsCount = len(browser.find_elements_by_tag_name('tr'))
#
# binList = []
# for counter in range(RowsCount-1):
#     CyclePathStartRange = f'#-row-{str(counter + 1)} > td:nth-child(3)'
#     StartRangeValue = browser.find_element_by_css_selector(CyclePathStartRange).text
#     binList.append(StartRangeValue)


# cardBinListCross = StartRangeValue in BinList
# if cardBinListCross:
#     CyclePathEditButton = '#-row-' + str(counter + 1) + ' > td:nth-child(8) > span:nth-child(1)'
#     browser.find_element_by_css_selector(CyclePathEditButton).click()
#     core_functions.wait_until_element_visible(
#         By.CSS_SELECTOR, '.checkbox > label:nth-child(1) > input:nth-child(1')
#     browser.find_element_by_css_selector('.checkbox > label:nth-child(1) > input:nth-child(1)').click()
#     browser.find_element_by_css_selector('input.btn').click()
#     sleep(30)


# browser.close()
# conn_info=core_functions.vertica_DB_connector(config.vertica_DB_host,
#                      config.vertica_DB_port,
#                      config.vertica_DB_login,
#                      config.vertica_DB_password,
#                      config.vertica_DB_dbname,
#                      unicode_error='strict',
#                      ssl=False,
#                      use_prepared_statements=False,
#                      connection_timeout='5')

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
	'connection_timeout': 5
	}
with vertica_python.connect(**conn_info) as connection:
	cur = connection.cursor()
	SQLRequest = "SELECT * from vertica.checkout.transactions WHERE co_status='Refunded' LIMIT 10;"
	cur.execute(SQLRequest)
	for row in cur.iterate():
		print(row)
	print(cur.fetchall())
connection.close()

