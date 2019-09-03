import json
import requests
import config
from requests import HTTPError
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter


loginId = config.loginId
password = config.password
orderId = ''
purchaseId = ''
customerId = '765725'
txnType = ''
paySource = ''
responseType = ''
merchantTxnId = ''
clientTxnId = ''
merchantId = ''
cardLast4 = ''
cardBin = ''
achAccountNumber = ''
achRoutingNumber = ''
isChargedback = ''
firstName = ''
lastName = ''
companyName = ''
address1 = ''
address2 = ''
postalCode = ''
city = ''
state = ''
country = ''
emailAddress = ''
phoneNumber = ''
affId = ''
showExternal = ''
dateRangeType = ''
startDate = ''
endDate = ''
startTime = ''
endTime = ''
sortDir = ''
resultsPerPage = ''
page = ''



# _______________________________________________________________________________
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
def konnektiveTransactionsQuery():
    PARAMS = {
        'loginId': loginId,
        'password': password,
        'orderId': orderId,
        'purchaseId': purchaseId,
        'customerId': customerId,
        'txnType': txnType,
        'paySource': paySource,
        'responseType': responseType,
        'merchantTxnId': merchantTxnId,
        'clientTxnId': clientTxnId,
        'merchantId': merchantId,
        'cardLast4': cardLast4,
        'cardBin': cardBin,
        'achAccountNumber': achAccountNumber,
        'achRoutingNumber': achRoutingNumber,
        'isChargedback': isChargedback,
        'firstName': firstName,
        'lastName': lastName,
        'companyName': companyName,
        'address1': address1,
        'address2': address2,
        'postalCode': postalCode,
        'city': city,
        'state': state,
        'country': country,
        'emailAddress': emailAddress,
        'phoneNumber': phoneNumber,
        'affId': affId,
        'showExternal': showExternal,
        'dateRangeType': dateRangeType,
        'startDate': startDate,
        'endDate': endDate,
        'startTime': startTime,
        'endTime': endTime,
        'sortDir': sortDir,
        'resultsPerPage': resultsPerPage,
        'page': page,
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
    # обращение к  элементу konnektiveTransactionsQuery()[0] = parseResponseUrlDict
    # print(konnektiveTransactionsQuery()[0]['message']['data'][1])


print(konnektiveTransactionsQuery()[0]['message']['data'][1])
# ResponseJSON = konnektiveTransactionsQuery()
# if ResponseJSON['result'] == 'SUCCESS':
#     print(ResponseJSON['message']['totalResults'])
# elif ResponseJSON['result'] == 'ERROR':
#     print(ResponseJSON['result'], ResponseJSON['message'])
