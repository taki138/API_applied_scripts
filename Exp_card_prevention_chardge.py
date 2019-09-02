import datetime

from datetime import date
from dateutil.relativedelta import relativedelta
import os
import socket
import sys
from timeit import default_timer as timer
import requests
import vertica_python
from vertica_python import errors
import config
from core_functions import check_directory_existence
from core_functions import next_mont_first_date
from core_functions import date_time_convert_verticaDB_format
from core_functions import next_mont_2_first_date
from core_functions import next_month
from core_functions import csv_first_line_writer
from core_functions import konnektivePurchaseQuery
from core_functions import csv_result_writer
from datetime import date
from dateutil.relativedelta import relativedelta
from f import pcall_wraps

scriptName = os.path.basename(__file__)
print(f'{scriptName} started')
start = timer()

# outputFilename = f'expired_cards_move_billing_date_{datetime.date.today().strftime("%d.%m.%Y")}.csv'
# outputFilePath = f'{config.outputCoreFilePath}expired_cards_move_billing\\'
# check_directory_existence(outputFilePath)
csvFirstLineWriter = 'costumerEmail', 'customerPhone', 'merchantId', 'purchaseId', 'cardBin', \
                     'resultApiCall1', 'messageApiCall1', 'customerId'

billNow = 0  # 0 - не форсится, 1 - форсится

next_mont_first_date = date_time_convert_verticaDB_format(next_mont_first_date())[1]
next_mont_2_first_date = date_time_convert_verticaDB_format(next_mont_2_first_date())[1]
SQLRequest = """
SELECT distinct(bi.konn_customerId), bi.konn_emailAddress, bi.konn_phoneNumber, bi.konn_merchantId, bi.konn_purchaseId, bi.konn_cardBin
FROM konn.bill_info AS bi
Where bi.konn_expDate > {}
  AND bi.konn_expDate < {}
  AND (bi.konn_status = 'ACTIVE' OR bi.konn_status = 'TRIAL' OR bi.konn_status = 'RECYCLE_BILLING')
group by bi.konn_customerId, bi.konn_emailAddress, bi.konn_phoneNumber, bi.konn_merchantId, bi.konn_purchaseId, bi.konn_cardBin
;
""".format(next_mont_first_date, next_mont_2_first_date)





# print(SQLRequest)


