# -*- coding: utf-8 -*-
# Общие переменые и процедуры проекта WebZagrTink

clicktity = {
'cMob' : {'t': 'x', 's': '//[@class="mobile_verified"]' , 'SQL': "1"}, # Звонок на этот мобильный телефон (вычисляемое)
'cIndREGAmn' : {'t': 'x', 's': '//[@class="amnesia_reg"]' , 'SQL': "IF(a.p_postalcode=0 OR a.p_postalcode=111111,1,0)"}, # Индекс =рег - не помню
'cAddrFACTtoo' : {'t': 'x', 's': '//LABEL[@for="reg_addr_is_home_addr"]' , 'SQL': "0"}, #ok Адрес проживания такой же?
'cIndFACTAmn' : {'t': 'x', 's': '//[@class="amnesia_home"]' , 'SQL': "IF(a.d_postalcode=0 OR a.d_postalcode=111111,1,0)"}, # Индекс =прож - не помню
'cNoStPhone' : {'t': 'x', 's': '//[@class="no_home_phone"]' , 'SQL': "IF(b.landline_phone<70000000000 OR b.landline_phone IS null,1,0)"}, # Нет стац. телефона
'cBisUnOfficial' : {'t': 'x', 's': '//SPAN[text()="Неофициальный бизнес"]' , 'SQL': "b.unofficial_employment_code"}, # Свой бизнес не официальный?
'cIndWORKAmn' : {'t': 'x', 's': '//[@class="amnesia_work"]' , 'SQL': "IF(b.w_postalcode=0 OR b.w_postalcode=111111,1,0)"}, # Индекс =раб - не помню
'cAddrWORKtoo' : {'t': 'x', 's': '//LABEL[@for="same_reg_home_org"]' , 'SQL': "0"}, #ok Адрес бизнеса такой же как рег?
'ПодтвМобТел' : {'t': 'x', 's': '//LABEL[@for="phone_mobile_check"]//SPAN[text()="Проверено"]' , 'SQL': "1"},
'ПодтвФамилии' : {'t': 'x', 's': '//LABEL[@for="surname_verified"]//SPAN[text()="Проверено"]' , 'SQL': "1"},
}

inputtity = {
'iId' : {'t': 'x', 's': '//[@class="id"]', 'SQL': "a.client_id"}, # Поле id для update b.loaded
'Фамилия' : {'t': 'x', 's': '//INPUT[@type="suggest"][@name="surname"]', 'SQL': "a.p_surname"}, # Фамилия
'Имя' : {'t': 'x', 's': '//INPUT[@type="suggest"][@name="name"]', 'SQL': "a.p_name"}, # Имя
'Отчество' : {'t': 'x', 's': '//INPUT[@type="suggest"][@name="patronymic"]', 'SQL': "a.p_lastname"}, # Отчество
'МобТелефон' : {'t': 'x', 's': '//INPUT[@type="tel"][@name="phone_mobile"]', 'SQL': "a.phone_personal_mobile-70000000000"}, # Мобильный телефон
'Email' : {'t': 'x', 's': '//INPUT[@type="suggest"][@name="email"]', 'SQL': "a.email"}, # Электронная почта
'СерияНомер' : {'t': 'x', 's': '//INPUT[@type="tel"][@name="id_code_number"]' , 'SQL': "CONCAT_WS('',a.p_seria,a.p_number)"}, # Паспорт (номер и серия)
'iPWho' : {'t': 'x', 's': '//[@class="passport_who_given"]' , 'SQL': "a.p_police"}, # Кто выдал
'iPDate' : {'t': 'x', 's': '//[@class="passport_date_given"]' , 'SQL': "DATE_FORMAT(a.p_date,'%d%m%Y')"}, # Дата выдачи
'КодПодразд' : {'t': 'x', 's': '//INPUT[@type="tel"][@name="id_division_code"]' , 'SQL': "a.p_police_code"}, # Код подразделения
'ДатаРождения' : {'t': 'x', 's': '//INPUT[@type="tel"][@name="birthdate"]' , 'SQL': "DATE_FORMAT(a.b_date,'%d%m%Y')"}, # Дата рождения
'МестоРождения' : {'t': 'x', 's': '//INPUT[@type="suggest"][@name="place_of_birth"]'
              , 'SQL': "CONCAT_WS(' ', a.b_country,a.b_region,a.b_district,a.b_place)"}, # Место рождения
'ИндексФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="tel"][@name="postal_code"]', 'SQL': "a.d_postalcode"}, # Индекс =факт
'РегионФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="suggest"][@name="place"]' , 'SQL': "a.d_region"}, # Регион =факт
'Район+ГородФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="suggest"][@name="area"]' ,
                    'SQL': "CONCAT_WS(' ',a.d_district_type,a.d_district,a.d_place_type,a.d_place)"}, # Район или город =факт
'НасПунктФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="suggest"][@name="city"]',
                 'SQL': "CONCAT_WS(' ',a.d_subplace_type,a.d_subplace)"}, # Населенный пункт =факт
'УлицаФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="suggest"][@name="street"]',
              'SQL': "CONCAT_WS(' ',a.d_street_type,a.d_street)"}, # Улица =рег
'ДомФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="text"][@name="building"]', 'SQL': "a.d_building"}, # Дом =факт
'КорпусФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="text"][@name="corpus"]' , 'SQL': "a.d_corpus"}, # Корпус =факт
'СтроениеФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="text"][@name="stroenie"]', 'SQL': ""}, # Строение =факт
'КвартираФАКТ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][2]//INPUT[@type="text"][@name="flat"]', 'SQL': "a.d_flat"}, # Квартира =факт
'ИндексРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="tel"][@name="postal_code"]', 'SQL': "a.p_postalcode"}, # Индекс =рег
'РегионРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="suggest"][@name="place"]', 'SQL': "a.p_region"}, # Регион =рег
'Район+ГородРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="suggest"][@name="area"]',
                    'SQL': "CONCAT_WS(' ',a.p_district_type,a.p_district,a.p_place_type,a.p_place)"}, # Район или город =рег
'НасПунктРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="suggest"][@name="city"]',
                 'SQL': "CONCAT_WS(' ',a.p_subplace_type,a.p_subplace)"}, # Населенный пункт =рег
'УлицаРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="suggest"][@name="street"]',
              'SQL': "CONCAT_WS(' ',a.p_street_type,a.p_street)"}, # Улица =рег
'ДомРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="text"][@name="building"]', 'SQL': "a.p_building"}, # Дом =рег
'КорпусРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="text"][@name="corpus"]' , 'SQL': "a.p_corpus"}, # Корпус =рег
'СтроениеРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="text"][@name="stroenie"]' , 'SQL': ""}, # Строение =рег
'КвартираРЕГ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][1]//INPUT[@type="text"][@name="flat"]' , 'SQL': "a.p_flat"}, # Квартира =рег
'iIndFACT' : {'t': 'x', 's': '//[@class="addresstype_home_postal_code"]' , 'SQL': "a.d_postalcode"}, # Индекс =прож
'iRegFACT' : {'t': 'x', 's': '//[@class="addresstype_home_place"]' , 'SQL': "a.d_region"}, # Регион =прож
'iPlaceFACT' : {'t': 'x', 's': '//[@class="addresstype_home_area"]' , 'SQL': "CONCAT_WS(' ',a.d_district,a.d_district_type,"
                                                      "a.d_place,a.d_place_type)"}, # Район или город =прож
'iSPlaceFACT' : {'t': 'x', 's': '//[@class="addresstype_home_city"]' , 'SQL': "IF(a.d_subplace IS NULL OR CHAR_LENGTH(TRIM(a.d_subplace))=0,"
                                                     "CONCAT_WS(' ',a.d_district,a.d_district_type,"
                                                      "a.d_place,a.d_place_type),"
                                                      "CONCAT_WS(' ',a.d_subplace,a.d_subplace_type))"}, # Населенный пункт =прож
