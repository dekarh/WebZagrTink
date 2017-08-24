# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys
from mysql.connector import MySQLConnection, Error

from lib import read_config
from tink_env import clicktity, inputtity, inputtity_first, selectity, gluk_w_point

import time

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'


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
fillconfig = read_config(filename='tink.ini', section='fill')
dbconfig = read_config(filename='tink.ini', section='mysql')

driver = webdriver.Chrome()  # Инициализация драйвера
authorize(driver, **webconfig)  # Авторизация
driver.get(**fillconfig)  # Открытие страницы
time.sleep(1)

conn = MySQLConnection(**dbconfig) # Открываем БД из конфиг-файла
cursor = conn.cursor()

# Заполняем массив дурацкого  селектора "Занимаемая должность"
emptity = []
cursor.execute('SELECT code,text FROM status_employment_position WHERE code >-1;')
rows = cursor.fetchall()
for row in rows:
    emptity.append(row[1])

# Формируем SQL
sql = 'SELECT '
for i, inp_i in enumerate(clicktity):
    if str(type(clicktity[inp_i]))=="<class 'str'>" and clicktity[inp_i] != '':
        sql = sql + clicktity[inp_i] + ','

for i, inp_i in enumerate(inputtity):
    if str(type(inputtity[inp_i]))=="<class 'str'>" and inputtity[inp_i] != '':
        sql = sql + inputtity[inp_i] + ','

for i, sel_i in enumerate(selectity):
    if selectity[sel_i] != '':
        sql = sql + selectity[sel_i] + ','

sql = sql[:len(sql) - 1] + " FROM clients AS a INNER JOIN contracts AS b ON a.client_id=b.client_id WHERE b.loaded=0"

#sql = "SELECT banks.bank_id, banks.bank_name, banks.type_rasch, banks.per_day, banks.koef_185_fz, " \
#      "gar_banks.delta, gar_banks.summ, gar_banks.perc_fz_44, gar_banks.min_fz_44 FROM gar_banks,banks" \
#      " WHERE (gar_banks.bank_id = banks.bank_id) AND (banks.per_day = TRUE) AND (gar_banks.delta >= %s)" \
#      " AND (gar_banks.summ >= %s) ORDER BY (gar_banks.delta - %s), (gar_banks.summ - %s)"
#cursor.execute(sql, (delta.days, summ, delta.days, summ))
cursor.execute(sql)
rows = cursor.fetchall()

for row in rows:                    # Цикл по строкам таблицы (основной)
    j = 0
    res_cli = {}
    for i, inp_i in enumerate(clicktity):
        if str(type(clicktity[inp_i])) == "<class 'str'>" and clicktity[inp_i] != '':
            if row[j] == None:
                res_cli[inp_i] = 0
            else:
                res_cli[inp_i] = row[j]
            j += 1

    res_inp = {}
    for i, inp_i in enumerate(inputtity):
        if str(type(inputtity[inp_i])) == "<class 'str'>" and inputtity[inp_i] != '':
            res_inp[inp_i] = row[j]
            j += 1

    res_sel = {}
    for i, sel_i in enumerate(selectity):
        if selectity[sel_i] != '':
            res_sel[sel_i] = row[j]
            j += 1

# ---------------------------------- ИНИЦИАЛИЗАЦИЯ--------------------------------------------------
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe")) # Переключаемся во фрейм
    elem = driver.find_element_by_xpath('//LABEL[@for="reg_addr_is_home_addr"]') #Адреса регистрации и проживания всегда отличаются
    elem.click()
    elem = driver.find_element_by_xpath("(//DIV[@class='tcs-plugin-select2'])[1]") # Тип занятости
    elem.click()
    i = 0
    while i < res_sel["(//DIV[@class='tcs-plugin-select2'])[1]"]:
        elem.send_keys(Keys.ARROW_DOWN)
        i+=1
    elem.send_keys(Keys.ENTER)

    elem = driver.find_element_by_name("not_work") # Если не работаю то почему
    if elem.is_displayed():
        elem.click()
        i = 0
        while i < res_sel["not_work"]:
            elem.send_keys(Keys.ARROW_DOWN)
            i+=1
        elem.send_keys(Keys.ENTER)

# Занимаемая должность - не срабатывает стрелка вниз
    elem = driver.find_element_by_xpath("(//DIV[@class='tcs-plugin-select2'])[2]")
    time.sleep(1)
    if elem.is_displayed() and res_sel["(//DIV[@class='tcs-plugin-select2'])[2]"] != 0 \
            and res_sel["(//DIV[@class='tcs-plugin-select2'])[2]"] != None:
        time.sleep(1)
        elem.click()
        elem1 = driver.find_element_by_xpath("//LI[@class='tcs-plugin-select2__list-item'][text()='"
                                             + emptity[res_sel["(//DIV[@class='tcs-plugin-select2'])[2]"]] + "']")
        time.sleep(1)
        elem1.click()

