# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import sys
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import openpyxl
from openpyxl import Workbook
from openpyxl.writer.write_only import WriteOnlyCell
import NormalizeFields as norm
import datetime
import time

LOGIN = 'cca433779_ff1'
PASSWORD = '03124edbfe9'
AUTHORIZE_PAGE = 'https://brokers.tcsbank.ru/pages/auth/'
FILL_FORM_PAGE = 'https://brokers.tcsbank.ru/pages/form/'
# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'
clicktity = {
               "mobile_verified"        : "1" # Звонок на этот мобильный телефон (вычисляемое)
             , "amnesia_reg"            : "IF(a.p_postalcode=0 OR a.p_postalcode=111111,1,0)"  # Индекс =рег - не помню
             , "reg_addr_is_home_addr"  : "0"  # Адрес проживания такой же?
             , "amnesia_home"           : "IF(a.d_postalcode=0 OR a.d_postalcode=111111,1,0)"  # Индекс =прож - не помню
             , "no_home_phone"          : "IF(b.landline_phone<70000000000 OR b.landline_phone IS null,1,0)"  # Нет стац. телефона
             , "not_official"           : "b.unofficial_employment_code"  # Свой бизнес не официальный?
             , "amnesia_work"           : "IF(b.w_postalcode=0 OR b.w_postalcode=111111,1,0)"  # Индекс =раб - не помню
             }