'iStreetFACT' : {'t': 'x', 's': '//[@class="addresstype_home_street"]' , 'SQL': "CONCAT_WS(' ',a.d_street,a.d_street_type)"}, # Улица =прож
'iHomeFACT' : {'t': 'x', 's': '//[@class="addresstype_home_building"]' , 'SQL': "a.d_building"}, # Дом =прож
'iCorpFACT' : {'t': 'x', 's': '//[@class="addresstype_home_corpus"]' , 'SQL': "a.d_corpus"}, # Корпус =прож
'iStrFACT' : {'t': 'x', 's': '//[@class="addresstype_home_stroenie"]' , 'SQL': ""}, # Строение =прож
'iFlatFACT' : {'t': 'x', 's': '//[@class="addresstype_home_flat"]' , 'SQL': "a.d_flat"}, # Квартира =прож
'iStPhone' : {'t': 'x', 's': '//[@class="phone_home"]' , 'SQL': "b.landline_phone-70000000000"}, # Стационарный телефон по месту проживания или регистрации
'iStDopPhone' : {'t': 'x', 's': '//[@class="additional_phone_home"]' , 'SQL': "IF(b.landline_phone>70000000000 AND b.landline_phone IS NOT NULL,"
                                                      "NULL,IF(b.landline_phone_relatives>70000000000 AND "
                                                      "b.landline_phone_relatives IS NOT NULL,"
                                                      "b.landline_phone_relatives-70000000000,NULL))"}, # Дополнительный стационарный телефон
# 'i' : {'t': 'x', 's': '//[@class="additional_phone_home_comment"]' , 'SQL': '"родственники"' # Всегда родственники
'НазвФирмы' : {'t': 'x', 's': '//TEXTAREA[@name="work_name"]' , 'SQL': "b.employment_organization"}, # Наименование организации
'НазвДолжности' : {'t': 'x', 's': '//INPUT[@name="work_position_text"]' , 'SQL': ""}, # Название должности !!!!!ПОКА НЕТ!!!!
'ТелефонРАБ' : {'t': 'x', 's': '//INPUT[@name="phone_work"]' , 'SQL': "b.employment_phone-70000000000"}, # Рабочий телефон
'ИндексРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="tel"][@name="postal_code"]', 'SQL': "b.w_postalcode"}, # Индекс =раб
'РегионРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="suggest"][@name="place"]' , 'SQL': "b.w_region"}, # Регион =раб
'Район+ГородРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="suggest"][@name="area"]' ,
                    'SQL': "CONCAT_WS(' ',b.w_district_type,b.w_district,b.w_place_type,b.w_place)"}, # Район или город =раб
'НасПунктРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="suggest"][@name="city"]' ,
                 'SQL': "CONCAT_WS(' ',b.w_subplace_type,b.w_subplace)"}, # Населенный пункт =раб
'УлицаРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="suggest"][@name="street"]' ,
              'SQL': "CONCAT_WS(' ',b.w_street_type,b.w_street)"}, # Улица =раб
'ДомРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="text"][@name="building"]' , 'SQL': "b.w_building"}, # Дом =раб
'КорпусРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="text"][@name="corpus"]' , 'SQL': "b.w_corpus"}, # Корпус =раб
'СтроениеРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="text"][@name="stroenie"]' , 'SQL': ""}, # Строение =раб
'НомОфисаРАБ' : {'t': 'x', 's': '//DIV[@class="ui-kladr"][3]//INPUT[@type="text"][@name="flat"]' , 'SQL': "b.w_flat"}, # Номер офиса =раб
'НеРаботаю-Другое' : {'t': 'x', 's': '//INPUT[@name="notwork_other_text"]' , 'SQL': "b.unemployment_other"}, # Не работаю - другое
'iExpences' : {'t': 'x', 's': '//[@class="income_individual"]' , 'SQL': "b.personal_income"}, # Персональный доход
'iFlatPayment' : {'t': 'x', 's': '//[@class="expenses_amount"]' , 'SQL': "b.flat_payment"}, # Сумма аренды квартиры
'iBanksPayment' : {'t': 'x', 's': '//[@class="liability_n_w_amount"]' , 'SQL': "b.banks_payment"}, # Сумма платежей по тек.кредитам в др.банках
'КредЛимит' : {'t': 'x', 's': '//INPUT[@type="tel"][@name="desired_credit_limit"]', 'SQL': "b.want_amount"}, # Кредитный лимит
}

