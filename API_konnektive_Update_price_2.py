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
cardBinList = [
    '627252',
    '520915',
    '416363',
    '453220',
    '468762',
    '524632',
    '531175',
    '456364',
    '455561',
    '474180',
    '493542',
    '493511',
    '423067',
    '531172',
    '480160',
    '416377',
    '528287',
    '558626',
    '454727',
    '535133',
    '546491',
    '522694',
    '411786',
    '543305',
    '510171',
    '402425',
    '531170',
    '522701',
    '456542',
    '546985',
    '526739',
    '558793',
    '540058',
    '531174',
    '459819',
    '533862',
    '487710',
    '543251',
    '548102',
    '526736',
    '546982',
    '518962',
    '534223',
    '546986',
    '558686',
    '548398',
    '531154',
    '408443',
    '531247',
    '552963',
    '408089',
    '533875',
    '670999',
    '536414',
    '530514',
    '552734',
    '429441',
    '533317',
    '534232',
    '558646',
    '531414',
    '546861',
    '437863',
    '403035',
    '402360',
    '516795',
    '540608',
    '546984',
    '539832',
    '534207',
    '434994',
    '535476',
    '403027',
    '512669',
    '535570',
    '531340',
    '489452',
    '518964',
    '526724',
    '416365',
    '542188',
    '531158',
    '527329',
    '522036',
    '402361',
    '543409',
    '520956',
    '535584',
    '474227',
    '526211',
    '483054',
    '543785',
    '520330',
    '432917',
    '535921',
    '483843',
    '432919',
    '432918',
    '456335',
    '419704',
    '416028',
    '529948',
    '535586',
    '554811',
    '527345',
    '400318',
    '546980',
    '524694',
    '447149',
    '531833',
    '531176',
    '520014',
    '542763',
    '525621',
    '406390',
    '486470',
    '522239',
    '427324',
    '494331',
    '527378',
    '487724',
    '527360',
    '535590',
    '469170',
    '409932',
    '493549',
    '510247',
    '554360',
    '553389',
    '413428',
    '535426',
    '498802',
    '402574',
    '411788',
    '427380',
    '544148',
    '534924',
    '489464',
    '489460',
    '540610',
    '474503',
    '539152',
    '414049',
    '530826',
    '676403',
    '535463',
    '465943',
    '432920',
    '499807',
    '522069',
    '528097',
    '409928',
    '520012',
    '525503',
    '409933',
    '487717',
    '483063',
    '549532',
    '531341',
    '483045',
    '517515',
    '409930',
    '524626',
    '446256',
    '402041',
    '528158',
    '495000',
    '409934',
    '547461',
    '431940',
    '520989',
    '547176',
    '546983',
    '549001',
    '401875',
    '510079',
    '459812',
    '438152',
    '401820',
    '530772',
    '485802',
    '493590',
    '490117',
    '459825',
    '455777',
    '445471',
    '428999',
    '558687',
    '541962',
    '474178',
    '434960',
    '432983',
    '409442',
    '554593',
    '531260',
    '513659',
    '497402',
    '493514',
    '492296',
    '477900',
    '465942',
    '416313',
    '402547',
    '416334',
    '458179',
    '519004',
    '464971',
    '516109',
    '441168',
    '533840',
    '475129',
    '453755',
    '557484',
    '535552',
    '530446',
    '528838',
    '546805',
    '457662',
    '533217',
    '446259',
    '533669',
    '537434',
    '516744',
    '558475',
    '432610',
    '535522',
    '540049',
    '536545',
    '484657',
    '421357',
    '421355',
    '526759',
    '497291',
    '521729',
    '526740',
    '424946',
    '510022',
    '413561',
    '419990',
    '528397',
    '417631',
    '533307',
    '522680',
    '539976',
    '529913',
    '467094',
    '497410',
    '493560',
    '476389',
    '546955',
    '532180',
    '516746',
    '513163',
    '513162',
    '465560',
    '453978',
    '409929',
    '403731',
    '400325',
    '541344',
    '549548',
    '535473',
    '534624',
    '459440',
    '433719',
    '522842',
    '677571',
    '676164',
    '557014',
    '536550',
    '530993',
    '525477',
    '485752',
    '477044',
    '454832',
    '450910',
    '450455',
    '440255',
    '434961',
    '433592',
    '429154',
    '428303',
    '427432',
    '424732',
    '424060',
    '421633',
    '407571',
    '406224',
    '403089',
    '553435',
    '552660',
    '539701',
    '494025',
    '407464',
    '497932',
    '531935',
    '475117',
    '548667',
    '544958',
    '544006',
    '523718',
    '522675',
    '517805',
    '513776',
    '492010',
    '455103',
    '424671',
    '418928',
    '676181',
    '558278',
    '557883',
    '546988',
    '546987',
    '545168',
    '542815',
    '541556',
    '540776',
    '539853',
    '531647',
    '526274',
    '512750',
    '497490',
    '493554',
    '492298',
    '479649',
    '472684',
    '453979',
    '432439',
    '431947',
    '423608',
    '420134',
    '409925',
    '409036',
    '546010',
    '540117',
    '525591',
    '521805',
    '513130',
    '493598',
    '476358',
    '416575',
    '515589',
    '493770',
    '491832',
    '431932',
    '427938',
    '427620',
    '414366',
    '412752',
    '410232',
    '409360',
    '522055',
    '453973',
    '676115',
    '535142',
    '526927',
    '412516',
    '406252',
    '676241',
    '675761',
    '559243',
    '558795',
    '557907',
    '557506',
    '555949',
    '554586',
    '554522',
    '552651',
    '552490',
    '552213',
    '548968',
    '546938',
    '545159',
    '544915',
    '544677',
    '544567',
    '544322',
    '543933',
    '542418',
    '539665',
    '537673',
    '536295',
    '536058',
    '535585',
    '535520',
    '535297',
    '534860',
    '533989',
    '533224',
    '533148',
    '532541',
    '532196',
    '531284',
    '531106',
    '530380',
    '529097',
    '528398',
    '525303',
    '524886',
    '523400',
    '523256',
    '523253',
    '523150',
    '521892',
    '520998',
    '518869',
    '516968',
    '516834',
    '516762',
    '516376',
    '516366',
    '516053',
    '511674',
    '511054',
    '499001',
    '498803',
    '497953',
    '497696',
    '496611',
    '495083',
    '495016',
    '492915',
    '491780',
    '491014',
    '485738',
    '483886',
    '483316',
    '480161',
    '478769',
    '473865',
    '472409',
    '466245',
    '465902',
    '462437',
    '462287',
    '459624',
    '459489',
    '459413',
    '457418',
    '456882',
    '455237',
    '455183',
    '454703',
    '454312',
    '453223',
    '452520',
    '451607',
    '450197',
    '446296',
    '446295',
    '441104',
    '441048',
    '440577',
    '433595',
    '432739',
    '429599',
    '427766',
    '427343',
    '426684',
    '426374',
    '425122',
    '423121',
    '422309',
    '422240',
    '421821',
    '421144',
    '420767',
    '419644',
    '419503',
    '419037',
    '413502',
    '412720',
    '411093',
    '410970',
    '406583',
    '405071',
    '403541',
    '402042',
    '402007',
    '400770',
    '400361',
    '400268',
    '558158',
    '510020',
    '485720',
    '530558',
    '427638',
    '432479',
    '431946',
    '537514',
    '516901',
    '494116',
    '551898',
    '539697',
    '532080',
    '457013',
    '415185',
    '498596',
    '530039',
    '468918',
    '421410',
    '557522',
    '525855',
    '454846',
    '421584',
    '410089',
    '542226',
    '539659',
    '529886',
    '512972',
    '510199',
    '498406',
    '489377',
    '474581',
    '440942',
    '438153',
]
price = '69.90'
inputFilename = "update_price2.csv"
# _______________________________________________________________________________
inputFilePath = "C:\\Users\\GuestUser\\Desktop\\AF decline cascading\\"
loginId = config.loginId
password = config.password
i = 0
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
        outputFilename = "price increase IT " + datetime.date.today().strftime("%d.%m.%Y") + ".csv"

        urlUpdatePurchase1 = 'https://api.konnektive.com/transactions/query/?' \
                             'loginId=' + \
                             loginId + \
                             '&password=' + \
                             password + \
                             '&customerId=' + \
                             customerId
        # '&nextBillDate=' + \
        # nextBillDate
        r = requests.post(urlUpdatePurchase1)
        responseUpdatePurchase = requests.post(urlUpdatePurchase1)
        parseResponseUpdatePurchase = responseUpdatePurchase.json()
        try:
            cardBin = parseResponseUpdatePurchase['message']['data'][0]['cardBin']
            customerPhone = parseResponseUpdatePurchase['message']['data'][0]['phoneNumber']
        except:
            print('Incorrect input data for file line: ' + str(line))
        print(customerId, cardBin)
        cardBinListCross = cardBin in cardBinList
        if cardBinListCross:
            i = i + 1
            if i%2==0:
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
                    stringWriter = costumerEmail, purchaseId, resultApiCall1, messageApiCall1, cardBin, \
                                   customerPhone
                    writer = csv.writer(file)
                    writer.writerow(stringWriter)
                print(costumerEmail, purchaseId, resultApiCall1, messageApiCall1, cardBin, customerPhone, i)
