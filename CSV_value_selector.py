import requests
import datetime
from time import sleep
import calendar
import json
import csv
import random
import core_functions
import config
import telebot

cardBinList = [
	'401030',
	'415059',
	'417174',
	'450477',
	'453332',
	'453341',
	'453342',
	'453352',
	'453397',
	'455660',
	'456215',
	'456221',
	'456233',
	'456235',
	'456239',
	'456254',
	'456263',
	'456282',
	'456283',
	'457737',
	'463219',
	'472686',
	'497039',
	'497048',
	'497152',
	'497164',
	'497204',
	'497208',
	'497222',
	'497226',
	'497230',
	'497315',
	'497367',
	'497408',
	'497446',
	'497452',
	'497456',
	'497477',
	'497500',
	'497518',
	'497519',
	'497533',
	'497539',
	'497561',
	'497563',
	'497568',
	'497616',
	'497623',
	'497685',
	'497696',
	'497862',
	'497892',
	'497940',
	'497988',
	'499001',
	'499011',
	'499023',
	'499033',
	'499050',
	'513028',
	'513029',
	'513031',
	'513104',
	'513107',
	'513284',
	'513513',
	'513536',
	'513734',
	'513742',
	'513776',
	'513782',
	'513854',
	'517365',
	'529097',
	'529430',
	'529434',
	'530446',
	'531442',
	'533317',
	'534101',
	'534111',
	'535584',
	'535586',
	'535590',
	'535611',
	'536107',
	'536115',
	'537106',
	'537964',
	'549298',
	'549538',
	'553979',
	'554591',
	'554965',
	'559618',
	]

# _______________________________________________________________________________
inputFilePath = "C:\\Users\GuestUser\\Documents\\NodeProjects\\konnektive-api-caller\\csv\\result\\"
inputFilename = '20190827_095623_success' + '.csv'
outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\csv_value_separation\\"
core_functions.check_directory_existence(outputFilePath)
outputFilename = "CSV selected values VISA FR " + datetime.date.today().strftime("%d.%m.%Y") + ".csv"


def CSVresultWriter():
	with open(outputFilePath + outputFilename, "a", newline="") as file:
		stringWriter = customerId, customerEmail, cardBin, customerPurchaseId
		writer = csv.writer(file)
		writer.writerow(stringWriter)
	print(customerId)


with open(inputFilePath + inputFilename, "r", encoding="latin-1") as f:
	lst = csv.reader(f, delimiter=',')
	for line in lst:
		customerId = line[0]
		customerEmail = line[1]
		cardBin = line[3]
		customerPurchaseId = line[4]

		cardBinListCross = cardBin in cardBinList
		if cardBinListCross:
			CSVresultWriter()

sendFileObject = core_functions.send_file_by_bot(outputFilePath, outputFilename)

print(sendFileObject.date)