selectity = {
'ТипЗанятости' : {'t': 'x', 's': '//SELECT[@name="employment_type"]/..', 'SQL': "employment_status_code"},
'ТипНезанятости' : {'t': 'x', 's': "not_work"                                   , 'SQL': "unemployment_code"}, # Если не работаю то Кем ПРОВЕРИТЬ ИЗМЕНЕНИЯ !!!!!
'Должность' : {'t': 'x', 's': '//SPAN[text()="Тип должности"]', 'SQL': "employment_position_code"}, # Если работаю то Должность
'Стаж' : {'t': 'x', 's': '//SPAN[text()="Стаж работы"]' , 'SQL': "b.employment_experience_months"}, # Стаж работы (мес)
'СкДетей' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[3]'    , 'SQL': "status_childs_code"}, # Количество детей
'СемейноеПоложение' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[4]'    , 'SQL': "status_marital_code"}, # Семейное положение
'Образование' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[5]'    , 'SQL': "status_education_code"}, # Образование
'Автомобиль' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[6]'    , 'SQL': "status_car_code"}, # Автомобиль
'КркдитнаяИстория' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[7]'    , 'SQL': "status_credit_history_code"}, # Какая кредитная история
'ПросрочкиПоКредитам' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[8]'    , 'SQL': "status_credit_delay_code"}, # Просрочки по текущим кредитам
'ПрВодительскоеУд' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[9]'    , 'SQL': "driver_card_attachment_id"}, # Предоставит вод.удостоверение
'ПрЗагранпаспорт' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[10]'   , 'SQL': "international_passport_attachment_id"}, # Предоставит Загранпаспорт
'ПрПенсионноеУд' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[11]'   , 'SQL': "pensioner_card_attachment_id"}, # Предоставит Пенс.удостоверение
'ПрУдОфицера' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[12]'   , 'SQL': "identity_card_mvd_attachment_id"}, # Предоставит Удост.офицера МВД
'ПрВоенныйБилет' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[13]'   , 'SQL': "military_card_attachment_id"}, # Предоставит Военный билет
'ПрСвРегТС' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[14]'   , 'SQL': "auto_reg_attachment_id"}, # Cвидетельство регистрации ТС
'ПрОригПТС' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[15]'   , 'SQL': "auto_pts_attachment_id"}, # Оригинал ПТС
'ПрПолисКАСКО' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[16]'   , 'SQL': "auto_kasko_attachment_id"}, # Полис страхования КАСКО
'ПрПолисОСАГО' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[17]'   , 'SQL': "auto_osago_attachment_id"}, # Полис ОСАГО
'ПрСНИЛС' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[18]'   , 'SQL': "number_attachment_id"}, # Предоставит СНИЛС
'ПрИНН' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[19]'   , 'SQL': "inn_attachment_id"}, # Предоставит ИНН
'Пр2НДФЛ' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[20]'   , 'SQL': "has_2NDFL"}, # Предоставит 2 НДФЛ
'ПрСправкуОДоходах' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[21]'   , 'SQL': "has_income_report"}, # Предоставит Справку о доходах
}

