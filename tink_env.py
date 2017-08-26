# -*- coding: utf-8 -*-
# Общие переменые и процедуры проекта WebZagrTink

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
               "id"                                 : "a.client_id" # Поле id для update b.loaded
             , "surname"                            : "a.p_surname"    # Фамилия
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

