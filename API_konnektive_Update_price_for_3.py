import requests
import datetime
import config
import json
import csv
import random

# MidList = [
# '467',
# '469',
# '471',
# '473',
# '475'
# ]
# cardBinList = [
#     '402360',
#     '533317',
#     '403027',
#     '408443',
#     '402361',
#     '408089',
#     '489452',
#     '423067',
#     '403035',
#     '437863',
#     '416334',
#     '456542',
# ]
price = '85.80'
inputFilename = "update_price3.csv"
# _______________________________________________________________________________
inputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
loginId = config.loginId
password = config.password
with open(inputFilePath + inputFilename, "r", encoding="latin-1") as f:
    lst = csv.reader(f, delimiter=',')
    for line in lst:
        purchaseId = line[0]
        customerId = line[1]
        costumerEmail = line[2]
        # ListLen = len(MidList)-1
        # randomNumMID = random.randint(0, ListLen)
        # newMerchantId = MidList[randomNumMID]
        outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
        outputFilename = "increase price CHE " + datetime.date.today().strftime("%d.%m.%Y") + ".csv"

        # urlUpdatePurchase1 = 'https://api.konnektive.com/transactions/query/?' \
        #                      'loginId=' + \
        #                      loginId + \
        #                      '&password=' + \
        #                      password + \
        #                      '&customerId=' + \
        #                      customerId
        # '&nextBillDate=' + \
        # nextBillDate
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
            stringWriter = costumerEmail, purchaseId, customerId
            writer = csv.writer(file)
            writer.writerow(stringWriter)
        # print(costumerEmail, purchaseId, resultApiCall1, messageApiCall1, cardBin, customerPhone)
        print(costumerEmail)