# -*- coding: utf-8 -*-
# Робот, ежедневно загружающий отчет из Tinkoff в Сатурн

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import sys
from mysql.connector import MySQLConnection, Error

from lib import read_config, lenl, s_minus
from lib_scan import wj, p
from tink_env import clicktity, inputtity, inputtity_first, selectity, select_selectity, gluk_w_point

import time
import datetime

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

localtity = {
'От' : {'t': 'x', 's': '//INPUT[@name="date_from"]'}, #
'До' : {'t': 'x', 's': '//INPUT[@name="date_to"]' }, #
'КнопкаПоиск' : {'t': 'x', 's': '//INPUT[@value="Поиск"]' }, #
}


def authorize(driver, login, password, authorize_page=''):
    if authorize_page != '':
        driver.get(authorize_page)
    # Ввод логина
    elem = driver.find_element_by_name("login")
    elem.send_keys(login)

    # Ввод пароля
    elem = driver.find_element_by_name("password")
    elem.send_keys(password)

    # Отправка формы нажатием кнопки
    elem = driver.find_element_by_name('go')
    elem.click()


# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

webconfig = read_config(filename='tink.ini', section='web')
reportconfig = read_config(filename='tink.ini', section='report')
dbconfig = read_config(filename='tink.ini', section='mysql')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(10)
authorize(driver, **webconfig)  # Авторизация
driver.get(**reportconfig)  # Открытие страницы
time.sleep(1)

conn = MySQLConnection(**dbconfig) # Открываем БД из конфиг-файла
cursor = conn.cursor()

elem = p(d=driver, f='c', **localtity['От'])
wj(driver)
elem.send_keys(datetime.date.today())
wj(driver)

cursor.execute('SELECT code,text FROM status_employment_position WHERE code >-1;')
rows = cursor.fetchall()
for row in rows:
    emptity.append(row[1])