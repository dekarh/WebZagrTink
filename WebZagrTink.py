# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import sys
import time
import openpyxl
from openpyxl import Workbook
from openpyxl.writer.write_only import WriteOnlyCell
import NormalizeFields as norm
import datetime

LOGIN = 'cca433779_ff1'
PASSWORD = '03124edbfe9'
AUTHORIZE_PAGE = 'https://brokers.tcsbank.ru/pages/auth/'
FILL_FORM_PAGE = 'https://brokers.tcsbank.ru/pages/form/'
# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

conformity = [[0,'Фамилия','Фамилия'],
              [1,'Имя', 'Имя'],
              [2,'Отчество', 'Отчество'],
              [3,'Дата рождения', 'Дата рождения'],
              [4,'Место рождения', 'Место рождения'],
              [5,'Пол', 'Пол'],
              [6,'СНИЛС', 'СНИЛС'],
              [7,'Адрес -Индекс', 'Почтовый индекс'],
              [8,'Город', 'Город прописки'],
              [9,'Улица', 'Улица прописки'],
              [10,'Дом', 'Номер дома'],
              [11,'Квартира', 'Номер квартиры'],
              [12,'Документ-Серия', 'Серия и номер паспорта'],
              [13,'Номер', 'Серия и номер паспорта'],
              [14,'Кем выдан', 'Кем выдан'],
              [15,'Дата', 'Паспорт выдан'],
              [16,'Телефон', 'Контактный номер телефона'],
              [17,'89648846302', 'Телефон для получения СМС']
              ]



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


def fill_form(driver, row, head2):                                          #row строка, а head2 - заголовок excel
    conformity_i = []
    for z, zj in enumerate(conformity):
        conformity_i.append(zj[1])
    time.sleep(5)
    elems = driver.find_elements_by_tag_name('label')                       # все поля label из web-страницы
    for z in elems:
        if z.text == 'Даю согласие на обработку персональных данных':
            z.click()
            break
    for jj, j in enumerate(conformity):
        for i in elems:                                                     # i - текущее поле ввода web-страницы
            if i.text == j[2]:                                     # сравниваем наш массив и текст поля ввода web-страницы
                elem_id = driver.find_element_by_id(i.get_attribute('for')) # экземпляр нужного поля ввода
                e = ''
                if i.text == 'Пол':                                         # исключая эти случаи
                    if str(row[conformity_i.index(j[1])]) == '1':
                        e += i.get_attribute('for') + '_1'
                    elif str(row[conformity_i.index(j[1])]) == '0':
                        e += i.get_attribute('for') + '_2'
                    elem_id = driver.find_element_by_id(e)
                    elem_id.click()
                    continue

                if j[1] == 'Номер':                                            # исключая эти случаи
                    e = i.get_attribute('for').replace('series', 'number')
                    elem_id = driver.find_element_by_id(e)
                    elem_id.send_keys(norm.normalize_index(str(row[conformity_i.index(j[1])])))
                    continue

                if j[1] == 'Документ-Серия':                                            # исключая эти случаи
                    string = norm.normalize_number(str(row[conformity_i.index(j[1])]))
                    elem_id.send_keys(string)
                    continue


                if i.text == 'Контактный номер телефона' and elem_id.get_attribute('name') == 'phone.prefix':
                    string = norm.normalize_phone_number(str(row[conformity_i.index(j[1])]))
                    if string == norm.ERROR_VALUE:
                        string = '89648846302'
                    string = string[1:4]
                    elem_id.send_keys(string)

                    e = i.get_attribute('for').replace('prefix', 'number')
                    elem_id = driver.find_element_by_id(e)
                    string = norm.normalize_phone_number(str(row[conformity_i.index(j[1])]))
                    if string == norm.ERROR_VALUE:
                        string = '89648846302'
                    string = string[4:]
                    elem_id.send_keys(string)
                    continue

                if i.text == 'Телефон для получения СМС' and elem_id.get_attribute('name') == 'mobilePhone.prefix':
                    string = '89648846302'
                    string = string[1:4]
                    elem_id.send_keys(string)

                    e = i.get_attribute('for').replace('prefix', 'number')
                    elem_id = driver.find_element_by_id(e)
                    string = '89648846302'
                    string = string[4:]
                    elem_id.send_keys(string)
                    continue

                if i.text == 'Дата рождения':
                    string = norm.normalize_date(str(row[conformity_i.index(j[1])]))
                    elem_id.send_keys(string)
                    continue

                if i.text == 'Паспорт выдан':
                    string = norm.normalize_date(str(row[conformity_i.index(j[1])]))
                    elem_id.send_keys(string)
                    continue

                elem_id.send_keys(Keys.HOME)
                elem_id.send_keys(norm.normalize_text(row[conformity_i.index(j[1])]))

    elems[0].click()
    time.sleep(1)
    # Отправка формы нажатием кнопки
    elem = driver.find_element_by_name("Verify")
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_name("Confirm")
    elem.click()
    dubl = 'Дубль - '
    try:
        time.sleep(1)
        elem = driver.find_element_by_name('Debug')
        elem.click()
        time.sleep(1)
        elem = driver.find_element_by_name('ok')
        elem.click()
        time.sleep(1)
    except NoSuchElementException:
        dubl = ''
        time.sleep(1)
    elem = driver.find_element_by_tag_name('a')
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_name('yes')
    elem.click()

