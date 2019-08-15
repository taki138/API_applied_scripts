from time import sleep

import config
import logging
import csv
from gevent import timeout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.firefox.options import Options
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
BinList = [
	'450060',
	'451014',
	'451015',
]

# __________________________________________________
opts = Options()
opts.set_headless()
assert opts.headless
def wait_until_element_visible(position_id, position_value):
    element = WebDriverWait(browser, 60).until(
        EC.visibility_of_element_located((position_id, position_value)))


browser = Firefox(options=opts)
browser.maximize_window()
WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located)
browser.get(config.konnektiveAdminPannelURL)
browser.find_element_by_name('userName').send_keys(config.seleniumUserName)
browser.find_element_by_name('password').send_keys(config.seleniumPassword)
browser.find_element_by_tag_name('button').submit()
sleep(6)
Brows_URL = 'https://crm.konnektive.com/merchants/binmapping/'
browser.get(Brows_URL)
wait_until_element_visible(By.CSS_SELECTOR, '#-row-1 > td:nth-child(1)')
try:
    RowsCount = len(browser.find_elements_by_tag_name('tr'))
    for counter in range(RowsCount-1):
        CyclePathStartRange = '#-row-' + str(counter + 1) + ' > td:nth-child(3)'
        StartRangeValue = browser.find_element_by_css_selector(CyclePathStartRange).text
        cardBinListCross = StartRangeValue in BinList
        if cardBinListCross:
            CyclePathEditButton = '#-row-' + str(counter + 1) + ' > td:nth-child(8) > span:nth-child(1)'
            browser.find_element_by_css_selector(CyclePathEditButton).click()
            wait_until_element_visible(By.CSS_SELECTOR, '.checkbox > label:nth-child(1) > input:nth-child(1')
            browser.find_element_by_css_selector('.checkbox > label:nth-child(1) > input:nth-child(1)').click()
            browser.find_element_by_css_selector('input.btn').click()
            sleep(30)
    browser.close()
    print('Done')
except:
    browser.close()
    print('Done with exception')

