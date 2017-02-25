#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import requests
import psycopg2
import sys
import getopt
import time
import logging as log
import subprocess
# import os
import tempfile


# Словарь с инфой по хранению путей до сертификатов и хранилищ ключей клиента, имя ключа передается через командную строку
CERT_STORAGE = {'Test': ['\\\.HDIMAGE\\test1', '/var/opt/cprocsp/clients/Test/base64.cer', '/tmp/test-session.tmp'],
                'new client': ['имя_хранилища_cryptopro', 'файл_сертификата', 'временный_маркер']}

# Logging section
logger = log.getLogger('ofd_checker')
logger.setLevel(log.DEBUG)
formatter=log.Formatter("%(asctime)s [%(levelname)s] -- %(name)s -- %(message)s")
ch = log.StreamHandler()
#ch.setLevel(log.ERROR)
ch.setFormatter(formatter)
logger.addHandler(ch)

# Параметры подключения к БД Set, переопределяются через командную строку
db_engine = 'psql'
server_ip = '172.16.2.76'
dbname = 'set'
dbuser = 'admin'
dbpass = 'qazxsw'
#dbpass = 'PA$$word123'
client = 'Test'
psql_options = {'connect_timeout': 3}
method = 'GetShiftStatus'

# Параметры командной строки
try:
    opts, args = getopt.getopt(sys.argv[1:], "hvs:d:u:p:c:e:m:")
except getopt.GetoptError as e:
    sys.exit(e)
for opt, arg in opts:
    if opt == "-h":
        print("Usage: " + sys.argv[0] + " -s <server_ip> -d <dbname> -u <username> -p <dbpass> -c <client> -e <psql|mssql> -m <request_method>")
        print("Show version: %s -v" % sys.argv[0])
        sys.exit()
    elif opt == "-v":
        print("%s v0.1 (by Sergey Lisikh (s.lisikh@crystals.ru) (C) CSI)" % sys.argv[0])
        sys.exit()
    elif opt == "-s":
        server_ip = arg.strip()
    elif opt == "-d":
        dbname = arg.strip()
    elif opt == "-u":
        dbuser = arg.strip()
    elif opt == "-p":
        dbpass = arg.strip()
    elif opt == "-c":
        client = arg.strip()
    elif opt == "-e":
        db_engine = arg.strip()
    elif opt == "-m":
        method = arg.strip()

cp_storage = CERT_STORAGE[client][0]
client_cert = CERT_STORAGE[client][1]
decrypted_marker = CERT_STORAGE[client][2]

status = 'OK: Расхождений не найдено'
ofd_data = []
send_data = []
check_data = []
output_data = []
output_schema = ['     ФН SET; СМЕНА SET; СТАТУС СМЕНЫ ОФД; '
                 'ВЫРУЧКА SET;   НАЛ SET; БЕЗНАЛ SET; ВОЗВРАТЫ SET; ВОЗВРАТЫ НАЛ SET; ВОЗВРАТЫ БЕЗНАЛ SET; '
                 'ВЫРУЧКА ОФД; НАЛ ОФД; БЕЗНАЛ ОФД; ВОЗВРАТЫ ОФД; ВОЗВРАТЫ НАЛ ОФД; ВОЗВРАТЫ БЕЗНАЛ ОФД'
               ]
# ok_scheme = '; '.join([str(0) for i in range(15)])

API = "http://api-tlk-ofd.taxcom.ru/API/"

try:
    with open(decrypted_marker, 'r') as token:
        session_token = token.read()
except:
    session_token = ''

HEADERS = {'Content-Type': 'application/json',
           'Session-Token': session_token
           }

def get_marker():
    '''
    Делает запрос в ОФД на получение временного маркера, дешифрует с помощью утилит КриптоПро, записывает результат во временный файл
    :return: Null
    '''
    global session_token

    with open(client_cert, 'rb') as fd:
        data = fd.read()

    try:
        r = requests.post(API + 'CertificateLogin', data=data)
    except Exception as E:
        sys.exit('ERROR %s' % E)

    if r.status_code == 200:
        logger.debug('Получен временный маркер')
        #encrypted_marker = '/tmp/' + client + '.tmp'
        with tempfile.NamedTemporaryFile() as tmpfile:
            tmpfile.write(r.content)
            tmpfile.seek(0)
            try:
                subprocess.check_output(['/opt/cprocsp/bin/amd64/cryptcp', '-nochain', '-decr', tmpfile.name, decrypted_marker], stderr=subprocess.STDOUT)
            except Exception as E:
                sys.exit('ERROR: Не удалось расшифровать временный маркер, %s' % E)
            logger.debug('Временный маркер успешно расшифрован')
    else:
        exit_error(r.json())

    with open(decrypted_marker, 'r') as fd:
        marker = fd.read()
    return marker


# TODO: MSSQL connect
def mssql():
    pass