# ---------------------------------- КОНЕЦ ИНИЦИАЛИЗАЦИИ----------------------------------------------

    i = 3
    while i <= 21:                                          # Все остальные выпадающие списки
        elem = driver.find_element_by_xpath("(//DIV[@class='tcs-plugin-select2'])[" + str(i) + "]")
        if elem.is_displayed() and res_sel["(//DIV[@class='tcs-plugin-select2'])[" + str(i) + "]"] != 0 \
                and res_sel["(//DIV[@class='tcs-plugin-select2'])[" + str(i) + "]"] != None:
            time.sleep(1)
            elem.click()
            time.sleep(1)
            j = 0
            while j < res_sel["(//DIV[@class='tcs-plugin-select2'])[" + str(i) + "]"]:
                elem.send_keys(Keys.ARROW_DOWN)
                j += 1
            elem.send_keys(Keys.ENTER)
        i += 1

    for i, inp_i in enumerate(res_cli):                     # Все чекбоксы
        if inp_i == 'reg_addr_is_home_addr':
            continue
        elem = driver.find_element_by_name(inp_i)
        if res_cli[inp_i] == 0 or res_cli[inp_i] == 1:
            #            time.sleep(1)
            if elem.get_attribute('value') != str(res_cli[inp_i]):
                elem.click()

    for i, inp_i in enumerate(inputtity_first):             # Первоочередные поля (строгий порядок)
        if inp_i.find('place') == -1 and inp_i.find('area') == -1:
            elem = driver.find_element_by_name(inp_i)
            if elem.is_displayed() and res_inp[inp_i] != None:
                j = 0
                while j < 30:
                    elem.send_keys(Keys.BACKSPACE)
                    j+=1
                elem.click()
    #            time.sleep(1)
                elem.send_keys(res_inp[inp_i])
                elem = driver.find_element_by_name("id_division_code")
                elem.click()
                elem.click()
    #            elem.send_keys(Keys.ENTER)
    #            j = 0

    for i, inp_i in enumerate(res_inp):
        if inp_i in inputtity_first:
            continue
        if inp_i == 'id':
            continue
        elem = driver.find_element_by_name(inp_i)
        if elem.is_displayed() and res_inp[inp_i] != None:
#            j = 0
#            while j < 30:
#                elem.send_keys(Keys.BACKSPACE)
#                j+=1
            elem.click()
#            time.sleep(1)
#-------------------------------------------------Глюколовка старт-----------------------------
            if inp_i == 'account_duration_months' or inp_i == 'account_duration_years':
                elem.send_keys(Keys.BACKSPACE,Keys.BACKSPACE,Keys.BACKSPACE)
            if inp_i in gluk_w_point:
                elem.send_keys(res_inp[inp_i].replace('.',' '))
            else:
# -------------------------------------------------Глюколовка конец-----------------------------
                elem.send_keys(res_inp[inp_i])
            elem = driver.find_element_by_name("id_division_code")
            elem.click()
            elem.click()
#            elem.send_keys(Keys.ARROW_DOWN)
#            elem.send_keys(Keys.ENTER)
    elem = driver.find_element_by_xpath("// A[ @ href = '#'][text() = 'Оформить']") # Оформить
    elem.click()  # Пока на стрелку "Сохранить" то нажимаем, то не нажимаем!!!!!

    loaded = False
    try:
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))  # Переключаемся во фрейм
    except Exception:
        loaded = False                                                     # Если уже во фрейме - ошибка
        continue
    try:
        elem = driver.find_element_by_name('surname')
        if elem.get_attribute('value') == res_inp['surname']:
            loaded = False
        else:
            loaded = True
    except NoSuchElementException:
        loaded = True
    except Exception:
        loaded = False

    if loaded:
        sql = 'UPDATE contracts SET loaded=1 WHERE client_id=%s AND id>-1'
        cursor.execute(sql, (res_inp['id'],))
        conn.commit()

# Пока выдает пустую страницу после нажатия "Оформить" и никуда не пускает. Приходится заново входить
    driver.close()
    driver = webdriver.Chrome()  # Инициализация драйвера
    authorize(driver, **webconfig)  # Авторизация
    driver.get(**fillconfig)  # Открытие страницы
    time.sleep(1)


driver.close()



