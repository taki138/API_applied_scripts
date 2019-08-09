import requests
import datetime
import json
import csv
import config
import random
import re

# MidList = [
# '467',
# '469',
# '471',
# '473',
# '475'
# ]
# cardBinList = [
# '402360',
# '533317',
# '403027',
# '408443',
# '402361',
# '408089',
# '489452',
# '423067',
# '403035',
# '437863',
# '416334',
# '456542',
# ]
price = '69.90'
inputFilename = ""
# _______________________________________________________________________________
inputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
i = 0
with open(inputFilePath + inputFilename, "r", encoding="latin-1") as f:
    lst = csv.reader(f, delimiter=',')
    for line in lst:
        purchaseId = line[1]
        customerId = line[0]
        costumerEmail = line[2]

        loginId = config.loginId
        password = config.password
        # ListLen = len(MidList)-1
        # randomNumMID = random.randint(0, ListLen)
        # newMerchantId = MidList[randomNumMID]
        outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
        outputFilename = "price increase IT 1 cycle " + datetime.date.today().strftime("%d.%m.%Y") + ".csv"

        # urlUpdatePurchase1 = 'https://api.konnektive.com/transactions/query/?' \
        #                      'loginId=' + \
        #                      loginId + \
        #                      '&password=' + \
        #                      password + \
        #                      '&customerId=' + \
        #                      customerId
        # # '&nextBillDate=' + \
        # # nextBillDate
        # r = requests.post(urlUpdatePurchase1)
        # responseUpdatePurchase = requests.post(urlUpdatePurchase1)
        # parseResponseUpdatePurchase = responseUpdatePurchase.json()
        # try:
        #     cardBin = parseResponseUpdatePurchase['message']['data'][0]['cardBin']
        #     customerPhone = parseResponseUpdatePurchase['message']['data'][0]['phoneNumber']
        # except:
        #     print('Incorrect input data for file line: ' + str(line))
        # print(customerId, cardBin)
        # cardBinListCross = cardBin in cardBinList
        # if cardBinListCross:



        i = i + 1
        # if re.match(r'[0-6]+$', str(i)): # меняет прайс для 70% клиентов
        if i % 2 == 0: # меняетпрайс для 50% клиентов
            urlUpdatePurchase1 = 'https://api.konnektive.com/purchase/update/?' \
                                   'loginId=' + \
                                   loginId + \
                                   '&password=' + \
                                   password + \
                                   '&purchaseId=' + \
                                   purchaseId + \
                                   '&price=' + \
                                   price
                                   # '&nextBillDate=' + \
                                   # nextBillDate
            r = requests.post(urlUpdatePurchase1)
            responseUpdatePurchase = requests.post(urlUpdatePurchase1)
            parseResponseUpdatePurchase = responseUpdatePurchase.json()
            resultApiCall1 = parseResponseUpdatePurchase['result']
            messageApiCall1 = parseResponseUpdatePurchase['message']
            with open(outputFilePath + outputFilename, "a", newline="") as file:
                stringWriter = costumerEmail, purchaseId, resultApiCall1, messageApiCall1, \
                               # cardBin, customerPhone
                writer = csv.writer(file)
                writer.writerow(stringWriter)
            print(costumerEmail, purchaseId, resultApiCall1, messageApiCall1, i)
