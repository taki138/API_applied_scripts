from builtins import len, range
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

from core_functions import browser_init, browser_open, wait_until_element_visible

fp = browser_init()
browser = browser_open(fp)

Brows_URL_MID_list = f"{config.konnektiveAdminPannelURL}/merchants/merchants/mids/"
RowsCount = len(browser.find_elements_by_tag_name('tr'))
print(RowsCount)
MIDId = 0
for MIDId in range(RowsCount - 1):
	Brows_URL = f"{config.konnektiveAdminPannelURL}/merchants/mids/edit/?billerId={MIDId}"
	print(Brows_URL)
	wait_until_element_visible(By.CSS_SELECTOR, '#-row-1 > td:nth-child(1)')
	accountCSSSelector = '# billerUniqueFields > div:nth-child(1) > input:nth-child(3)'
	accountValue = browser.find_element_by_css_selector(accountCSSSelector).text
	print(accountValue)

browser.close()