inputtity = {
               "surname"                            : "a.p_surname"    # Фамилия
             , "name"                               : "a.p_name"    # Имя
             , "patronymic"                         : "a.p_lastname"    # Отчество
             , "phone_mobile"                       : "a.phone_personal_mobile-70000000000"    # Мобильный телефон
             , "email"                              : "a.email"    # Электронная почта
             , "id_code_number"                     : "CONCAT_WS('',a.p_seria,a.p_number)"    # Паспорт (номер и серия) (обработать?)
             , "passport_who_given"                 : "a.p_police"    # Кто выдал
             , "passport_date_given"                : "DATE_FORMAT(a.p_date,'%d%m%Y')"    # Дата выдачи
             , "id_division_code"                   : "a.p_police_code"    # Код подразделения
             , "birthdate"                          : "DATE_FORMAT(a.b_date,'%d%m%Y')"    # Дата рождения
             , "place_of_birth"                     : "CONCAT_WS(' ', a.b_country,a.b_region,a.b_district,a.b_place)"    # Место рождения
             , "addresstype_registered_postal_code" : "a.p_postalcode"    # Индекс =рег
             , "addresstype_registered_place"       : "a.p_region"    # Регион =рег
             , "addresstype_registered_area"        : "CONCAT_WS(' ',a.p_district,a.p_district_type,"
                                                      "a.p_place,a.p_place_type)"    # Район или город =рег
             , "addresstype_registered_city"        : "IF(a.p_subplace IS NULL OR CHAR_LENGTH(TRIM(a.p_subplace))=0,"
                                                      "CONCAT_WS(' ',a.p_district,a.p_district_type,"
                                                      "a.p_place,a.p_place_type),"
                                                      "CONCAT_WS(' ',a.p_subplace,a.p_subplace_type))"# Населенный пункт =рег
             , "addresstype_registered_street"      : "CONCAT_WS(' ',a.p_street,a.p_street_type)"    # Улица =рег
             , "addresstype_registered_building"    : "a.p_building"    # Дом =рег
             , "addresstype_registered_corpus"      : "a.p_corpus"    # Корпус =рег
             , "addresstype_registered_stroenie"    : ""    # Строение =рег
             , "addresstype_registered_flat"        : "a.p_flat"    # Квартира =рег
             , "addresstype_home_postal_code"       : "a.d_postalcode"    # Индекс =прож
             , "addresstype_home_place"             : "a.d_region"    # Регион =прож
             , "addresstype_home_area"              : "CONCAT_WS(' ',a.d_district,a.d_district_type,"
                                                      "a.d_place,a.d_place_type)"    # Район или город =прож
             , "addresstype_home_city"              : "IF(a.d_subplace IS NULL OR CHAR_LENGTH(TRIM(a.d_subplace))=0,"
                                                      "CONCAT_WS(' ',a.d_district,a.d_district_type,"
                                                      "a.d_place,a.d_place_type),"
                                                      "CONCAT_WS(' ',a.d_subplace,a.d_subplace_type))"    # Населенный пункт =прож
             , "addresstype_home_street"            : "CONCAT_WS(' ',a.d_street,a.d_street_type)"    # Улица =прож
             , "addresstype_home_building"          : "a.d_building"    # Дом =прож
             , "addresstype_home_corpus"            : "a.d_corpus"    # Корпус =прож
             , "addresstype_home_stroenie"          : ""    # Строение =прож
             , "addresstype_home_flat"              : "a.d_flat"    # Квартира =прож
             , "phone_home"                         : "b.landline_phone-70000000000"    # Стационарный телефон по месту проживания или регистрации
             , "additional_phone_home"              : "IF(b.landline_phone>70000000000 AND b.landline_phone IS NOT NULL,"
                                                      "NULL,IF(b.landline_phone_relatives>70000000000 AND "
                                                      "b.landline_phone_relatives IS NOT NULL,"
                                                      "b.landline_phone_relatives-70000000000,NULL))" # Дополнительный стационарный телефон
#             , "additional_phone_home_comment"      : '"родственники"' # Всегда родственники
             , "work_name"                          : "b.employment_organization"    # Наименование организации
             , "phone_work"                         : "b.employment_phone-70000000000"    # Рабочий телефон
             , "account_duration_years"             : "FLOOR(TRUNCATE(b.employment_experience_months/12,0))"    # Сколько лет работаю
             , "account_duration_months"            : "FLOOR(b.employment_experience_months-TRUNCATE"
                                                      "(b.employment_experience_months/12,0)*12)"    # Сколько месяцев работаю
             , "addresstype_work_postal_code"       : "b.w_postalcode"    # Индекс =раб
             , "addresstype_work_place"             : "b.w_region"    # Регион =раб
             , "addresstype_work_area"              : "CONCAT_WS(' ',b.w_district,b.w_district_type,"
                                                      "b.w_place,b.w_place_type)"    # Район или город =раб
             , "addresstype_work_city"              : "IF(b.w_subplace IS NULL OR CHAR_LENGTH(TRIM(b.w_subplace))=0,"
                                                      "CONCAT_WS(' ',b.w_district,b.w_district_type,"
                                                      "b.w_place,b.w_place_type),"
                                                      "CONCAT_WS(' ',b.w_subplace,b.w_subplace_type))"# Населенный пункт =раб
             , "addresstype_work_street"            : "CONCAT_WS(' ',b.w_street,b.w_street_type)"    # Улица =раб
             , "addresstype_work_building"          : "b.w_building"    # Дом =прож
             , "addresstype_work_corpus"            : "b.w_corpus"    # Корпус =прож
             , "addresstype_work_stroenie"          : ""     # Строение =раб
             , "addresstype_work_flat"              : "b.w_flat"    # Номер офиса =раб
             , "notwork_other_text"                 : "b.unemployment_other" # Не работаю - другое
             , "income_individual"                  : "b.personal_income"    # Персональный доход
             , "expenses_amount"                    : "b.flat_payment"    # Сумма аренды квартиры
             , "liability_n_w_amount"               : "b.banks_payment"    # Сумма платежей по тек.кредитам в др.банках
             , "desired_credit_limit"               : "b.want_amount"    # Желательная сумма кредита
            }

inputtity_first = [
                   "addresstype_registered_postal_code", "addresstype_registered_place",
                   "addresstype_registered_area", "addresstype_registered_city",
                   "addresstype_registered_street", "addresstype_registered_building",
                   "addresstype_registered_corpus", "addresstype_registered_flat", "addresstype_home_postal_code",
                   "addresstype_home_place", "addresstype_home_area", "addresstype_home_city",
                   "addresstype_home_street", "addresstype_home_building",
                   "addresstype_home_corpus", "addresstype_home_flat",
                   "addresstype_work_postal_code", "addresstype_work_place", "addresstype_work_area",
                   "addresstype_work_city", "addresstype_work_street", "addresstype_work_building",
                   "addresstype_work_corpus", "addresstype_work_flat"
                  ]