# def SQL_SELECT_from_vertica(SQLRequest):
# 	this_function_name = sys._getframe().f_code.co_name
# 	print(f"{this_function_name} started")
# 	conn_info = {
# 		'host': config.vertica_DB_host,
# 		'port': config.vertica_DB_port,
# 		'user': config.vertica_DB_login,
# 		'password': config.vertica_DB_password,
# 		'database': config.vertica_DB_dbname,
# 		# autogenerated session label by default,
# 		# 'session_label': 'some_label',
# 		# default throw error on invalid UTF-8 results
# 		'unicode_error': 'strict',
# 		# SSL is disabled by default
# 		'ssl': False,
# 		# using server-side prepared statements is disabled by default
# 		'use_prepared_statements': False,
# 		# connection timeout is not enabled by default
# 		'connection_timeout': 10
# 		}
#
# 	resultSQLList = []
#
# 	try:
# 		with vertica_python.connect(**conn_info) as connection:
# 			cur = connection.cursor()
# 			cur.execute(SQLRequest)
# 			for row in cur.iterate():
# 				resultSQLList.append(row)
# 			cur.close()
# 			connection.close()
# 	except socket.error as socketerror:
# 		print("{this_function_name}: Error: ", socketerror)
# 	except socket.timeout:
# 		print(f"{this_function_name}: NO RESPONSE")
# 	except errors.ConnectionError as err:
# 		print(f'{this_function_name}: Error occurred: {err}')
# 	finally:
# 		connection.close()
# 	print(f"{this_function_name} fullfilled")
# 	return resultSQLList
#
#
# def purchaseStatusChecker(inputPurchaseIdList: list) -> list:
# 	this_function_name = sys._getframe().f_code.co_name
# 	print(f"{this_function_name} started")
# 	resultFilteredList = []
# 	for x in inputPurchaseIdList:
# 		try:
# 			PARAMS = {
# 				'loginId': config.loginId,
# 				'password': config.password,
# 				'customerId': x[0],
# 				}
# 			requestResponce = konnektivePurchaseQuery(PARAMS)[0]
# 			result = requestResponce['result']
# 			if result == 'SUCCESS':
# 				status = requestResponce['message']['data'][0]['status']
# 				if status == 'ACTIVE' or status == 'TRIAL' or status == 'RECYCLE_BILLING':
# 					row = x[0], x[1], x[2], x[3], x[4], x[5], status
# 					resultFilteredList.append(row)
# 					print(row)
# 			elif result == 'ERROR':
# 				print(requestResponce['message'])
# 			else:
# 				print(requestResponce)
# 		except Exception as excpt:
# 			print(f'Function {this_function_name} error occurred: {excpt}')
# 	print(f'Function {this_function_name} fulfilled')
# 	return resultFilteredList
#
#
# resultSQLList = SQL_SELECT_from_vertica(SQLRequest)
# resultSQLList = purchaseStatusChecker(resultSQLList)
#
# csv_first_line_writer(outputFilePath, outputFilename, csvFirstLineWriter)
# for i in range(len(resultSQLList)):
# 	print('\t requests started')
# 	customerId = resultSQLList[i][0]
# 	costumerEmail = resultSQLList[i][1]
# 	customerPhone = resultSQLList[i][2]
# 	merchantId = resultSQLList[i][3]
# 	purchaseId = resultSQLList[i][4]
# 	cardBin = resultSQLList[i][5]
# 	purchaseStatus = resultSQLList[i][6]
#
# 	if purchaseStatus == 'ACTIVE':
# 		urlUpdatePurchase1 = 'https://api.konnektive.com/purchase/update/?' \
# 		                     'loginId=' + \
# 		                     config.loginId + \
# 		                     '&password=' + \
# 		                     config.password + \
# 		                     '&purchaseId=' + \
# 		                     purchaseId + \
# 		                     '&billNow=0' + \
# 		                     '&nextBillDate=08/31/2019'
# 		r = requests.post(urlUpdatePurchase1)
# 		responseUpdatePurchase = requests.post(urlUpdatePurchase1)
# 		parseResponseUpdatePurchase = responseUpdatePurchase.json()
# 		resultApiCall1 = parseResponseUpdatePurchase['result']
# 		messageApiCall1 = parseResponseUpdatePurchase['message']
# 		resultWritedWalues = costumerEmail, customerPhone, merchantId, purchaseId, cardBin, \
# 		                     resultApiCall1, messageApiCall1, customerId
# 		csv_result_writer(outputFilename, outputFilePath, resultWritedWalues)
# 	else:
# 		urlUpdatePurchase2 = 'https://api.konnektive.com/purchase/update/?' \
# 		                     'loginId=' + \
# 		                     config.loginId + \
# 		                     '&password=' + \
# 		                     config.password + \
# 		                     '&purchaseId=' + \
# 		                     purchaseId + \
# 		                     '&reactivate=1'
# 		r = requests.post(urlUpdatePurchase2)
# 		responseUpdatePurchase2 = requests.post(urlUpdatePurchase2)
# 		parseResponseUpdatePurchase2 = responseUpdatePurchase2.json()
# 		resultApiCall2 = parseResponseUpdatePurchase2['result']
# 		messageApiCall2 = parseResponseUpdatePurchase2['message']
#
# 		urlUpdatePurchase1 = 'https://api.konnektive.com/purchase/update/?' \
# 		                     'loginId=' + \
# 		                     config.loginId + \
# 		                     '&password=' + \
# 		                     config.password + \
# 		                     '&purchaseId=' + \
# 		                     purchaseId + \
# 		                     '&nextBillDate=08/31/2019'
#
# 		r = requests.post(urlUpdatePurchase1)
# 		responseUpdatePurchase1 = requests.post(urlUpdatePurchase1)
# 		parseResponseUpdatePurchase1 = responseUpdatePurchase1.json()
# 		resultApiCall1 = parseResponseUpdatePurchase1['result']
# 		messageApiCall1 = parseResponseUpdatePurchase1['message']
# 		resultWritedWalues = costumerEmail, customerPhone, merchantId, purchaseId, cardBin, \
# 		                     resultApiCall1, messageApiCall1, customerId
# 		csv_result_writer(outputFilename, outputFilePath, resultWritedWalues)
#
# end = timer()
# print(f'{scriptName} execution time: {end - start}')
