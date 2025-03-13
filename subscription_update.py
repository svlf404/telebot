
import pymysql
import glob
import os
import time
import datetime
import requests
import logger as log
from config import token
localfolder = ""
log = open(localfolder + 'log/notify.log', mode ='a', encoding='utf-8')
dtn = datetime.datetime.now()
mydb = pymysql.connect(host="input_ip_mysql", user="input_login_mysql", passwd="input_pass_mysql", database="input_name_mysql", port=int(input_port_mysql), cursorclass=pymysql.cursors.DictCursor)
mydb.ping(reconnect=True)
mycursor = mydb.cursor()
print(dtn.strftime("%d-%m-%Y %H:%M"), file=log)
mycursor.execute("UPDATE autoscheduler SET datewas = datebecame, izmen = '0'")
print("1. Обновляю файлы в папках участка. Ищу файлы с изменениями...", file=log)
area = ["mvu", "ru", "du", "tu", "sku", "svu"]
messg = "⏳Файл в процессе модерации"
for x in area:
    os.chdir(localfolder + "data/uchastok/" + x + "/documents")
    rez = [os.path.normpath(i) for i in glob.glob("*/*.jpg")]
    for n, item in enumerate(rez):
        files = os.path.basename(item)
        dir = os.path.dirname(item)
        datechange = os.path.getmtime(item)
        mycursor.execute("SELECT * FROM autoscheduler WHERE filename=%s AND folder=%s", (files, dir))
        data = "error"
        for i in mycursor:
            data = i
        if data == "error":
            timestamp = datetime.datetime.fromtimestamp(datechange)
            mycursor.execute("REPLACE INTO autoscheduler(filename, folder, area, datewas, datebecame, message_text, izmen, podpiska) VALUES('" + files + "', '" + dir + "', '" + x + "', '" + str(timestamp) + "', '" + str(timestamp) + "', '" + messg + "', '0', '1')")
        else:
            mycursor.execute("SELECT * FROM autoscheduler WHERE filename=%s AND folder=%s", (files, dir))
            result = mycursor.fetchall()
            for row in result:
                find_sn = str(row["sn"])
            timestamp = datetime.datetime.fromtimestamp(datechange)
            mycursor.execute("UPDATE autoscheduler SET area = '" + x + "', folder = %s, datebecame= %s WHERE sn=%s", (dir, timestamp, find_sn))
    os.chdir("../../../../")
mydb.commit()
print("2. Выполняю сравнение столбцов и ставлю переменную izmen...", file=log)
mycursor.execute("SELECT * FROM autoscheduler WHERE datewas NOT IN (SELECT datebecame FROM autoscheduler)")
result = mycursor.fetchall()
for row in result:
    find_sn = row["sn"] 
    mycursor.execute("UPDATE autoscheduler set izmen = '1' WHERE sn=%s",(find_sn)) 
    print("Найден изменёный файл: " + str(find_sn), file=log)
mydb.commit()
print("3. Отправка сообщений...", file=log)
mycursor.execute("SELECT * FROM autoscheduler WHERE izmen='1'")
result_izmen = mycursor.fetchall()
for row in result_izmen:
    find_message_text_autoscheduler = str(row['message_text'])
    find_area_autoscheduler = str(row['area'])
    mycursor.execute("SELECT * FROM users WHERE maillist='1'") 
    result_maillist = mycursor.fetchall() 
    for row in result_maillist: 
        find_chat_id = str(row["chat_id"]) 
        find_area_user = str(row['area'])
        find_comment_user = str(row['comment'])
        if find_area_autoscheduler == find_area_user: 
            send_message = ("https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s") % (token, find_chat_id, find_message_text_autoscheduler) 
            r = requests.post(send_message)
            time.sleep(0.05)
            print("Отправлено: " + find_message_text_autoscheduler + " Для: " + find_comment_user + " " + find_chat_id, file=log)
mydb.commit()
mydb.close()
