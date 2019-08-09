import requests
import datetime
import csv
import os
import config



billNow = '1'
loginId = config.loginId
password = config.password
inputFilename = "update purchase.csv"
inputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
outputFilename = "billNow " + datetime.date.today().strftime("%d.%m.%Y") + ".csv"
outputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\BillNow Results\\"

# _______________________________________________________________________________
try:
    os.makedirs(outputFilePath)
except FileExistsError:
    # directory already exists
    pass

def CSVFirstLineWriter():
    with open(outputFilePath + outputFilename, "a", newline="") as file:
        stringWriter = 'costumerEmail', 'customerPhone', 'merchantId', 'purchaseId', 'cardBin', \
                       'resultApiCall1', 'messageApiCall1'
        writer = csv.writer(file)
        writer.writerow(stringWriter)


def CSVresultWriter():
    with open(outputFilePath + outputFilename, "a", newline="") as file:
        stringWriter = costumerEmail, customerPhone, merchantId, purchaseId, cardBin, resultApiCall1, messageApiCall1
        writer = csv.writer(file)
        writer.writerow(stringWriter)
    print(costumerEmail, purchaseId, resultApiCall1, messageApiCall1)


CSVFirstLineWriter()
with open(inputFilePath + inputFilename, "r", encoding="latin-1") as f:
    lst = csv.reader(f, delimiter=';')
    for line in lst:
        costumerEmail = line[0]
        customerPhone = line[1]
        merchantId = line[2]
        purchaseId = line[3]
        cardBin = line[6]

        url = 'https://api.konnektive.com/purchase/update/?' \
              'loginId=' + \
              loginId + \
              '&password=' + \
              password + \
              '&purchaseId=' + \
              purchaseId + \
              '&billNow=' + \
              billNow
        responseUrl = requests.post(url)
        parseResponseUrl = responseUrl.json()
        resultApiCall1 = parseResponseUrl['result']
        messageApiCall1 = parseResponseUrl['message']
        CSVresultWriter()
