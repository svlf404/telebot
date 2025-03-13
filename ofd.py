
import requests
import json
import pymysql
import time
from datetime import date
from datetime import timedelta
from config import token
date_request30 = str(date.today() + timedelta(days=+30))
date_request = str(date.today() + timedelta(days=-1))               
today = date.today() 
mydb = pymysql.connect(host="input_ip_mysql", user="input_login_mysql", passwd="input_pass_mysql", database="input_name_base", port=int(input_port), cursorclass=pymysql.cursors.DictCursor)
mydb.ping(reconnect=True)
localfolder = "/home/telebot/"
log = open(localfolder + 'log/ofd.log', mode ='a', encoding='utf-8')
url_auth = "input_url"
headers_auth = {"Content-Type": "application/json; charset=utf-8",          
           "Integrator-ID": "input_integrator_id"}
data_auth = {                                                               
    "login": "input_login",
    "password": "input_pass",
    "agreementNumber": "input_dogovor",
}
response = requests.post(url_auth, headers=headers_auth, json=data_auth)    
response_json = response.json()
send = "no"
if response.status_code == 200:                                             
    sessionToken = response_json['sessionToken']
    print("-----------------------------------------------------------\n", today, file=log)
    print("🔑 Авторизация прошла успешно\n\nВыполняем запросы:", file=log)
    fn_all = []                                                             
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM ofd")
        mydb.commit()
        print("✅ БД обновлена.", file=log)
    except:
        print("❌ Ошибка при создании\очистке БД", file=log)
    try:
        i = -1
        iall = []
        pointid = []
        url_OutletList = "input_url"
        headers_token = {"Session-Token": sessionToken}
        OutletList = {
            "agreementNumber": "input_dogovor",
        }
        response_OutletList = requests.get(url_OutletList, headers=headers_token, params=OutletList)
        parsed_json = response_OutletList.json()
        while i < 10000:
            i += 1
            iall.append(i)
        for item in iall: 
            try:
                pointid_temp = parsed_json["records"][item]["id"]
                pointid.append(pointid_temp)
            except Exception as e: 
                break
        print("✅ Извлечены списки торговых точек.", file=log)
    except:
        print("❌ Ошибка при извлечении списка торговых точек", file=log)
    try:
        for item in pointid:
            pointid = item
            i = -1
            iall = []
            url_kkt = "input_url"
            headers_token = {"Session-Token": sessionToken}
            data_kkt = {
                "id": pointid,
                "agreementNumber": "input_dogovor",
            }
            response_kkt = requests.get(url_kkt, headers=headers_token, params=data_kkt)
            parsed_json = response_kkt.json()
            while i < 1000:
                i += 1
                iall.append(i)
            for item in iall:
                try:
                    if parsed_json["records"][item]["cashdeskState"] == "Inactive":
                        None
                    else:
                        url_fn = "input_url"
                        headers_token = {"Session-Token": sessionToken}
                        fn_resp = {
                            "fn": parsed_json["records"][item]["fnFactoryNumber"],
                            "agreementNumber": "input_dogovor",
                        }
                        response_fn = requests.get(url_fn, headers=headers_token, params=fn_resp)
                        parsed_json_fn = response_fn.json()
                        cursor = mydb.cursor()
                        kkt = "INSERT INTO ofd(kkt, status, problem, fn, address, fnend, datereq, place) VALUES('" + parsed_json["records"][item]["kktFactoryNumber"] + "', '" + parsed_json["records"][item]["cashdeskState"] + "', '" + parsed_json["records"][item]["problemIndicator"] + "', '" + parsed_json["records"][item]["fnFactoryNumber"] + "', '" + parsed_json["outlet"]["address"] + "', '" + parsed_json_fn['cashdesk']['fnEndDateTime'][0:10] + "', '" + date_request + "', '" + str(parsed_json["outlet"]["name"]) +"');"
                        cursor.execute(kkt)  
                        mydb.commit()
                except Exception as e:  
                    break

        print("✅ Извлечены списки ККТ.", file=log)
    except:
        print("❌ Ошибка при извлечении списка ККТ", file=log)
    try:
        url_smena = "input_url"
        headers_token = {"Session-Token": sessionToken}
        data_smena = {
            "From": date_request + "T00:00:00",
            "To": date_request + "T23:59:59",
            "agreementNumber": "input_dogovor",
        }
        response_smena = requests.post(url_smena, headers=headers_token, json=data_smena)
        parsed_json = response_smena.json()
        data_json = json.dumps(parsed_json)
        data = json.loads(data_json)
        i = -1
        iall = []
        while i < 10000:
            i += 1
            iall.append(i)
        for item in iall:
            try:
                url_fd = "input_url"
                data_fd = {
                    "fn": data['Shifts'][item]['FnFactoryNumber'],
                    "shift": str(data['Shifts'][item]['Shift']),
                }
                response_fd = requests.get(url_fd, headers=headers_token, params=data_fd)
                parsed_json_fd = response_fd.json()
                fd = parsed_json_fd['shift']['closeFdNumber']
                check_day = parsed_json_fd['shift']['income']['receiptItemCount']
                average_day = round(((250000 - fd)/check_day)) if check_day != 0 else "0"
                kkt_temp = data['Shifts'][item]['KktFactoryNumber']
                fd_temp = parsed_json_fd['shift']['closeFdNumber']
                smena_temp = str(data['Shifts'][item]['Shift'])
                place_temp = data['Shifts'][item]['OutletName']
                depart_temp = data['Shifts'][item]['DepartamentName']
                check_day_all_temp = parsed_json_fd['shift']['income']['receiptItemCount']
                cursor = mydb.cursor()
                cursor.execute("UPDATE ofd SET fd = %s, smena = %s, place = %s, depart = %s, check_day_all = %s, possibledayfdend = %s WHERE kkt=%s", (fd_temp, smena_temp, place_temp, depart_temp, check_day_all_temp, average_day, kkt_temp))
                mydb.commit()
            except Exception as e:
                break

        print("✅ Извлечены номера смен за вчера.", file=log)
    except:
        print("❌ Ошибка при извлечении смен за вчера", file=log)
    mydb.close()
    print("✅ Работа с API Taxcom завершена.", file=log)
    send = "yes"
