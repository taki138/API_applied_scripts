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
import core_functions

# TODO: в корфункшинс вынгести функцию логина в админку
# TODO: в корфункшинс вынгести функцию проверки наличия БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию выборку SQL из БД клиентов, котоые будут чарджиться завтра
# TODO: в корфункшинс вынгести функцию проверки БИНа в бинмаппинге
# TODO: в корфункшинс вынгести функцию Импорт Ордер
# TODO: в корфункшинс вынгести функцию Рефанда транзакции
# TODO: провести проверку, если БИН, на котором прошла последняя транза не из списка, вызвать ф-ю Рефанда транзакции
# TODO: отправка итогового репорта в телеграм чат

fp = core_functions.browser_init()
browser = core_functions.browser_open(fp)
core_functions.login_Konnektive(browser, config.seleniumUserName, config.seleniumPassword)