selectity = {
               "(//DIV[@class='tcs-plugin-select2'])[1]"    : "employment_status_code"# Тип занятости
             , "not_work"                                   : "unemployment_code"# !!!! Если не работаю то Кем ПРОВЕРИТЬ ИЗМЕНЕНИЯ !!!!!
             , "(//DIV[@class='tcs-plugin-select2'])[2]"    : "employment_position_code"# Если работаю то Должность
             , "(//DIV[@class='tcs-plugin-select2'])[3]"    : "status_childs_code"# Количество детей
             , "(//DIV[@class='tcs-plugin-select2'])[4]"    : "status_marital_code"# Семейное положение
             , "(//DIV[@class='tcs-plugin-select2'])[5]"    : "status_education_code"# Образование
             , "(//DIV[@class='tcs-plugin-select2'])[6]"    : "status_car_code"# Автомобиль
             , "(//DIV[@class='tcs-plugin-select2'])[7]"    : "status_credit_history_code"# Какая кредитная история
             , "(//DIV[@class='tcs-plugin-select2'])[8]"    : "status_credit_delay_code"# Просрочки по текущим кредитам
             , "(//DIV[@class='tcs-plugin-select2'])[9]"    : "driver_card_attachment_id"# Предоставит вод.удостоверение
             , "(//DIV[@class='tcs-plugin-select2'])[10]"   : "international_passport_attachment_id"# Предоставит Загранпаспорт
             , "(//DIV[@class='tcs-plugin-select2'])[11]"   : "pensioner_card_attachment_id"# Предоставит Пенс.удостоверение
             , "(//DIV[@class='tcs-plugin-select2'])[12]"   : "identity_card_mvd_attachment_id"# Предоставит Удост.офицера МВД
             , "(//DIV[@class='tcs-plugin-select2'])[13]"   : "military_card_attachment_id"# Предоставит Военный билет
             , "(//DIV[@class='tcs-plugin-select2'])[14]"   : "auto_reg_attachment_id"# Cвидетельство регистрации ТС
             , "(//DIV[@class='tcs-plugin-select2'])[15]"   : "auto_pts_attachment_id"# Оригинал ПТС
             , "(//DIV[@class='tcs-plugin-select2'])[16]"   : "auto_kasko_attachment_id"# Полис страхования КАСКО
             , "(//DIV[@class='tcs-plugin-select2'])[17]"   : "auto_osago_attachment_id"# Полис ОСАГО
             , "(//DIV[@class='tcs-plugin-select2'])[18]"   : "number_attachment_id"# Предоставит СНИЛС
             , "(//DIV[@class='tcs-plugin-select2'])[19]"   : "inn_attachment_id"# Предоставит ИНН
             , "(//DIV[@class='tcs-plugin-select2'])[20]"   : "has_2NDFL"# Предоставит 2 НДФЛ
             , "(//DIV[@class='tcs-plugin-select2'])[21]"   : "has_income_report"  # Предоставит Справку о доходах
            }

gluk_w_point = ["surname", "name", "patronymic", "passport_who_given", "place_of_birth",
                "addresstype_registered_place", "addresstype_registered_area", "addresstype_registered_city",
                "addresstype_registered_street",
                "addresstype_home_place", "addresstype_home_area", "addresstype_home_city","addresstype_home_street",
                "addresstype_work_place", "addresstype_work_area", "addresstype_work_city", "addresstype_work_street"
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


# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
driver = webdriver.Chrome()  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

authorize(driver, LOGIN, PASSWORD, AUTHORIZE_PAGE)  # Авторизация

driver.get(FILL_FORM_PAGE)  # Открытие страницы
time.sleep(1)

# Открываем БД из конфиг-файла
dbconfig = read_db_config()
conn = MySQLConnection(**dbconfig)
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
    elem = driver.find_element_by_name('reg_addr_is_home_addr') #Адреса регистрации и проживания всегда отличаются
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
        cont = False
        for j, first in enumerate(inputtity_first):
            if inp_i == first:
                cont = True
        if cont:
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
    elem = driver.find_element_by_xpath("// A[ @ href = '#'][text() = 'Оформить']") # Сохраняем
#    elem.click()  # Пока на стрелку "Сохранить" не нажимаем!!!!!

    loaded = False
    try:
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))  # Переключаемся во фрейм !!! Не работает если уже переключены
        elem = driver.find_element_by_name('surname')
        if elem.get_attribute('value') == res_inp['surname']:
            loaded = False
        else:
            loaded = True
    except NoSuchElementException:
        loaded = True
    except Exception:
        loaded = False

    j = 0