else:
    print("\n❌ Авторизация завершилась с ошибкой: " + str(response.status_code), file=log)
if send == "yes":
    print("\n✅ Выполняется отправка отчетов ОФД.", file=log)
    mycursor = mydb.cursor()
    mydb.ping(reconnect=True)
    maillist_ofd = '1'
    mycursor.execute("SELECT * FROM users WHERE maillist_ofd=1")
    result = mycursor.fetchall()
    for row in result:
        find_chat_id = row['chat_id']
        comment = row['comment']
        print("************\n\nБудет отправленно для: " + str(find_chat_id), str(comment), file=log)
        mycursor_fd = mydb.cursor()
        mydb.ping(reconnect=True)
        mycursor_fd.execute("SELECT * FROM ofd WHERE fd > 240000")
        result_fd = mycursor_fd.fetchone()
        mydb.close()
        if result_fd is None:
            print("Нечего рассылать из ФД\n", file=log)
        else:
            mycursordate = mydb.cursor()
            mydb.ping(reconnect=True)
            mycursordate.execute("SELECT datereq FROM ofd")
            resultdate = mycursordate.fetchone()
            print("\nВыполняется отправка отчета ФД:\n", file=log)
            print('🐙 Отчет сформирован за ' + str(resultdate['datereq']) + '\nСписок ФН с количеством ФД выше 240к.', file=log)
            response_message = '🐙 Отчет сформирован за ' + str(
                resultdate['datereq']) + '\nСписок ФН с количеством ФД выше 240к.\n'
            send_message = ("input_url") % (
                token, find_chat_id, response_message)
            r = requests.post(send_message)
            mycursor_fd = mydb.cursor()
            mydb.ping(reconnect=True)
            mycursor_fd.execute("SELECT * FROM ofd WHERE fd > 240000")
            result_fd = mycursor_fd.fetchall()
            mydb.close()
            for row in result_fd:
                kkt = row['kkt']
                fn = row['fn']
                fd = row['fd']
                fnend = row['fnend']
                place = row['place']
                depart = row['depart']
                check_day_all = row['check_day_all']
                possibledayfdend = row['possibledayfdend']
                print('\n🧾ФД: ' + str(fd) + '\nЧеков за день: ' + str(check_day_all) + '\nХватит на ~' + str(
                                     possibledayfdend) + ' дней\nККТ: ' + str(kkt) + "\nФН: " + str(
                                     fn) + "\nСрок действия ФН: " + str(fnend) + "\nТорговая точка: " + str(
                                     place) + "\nПодразделение: " + str(depart), file=log)
                response_message = '🧾ФД: ' + str(fd) + '\nЧеков за день: ' + str(check_day_all) + '\nХватит на ~' + str(
                                     possibledayfdend) + ' дней\nККТ: ' + str(kkt) + "\nФН: " + str(
                                     fn) + "\nСрок действия ФН: " + str(fnend) + "\nТорговая точка: " + str(
                                     place) + "\nПодразделение: " + str(depart)
                send_message = ("input_url") % (
                    token, find_chat_id,
                    response_message)  
                r = requests.post(send_message)


        from datetime import date
        from datetime import timedelta
        date_request14 = str(date.today() + timedelta(
            days=+14))  
        date_request = str(date.today() + timedelta(days=-1))
        today = date.today()
        mycursor_fn = mydb.cursor()
        mydb.ping(reconnect=True)
        mycursor_fn.execute("SELECT datereq FROM ofd WHERE fnend BETWEEN '" + str(today) + "' AND '" + str(date_request14) + "' ORDER BY fnend DESC")

        result_fn_check = mycursor_fn.fetchone()
        mydb.close()

        if result_fn_check is None:
            print("\nНечего рассылать")
        else:
            mycursor_fn = mydb.cursor()
            mydb.ping(reconnect=True)
            mycursor_fn.execute("SELECT * FROM ofd WHERE fnend BETWEEN '" + str(today) + "' AND '" + str(
                date_request14) + "' ORDER BY fnend DESC")

            result = mycursor_fn.fetchall()
            mydb.close()
            print('\n🐙 Отчет сформирован за ' + str(result_fn_check['datereq']) + '\nСписок ФН которые заканчиваются в ближайшие 14 дней.', file=log)
            response_message = '\n🐙 Отчет сформирован за ' + str(
                result_fn_check['datereq']) + '\nСписок ФН которые заканчиваются в ближайшие 14 дней.\n'
            send_message = ("input_url") % (
                token, find_chat_id, response_message)
            r = requests.post(send_message)
            time.sleep(0.05)
            for row in result:
                kkt = row['kkt']
                fn = row['fn']
                fd = row['fd']
                fnend = row['fnend']
                place = row['place']
                depart = row['depart']
                print('\n🕑ККТ: ' + str(kkt) + '\nФН: ' + str(
                    fn) + "\nФД: " + str(fd) + "\nСрок действия ФН: " + str(fnend) + "\nТорговая точка: " + str(
                    place) + "\nПодразделение: " + str(depart), file=log)
                response_message = '🕑ККТ: ' + str(kkt) + '\nФН: ' + str(
                    fn) + "\nФД: " + str(fd) + "\nСрок действия ФН: " + str(fnend) + "\nТорговая точка: " + str(
                    place) + "\nПодразделение: " + str(depart)
                send_message = ("input_url") % (
                token, find_chat_id, response_message)
                r = requests.post(send_message)
                time.sleep(0.05)
else:
    print("Неверный логин\пароль", file=log)
