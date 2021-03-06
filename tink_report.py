# -*- coding: utf-8 -*-
# Робот, ежедневно загружающий отчет из Tinkoff в Сатурн

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import sys
import difflib
from mysql.connector import MySQLConnection, Error

from lib import read_config, lenl, s_minus
from lib_scan import wj, p
# from tink_env import

import time
import datetime

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

localtity = {
'От' : {'t': 'x', 's': '//INPUT[@name="date_from"]'}, #
'До' : {'t': 'x', 's': '//INPUT[@name="date_to"]' }, #
'КнопкаПоиск' : {'t': 'x', 's': '//INPUT[@value="Поиск"]' },
'ТаблицаСтроки' : {'t': 'x', 's': '//TABLE[@class="content"]//TR[not(@class="thead")]' },
'ТаблицаЯчейки' : {'t': 'x', 's': '//TABLE[@class="content"]//TR[not(@class="thead")]/TD', 'a': 'text'},

}
statuses = {'Новая': 0, 'В рассмотрении': 1, 'Отказ': 2, 'Одобрена': 3, 'Не отправлена - Ошибка в данных': 4,
            'Отправлена в Банк': 5, 'Зависла в Банке': 6, 'Исправлена в Банке - исправьте ФИО': 7}


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

#----------------------- Нужно в алгоритме все делать, так не работает

#write_cursor = conn.cursor()       # Если болльше трех дней рассматривают - посылаем заявку заново
#write_cursor.execute('UPDATE saturn_fin.contracts SET status_code = 0 WHERE transaction_date < DATE_SUB(NOW(),'
#                     ' INTERVAL 3 DAY) and (status_code = 1 or status_code = 5)')
#conn.commit()

elem = p(d=driver, f='c', **localtity['До'])
wj(driver)
dt = datetime.datetime.now()
for iq in range(1, 20):
    elem.send_keys(Keys.BACKSPACE)
wj(driver)
elem.send_keys(dt.strftime("%d.%m.%Y"))
wj(driver)
elem = p(d=driver, f='c', **localtity['От'])
wj(driver)
dt += datetime.timedelta(weeks=-3)     # !!!!! на 3 недели назад смотрим
for iq in range(1, 20):
    elem.send_keys(Keys.BACKSPACE)
wj(driver)
elem.send_keys(dt.strftime("%d.%m.%Y"))
wj(driver)
elem = p(d=driver, f='c', **localtity['КнопкаПоиск'])
wj(driver)
elem.click()

fios_t = []
dates_t= []
types_t = []
statuses_t = []
elems = p(d=driver, f='ps', **localtity['ТаблицаСтроки'])
n_strok = len(elems)
elems = p(d=driver, f='ps', **localtity['ТаблицаЯчейки'])
for i in range(0, n_strok):
    fios_t.append(elems[i*4])
    dates_t.append(elems[i*4+1])
    types_t.append(elems[i*4+2])
    statuses_t.append(elems[i*4+3])

cursor = conn.cursor()
cursor.execute('SELECT b.client_id, b.status_code, a.p_surname, a.p_name, a.p_lastname, b.transaction_date '
        'FROM clients AS a INNER JOIN contracts AS b ON a.client_id=b.client_id WHERE b.inserted_date >= %s;', (dt,))
rows = cursor.fetchall()
for row in rows:
    if row[5] != None:                                          # Точное совпадение ФИО
        not_found = True
        fio_db = row[2].strip() + ' ' + row[3].strip()[0] + '. ' + row[4].strip()[0] + '.'
        for i, fio_t in enumerate(fios_t):
            fio_html = fio_t.strip().replace('  ', ' ').replace('  ', ' ')
            if fio_html ==  fio_db and (datetime.datetime.strptime(dates_t[i].strip(), '%d.%m.%Y')
                                            - row[5]) < datetime.timedelta(days=2):
                not_found = False
                if statuses[statuses_t[i]] != row[1]:
                    write_cursor = conn.cursor()
                    write_cursor.execute('UPDATE contracts SET status_code=%s WHERE client_id=%s AND id>-1',
                                         (statuses[statuses_t[i]], row[0]))
                    conn.commit()

        if not_found and row[1] not in [2, 3]:              # Ошибка в ФИО
            differenses = []
            for i, fio_t in enumerate(fios_t):
                fio_html = fio_t.strip().replace('  ', ' ').replace('  ', ' ')
                differenses.append(1000)
                d = difflib.Differ()
                if (datetime.datetime.strptime(dates_t[i].strip(), '%d.%m.%Y') - row[5]) < datetime.timedelta(days=2):
                    differenses[i] = 0
                    diff = d.compare(fio_db,fio_html)
                    diff_rezs = '\n'.join(diff).split('\n')
                    for diff_rez in diff_rezs:
                        if diff_rez[0] != ' ':
                            differenses[i] += 1
            if min(differenses) <= 4:                     # Допускаем только 4 и меньше ошибок
                not_found = False
                error_message = 'В Банке ' + fio_db + ' было исправлено на ' + \
                              fios_t[differenses.index(min(differenses))].strip().replace('  ', ' ').replace('  ', ' ')\
                              + ' Если Вы согласны с этим исправлением - отредактируйте ФИО в паспортных данных.'
                write_cursor = conn.cursor()
                write_cursor.execute('UPDATE contracts SET status_code=7, error_message=%s WHERE client_id=%s AND id>-1',
                                     (error_message, row[0]))
                conn.commit()
                                                                                # ФИО не найдено - зависла в Банке
        if not_found and (datetime.datetime.now() - row[5]) > datetime.timedelta(days=3) and row[1] not in [2, 3]:
            write_cursor = conn.cursor()
            write_cursor.execute('UPDATE contracts SET status_code=6 WHERE client_id=%s AND id>-1', (row[0],))
            conn.commit()

driver.close()

