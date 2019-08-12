import requests
import datetime
import calendar
import json
import csv
import random
import core_functions
import config
import telebot

cardBinList = [
	'450060',
	'451014',
	'451015',
	'451401',
	'451407',
	'452001',
	'452002',
	'452005',
	'452088',
	'453081',
	'453091',
	'453092',
	'453600',
	'453733',
	'453734',
	'453737',
	'454033',
	'472409',
]

# _______________________________________________________________________________
inputFilePath = "C:\\Users\GuestUser\\Documents\\NodeProjects\\konnektive-api-caller\\csv\\result\\"
inputFilename = '20190812_131703_success' + '.csv'
outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\csv_value_separation\\"
core_functions.check_directory_existence(outputFilePath)
outputFilename = "CSV selected values VISA CA " + datetime.date.today().strftime("%d.%m.%Y") + ".csv"


def CSVresultWriter():
    with open(outputFilePath + outputFilename, "a", newline="") as file:
        stringWriter = customerId, customerEmail, cardBin
        writer = csv.writer(file)
        writer.writerow(stringWriter)
    print(customerId)
with open(inputFilePath + inputFilename, "r", encoding="latin-1") as f:
    lst = csv.reader(f, delimiter=',')
    for line in lst:
        customerId = line[0]
        # customerPurchaseId = line[1]
        customerEmail = line[1]
        cardBin = line[3]

        cardBinListCross = cardBin in cardBinList
        if cardBinListCross:
            CSVresultWriter()

sendFileObject = core_functions.send_file_by_bot(outputFilePath, outputFilename)

print(sendFileObject.date)