# PostgreSQL connect
def psql_get():
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpass, host=server_ip, port="5432", **psql_options)
        cur = conn.cursor()
        cur.execute('''
            select
                ch.eklznum as "fn",
                shiftnumber as "shift",
                amountbypurchasefiscal as "incomeTotal",
                amountbycashpurchase as "incomeCash",
                amountbycashlesspurchase as "incomeCard",
                amountbyreturnfiscal as "outcomeTotal",
                amountbycashreturn as "outcomeCash",
                amountbycashlessreturn as "outcomeCard",
                countpurchase + countreturn as "receipts",
                --(amountcashin+amountcashout)/(countpurchase + countreturn) as "avgIncome",
                dateshiftopen as "open",
                dateshiftclose as "close",
                zrusername as "cassier",
                case when (extract(epoch from dateshiftclose) - extract(epoch from dateshiftopen))/3600::float>24 then 2 else 0 end as "state"
            from
                erpi_zreport as ez
            inner join cash_cash as  ch
             on ch.factorynum = ez.factory_cash_number
             and ch.status = 'ACTIVE'
            where
                dateoperday = '20161214' --now()::date - '11 day'::interval
            and
                shift_state > 0
            and
                length(trim(ez.factory_cash_number)) = 10
            ''')

        # Формируем словари для отправки запроса и дальнейшей проверки ответа
        # send_data - словарь со сменой и номером ФН для отправки запроса в ОФД
        # check_data - словарь по БД Set со всеми проверяемыми полями
        for row in cur:
            send_data.append({'fn': row[0].strip(), 'shift': row[1]})
            check_data.append({'fn': row[0].strip(),
                               'shift': row[1],
                               'incomeTotal': row[2],
                               'incomeCash': row[3],
                               'incomeCard': row[4],
                               'outcomeTotal': row[5],
                               'outcomeCash': row[6],
                               'outcomeCard': row[7]
                               })
        conn.close()
    except psycopg2.DatabaseError as E:
        sys.exit('ERROR: ' + str(E))


def exit_error(response):
    api_details = response['Details']
    api_error = response['ApiErrorCode']
    api_error_comment = response['CommonDescription']
    sys.exit('ERROR: Код %s, %s: %s' % (api_error, api_error_comment, api_details))


def main_check(response):
    '''
    Сверяет данные из ОФД с данными БД Set, формирует список с расхождениями
    '''
    global status, ofd_data, check_data
    ofd_data = response['stats']
    for shift in check_data:
        for ofd_shift in ofd_data:
            if shift['fn'] == ofd_shift['fn'] and shift['shift'] == ofd_shift['shift']:
                if ofd_shift['statusCode'] == 1:
                    status = 'PROBLEM: Найдены незакрытые смены в ОФД'
                    logger.debug('ФН: %s, смена %s не закрыта' % (shift['fn'], shift['shift']))
                    output_data.append(('%s; %s; %d') % (shift['fn'], shift['shift'], ofd_shift['statusCode']))
                    break
                elif ofd_shift['statusCode'] == 2:
                    status = 'PROBLEM: Смены не найдены в ОФД'
                    logger.debug('ФН: %s, смена %s не найдена' % (shift['fn'], shift['shift']))
                    output_data.append(('%s; %s; %d') % (shift['fn'], shift['shift'], ofd_shift['statusCode']))
                    break
                else:
                    for key in shift:
                        if ofd_shift[key] != shift[key]:
                            status = 'PROBLEM: расхождения по суммам'
                            logger.debug('Расхождение по %s, в БД SET: смена %s - %s, в ОФД: смена %s - %s' % (key, shift['shift'], shift[key], ofd_shift['shift'],ofd_shift[key]))
                            output_data.append('{}; {:>9}; {:>16}; {:>11}; {:>9}; {:>10}; {:>12}; {:>16}; {:>19}; {:>11}; {:>7}; {:>10}; {:>12}; {:>16}; {:>19}'.format(
                                shift['fn'], shift['shift'], ofd_shift['statusCode'],
                                shift['incomeTotal'], shift['incomeCash'], shift['incomeCard'],
                                shift['outcomeTotal'], shift['outcomeCash'], shift['outcomeCard'],
                                ofd_shift['incomeTotal'], ofd_shift['incomeCash'], ofd_shift['incomeCard'],
                                ofd_shift['outcomeTotal'], ofd_shift['outcomeCash'], ofd_shift['outcomeCard'])
                            )
                            break
                    break
if method == 'CertificateLogin':
    sys.exit(get_marker())

if db_engine == 'psql':
    psql_get()
elif db_engine == 'mssql':
    mssql()

logger.debug(json.dumps(send_data, indent=4, sort_keys=True, ensure_ascii=False))
if not send_data:
    sys.exit('PROBLEM: Не найдены закрытые смены в БД SET')

# print(json.dumps(check_data, indent=4, sort_keys=True))

# Запрос сверки в ОФД
r = requests.post(API + method, data=json.dumps(send_data), headers=HEADERS)
if r.status_code == 200:
    main_check(r.json())
else:
    logger.debug((r.json()['ApiErrorCode'], r.json()['CommonDescription'], r.json()['Details']))
    if r.json()['ApiErrorCode'] == 2111:
        HEADERS['Session-Token'] = get_marker()
    else:
        sys.exit('ERROR: Код %s, %s, %s' %(r.json()['ApiErrorCode'], r.json()['CommonDescription'], r.json()['Details']))

    r = requests.post(API + method, data=json.dumps(send_data), headers=HEADERS)
    if r.status_code == 200:
        main_check(r.json())
    else:
        sys.exit('ERROR: Код %s, %s: %s' % (r.json()['ApiErrorCode'], r.json()['CommonDescription'], r.json()['Details']))

output_data.insert(0, status)

if not status.startswith('OK'):
    output_data.insert(1, output_schema)

#time.sleep(0.1)

for s in output_data:
    print(s)

#print(json.dumps(r.json(),indent=4,sort_keys=True, ensure_ascii=False))