#    elems = driver.find_elements_by_tag_name('button')
#    elems[2].click()

#    elem = driver.find_elements_by_id("btn-home")
#    elem = driver.find_element_by_class_name("modal-body")
#    e = elem.find_element_by_tag_name('input')
##    MOBILE_COD = input('Введите СМС:')   # Пока СМСки для подтверждения не нужны
#    MOBILE_COD = '1234'
#    e.send_keys(MOBILE_COD)
#    elem.click()
#    x5 = driver.find_elements_by_tag_name('button')
#    e = elem.find_element_by_tag_name('input') # просто так
    time.sleep(1)
    return dubl


# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
driver = webdriver.Chrome()  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

driver.get(FILL_FORM_PAGE)  # Открытие страницы

authorize(driver, LOGIN, PASSWORD)  # Авторизация

dbconfig = read_db_config()
conn = MySQLConnection(**dbconfig)
cursor = conn.cursor()
try:
    sql = "SELECT banks.bank_id, banks.bank_name, banks.type_rasch, banks.per_day, banks.koef_185_fz, " \
          "gar_banks.delta, gar_banks.summ, gar_banks.perc_fz_44, gar_banks.min_fz_44 FROM gar_banks,banks" \
          " WHERE (gar_banks.bank_id = banks.bank_id) AND (banks.per_day = TRUE) AND (gar_banks.delta >= %s)" \
          " AND (gar_banks.summ >= %s) ORDER BY (gar_banks.delta - %s), (gar_banks.summ - %s)"
    cursor.execute(sql, (delta.days, summ, delta.days, summ))
    rows = cursor.fetchall()

    b_bank_id = {}
    b_bank_name = {}
    b_type_rasch = {}
    b_per_day = {}
    b_koef_185_fz = {}
    b_delta = {}
    b_summ = {}
    b_perc_fz_44 = {}
    b_min_fz_44 = {}

    for row in rows:
        if b_bank_name.get(row[0]) == None:
            b_bank_id[row[0]] = row[0]

errors = []
date_err = []
longs = []
head = []
for j, sj in enumerate(ws_read.rows):
    for k, qk in enumerate(sj):                             # заголовок
         head.append(qk.value)
    break

