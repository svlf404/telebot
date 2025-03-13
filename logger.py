import datetime
localfolderbot = "/home/telebot/"


def writelog(user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + str(username) + " " + str(user_id) ,'написал следующее: ' + str(text), file=botlogfile)
    botlogfile.close()

def writelog_start(valid_comment, user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + valid_comment + " " + username +" " + str(user_id),'написал следующее: ' + str(text), file=botlogfile)
    botlogfile.close()

def writeloguser(in_text, user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + str(username) + " " + str(user_id) ,'написал следующее: ' + str(text) + str(in_text), file=botlogfile)
    botlogfile.close()

def writelog_send(user_id, comment, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot_send.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователю ' + str(user_id) + " " + comment,'  ' + str(text), file=botlogfile)
    botlogfile.close()

def writelog_send_header(text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot_send.log', mode='a', encoding='utf-8')
    print("\n==============================\n" + dtn.strftime("%d-%m-%Y %H:%M") + str(text), file=botlogfile)
    botlogfile.close()

def writelog_usrfind(who_find, find_comment, user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + who_find + " " + username +" " + str(user_id),'написал следующее: ' + str(text) + str(find_comment), file=botlogfile)
    botlogfile.close()

def writelog_usrfindid(find_comment, who_find, find_id, user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + who_find + " " + username +" " + str(user_id),'написал следующее: ' + str(text) + str(find_id) + ' ' + find_comment, file=botlogfile)
    botlogfile.close()

def writeloguseradd(input_comment, input_area, in_text, user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + str(username) + " " + str(user_id) ,'написал следующее: ' + str(text) + str(in_text) + ' ' + str(input_comment) + ' ' + str(input_area), file=botlogfile)
    botlogfile.close()

def writelogchuser(input_comment, input_area, user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/bot.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + str(username) + " " + str(user_id) ,'написал следующее: ' + str(text) + ' ' + str(input_comment) + ' на ' + str(input_area), file=botlogfile)
    botlogfile.close()

def writelogzayavka(user_id, username, text):
    dtn = datetime.datetime.now()
    botlogfile = open(localfolderbot + 'log/zayavka.log', mode='a', encoding='utf-8')
    print(dtn.strftime("%d-%m-%Y %H:%M"), 'Пользователь ' + str(username) + " " + str(user_id) ,'написал следующее: ' + str(text), file=botlogfile)
    botlogfile.close()