select_selectity = {
'ТипЗанятости' : [{'t': 'x', 's': '//UL[@class="ui-select__slider ui-select__slider_open"]'
                                  '//SPAN[text()="Работаю в организации"]', 'txt': 'Работаю в организации'},
                  {'t': 'x', 's': '//UL[@class="ui-select__slider ui-select__slider_open"]'
                                  '//SPAN[text()="Собственный бизнес"]', 'txt': 'Собственный бизнес'},
                  {'t': 'x', 's': '//UL[@class="ui-select__slider ui-select__slider_open"]'
                                  '//SPAN[text()="Не работаю"]', 'txt': 'Не работаю'}],
'ТипНезанятости' : [{'t': 'x', 's': '//DIV[text()="По возрасту/стажу работы"]', 'txt': 'По возрасту/стажу работы'}, # Если не работаю то почему
                    {'t': 'x', 's': '//DIV[text()="По инвалидности"]', 'txt': 'По инвалидности'},
                    {'t': 'x', 's': '//DIV[text()="Ищу работу"]', 'txt': 'Ищу работу'},
                    {'t': 'x', 's': '//DIV[text()="Содержит муж/жена"]', 'txt': 'Содержит муж/жена'},
                    {'t': 'x', 's': '//DIV[text()="Другое"]', 'txt': 'Другое'}],
'Должность' : [{'t': 'x', 's': '//SPAN[text()="Рабочий"]', 'txt': 'Рабочий'},  # Если работаю то Должность. Не заполнил - рабочий
               {'t': 'x', 's': '//SPAN[text()="Генеральный директор"]', 'txt': 'Генеральный директор'},
               {'t': 'x', 's': '//SPAN[text()="Руководитель"]', 'txt': 'Руководитель'},
               {'t': 'x', 's': '//SPAN[text()="Специалист"]', 'txt': 'Специалист'},
               {'t': 'x', 's': '//SPAN[text()="Рабочий"]', 'txt': 'Рабочий'},
               {'t': 'x', 's': '//SPAN[text()="Обсл. персонал"]', 'txt': 'Обсл. персонал'}],
'Стаж' : [{'t': 'x', 's': '//SPAN[text()="6 месяцев и меньше"]' , 'txt': '6 месяцев и меньше'}, # Стаж работы (мес)
          {'t': 'x', 's': '//SPAN[text()="0,5-3 года"]', 'txt': '0,5-3 года'},
          {'t': 'x', 's': '//SPAN[text()="3-5 лет"]', 'txt': '3-5 лет'},
          {'t': 'x', 's': '//SPAN[text()="5-7 лет"]', 'txt': '5-7 лет'},
          {'t': 'x', 's': '//SPAN[text()="7 и более лет"]', 'txt': '7 и более лет'},],
'СкДетей' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[3]'    , 'SQL': "status_childs_code"}, # Количество детей
'СемейноеПоложение' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[4]'    , 'SQL': "status_marital_code"}, # Семейное положение
'Образование' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[5]'    , 'SQL': "status_education_code"}, # Образование
'Автомобиль' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[6]'    , 'SQL': "status_car_code"}, # Автомобиль
'КркдитнаяИстория' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[7]'    , 'SQL': "status_credit_history_code"}, # Какая кредитная история
'ПросрочкиПоКредитам' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[8]'    , 'SQL': "status_credit_delay_code"}, # Просрочки по текущим кредитам
'ПрВодительскоеУд' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[9]'    , 'SQL': "driver_card_attachment_id"}, # Предоставит вод.удостоверение
'ПрЗагранпаспорт' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[10]'   , 'SQL': "international_passport_attachment_id"}, # Предоставит Загранпаспорт
'ПрПенсионноеУд' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[11]'   , 'SQL': "pensioner_card_attachment_id"}, # Предоставит Пенс.удостоверение
'ПрУдОфицера' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[12]'   , 'SQL': "identity_card_mvd_attachment_id"}, # Предоставит Удост.офицера МВД
'ПрВоенныйБилет' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[13]'   , 'SQL': "military_card_attachment_id"}, # Предоставит Военный билет
'ПрСвРегТС' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[14]'   , 'SQL': "auto_reg_attachment_id"}, # Cвидетельство регистрации ТС
'ПрОригПТС' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[15]'   , 'SQL': "auto_pts_attachment_id"}, # Оригинал ПТС
'ПрПолисКАСКО' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[16]'   , 'SQL': "auto_kasko_attachment_id"}, # Полис страхования КАСКО
'ПрПолисОСАГО' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[17]'   , 'SQL': "auto_osago_attachment_id"}, # Полис ОСАГО
'ПрСНИЛС' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[18]'   , 'SQL': "number_attachment_id"}, # Предоставит СНИЛС
'ПрИНН' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[19]'   , 'SQL': "inn_attachment_id"}, # Предоставит ИНН
'Пр2НДФЛ' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[20]'   , 'SQL': "has_2NDFL"}, # Предоставит 2 НДФЛ
'ПрСправкуОДоходах' : {'t': 'x', 's': '//[@class="tcs-plugin-select2"])[21]'   , 'SQL': "has_income_report"}, # Предоставит Справку о доходах
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


gluk_w_point = ["surname", "name", "patronymic", "passport_who_given", "place_of_birth",
                "addresstype_registered_place", "addresstype_registered_area", "addresstype_registered_city",
                "addresstype_registered_street",
                "addresstype_home_place", "addresstype_home_area", "addresstype_home_city","addresstype_home_street",
                "addresstype_work_place", "addresstype_work_area", "addresstype_work_city", "addresstype_work_street"
                ]