for i, ii in enumerate(ws_read.rows):                       # главный цикл по строчкам
    if i == 0:
        continue
    row = []
    for jj, j in enumerate(conformity):                     # формируем row в соотв с conformity
        for k, qk in enumerate(ii):
            if k < len(head):
                if head[k] == j[1]:
                    if qk.value == 'None' or qk.value == None:
                        row.append('')
                    else:
                        row.append(qk.value)
                    break
    had = False
    for k, fj in enumerate(loaded):
        if fj == row[6]:
            had = True
    for k, fj in enumerate(errors):
        if fj == row[6]:
            had = True
    for k, fj in enumerate(date_err):
        if fj == row[6]:
            had = True
    for k, fj in enumerate(longs):
        if fj == row[6]:
            had = True
    if had:
        continue
    exl_err = False
    for k, fj in enumerate(row):
        if not (k == 7 or k == 9 or k == 10 or k == 11):
            if fj == '':
                exl_err = True
                exl_type = 'Не заполнена колонка ' + conformity[k][1]
    if exl_err:
        errors.append([row[6],exl_type])
        continue
    elif row[15].date() > datetime.date.today():
        errors.append([row[6],'Паспорт выдан в будущем'])
        continue
    elif row[3].date() > datetime.date.today():
        errors.append([row[6], 'Человек родился в будущем'])
        continue
    elif (row[15] - row[3]).days < 5113:
        date_err.append(row[6])
        continue
    elif len(row[14]) >= 100:
        longs.append(row[6])
        continue
    else:
        try:
            dd = fill_form(driver, row, head)
            loaded.append(row[6])
        except:
            errors.append([row[6],'Поле не определено'])
            wb_out = Workbook(write_only=True)
            ws_write = wb_out.create_sheet('Загружено')
            ws_err = wb_out.create_sheet('Ошибки')
            ws_date = wb_out.create_sheet('Паспорт выдан раньше 14')
            ws_long = wb_out.create_sheet('Кем выдан > 100 симв')
            for ik, jkl in enumerate(loaded):
                cell = WriteOnlyCell(ws_write, value=jkl)
                ws_write.append([cell])
            for ik, jkl in enumerate(errors):
                cell = WriteOnlyCell(ws_err, value=jkl[0])
                cell2 = WriteOnlyCell(ws_err, value=jkl[1])
                ws_err.append([cell, cell2])
            for ik, jkl in enumerate(date_err):
                cell = WriteOnlyCell(ws_date, value=jkl)
                ws_date.append([cell])
            for ik, jkl in enumerate(longs):
                cell = WriteOnlyCell(ws_long, value=jkl)
                ws_long.append([cell])
            f = sys.argv[1].replace(sys.argv[1].split('/')[-1], 'err_' + sys.argv[1].split('/')[-1])
            wb_out.save(f)
            driver.close()
            driver = webdriver.Chrome()  # Инициализация драйвера
            driver.get(FILL_FORM_PAGE)  # Открытие страницы
            authorize(driver, LOGIN, PASSWORD)  # Авторизация
            continue
#    now_time = datetime.datetime.now()
#    print(dd, i, row[2], row[3], row[4], now_time.strftime("%M:%S"))

wb_out = Workbook(write_only=True)
ws_write = wb_out.create_sheet('Загружено')
ws_err = wb_out.create_sheet('Ошибки')
ws_date = wb_out.create_sheet('Паспорт выдан раньше 14')
ws_long = wb_out.create_sheet('Кем выдан > 100 симв')
for ik, jkl in enumerate(loaded):
    cell = WriteOnlyCell(ws_write, value=jkl)
    ws_write.append([cell])
for ik, jkl in enumerate(errors):
    cell = WriteOnlyCell(ws_err, value=jkl[0])
    cell2 = WriteOnlyCell(ws_err, value=jkl[1])
    ws_err.append([cell, cell2])
for ik, jkl in enumerate(date_err):
    cell = WriteOnlyCell(ws_date, value=jkl)
    ws_date.append([cell])
for ik, jkl in enumerate(longs):
    cell = WriteOnlyCell(ws_long, value=jkl)
    ws_long.append([cell])
f = sys.argv[1].replace(sys.argv[1].split('/')[-1], 'err_' + sys.argv[1].split('/')[-1])
wb_out.save(f)
driver.close()

