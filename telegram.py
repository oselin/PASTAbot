import telepot, textanalysis,setup
from pprint import pprint
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os.path
from os import path

def msghandler(msg):
    global DATA, echo, msgid
    chat_type = msg['chat']['type']

    try: text = msg['text']
    except: text = ""

    user_id, group_id = 0,0

    if text:
        if chat_type == ('private'):
            user_id = msg['chat']['id']
        elif (chat_type == 'group') | (chat_type == 'supergroup'):
            group_id, user_id = msg['chat']['id'], msg['from']['id']
    
    for g in DATA['groups']:

        if user_id in g.users:
            if user_id == DATA['admin']:
                if text == 'admin@help':
                    BOT.sendMessage(DATA['admin'],"LIST OF COMMANDS YOU CAN EXECUTE")
                    return
                elif text == 'admin@echo':
                    if echo: echo=0
                    else: echo = 1
                    return
                elif text == 'button':
                    BOT.sendMessage(DATA['groups'][0].id,"Quanti a pranzo oggi?",reply_markup = keyboard)
                    return
                
            #UNDERSTAND THE CONTENT OF TEXT     
            conf = textanalysis.compatibility(text,DATASET)#: pass#print(user_id," ha cancellato")
            if conf>0.7 and conf<1:
                textanalysis.savein('dataset/LUNCH.dat',text)
                DATASET.append(text.split(" "))
        
    
    else:#AUTHENTICATION
        if text[:5] == "auth@": 
            if textanalysis.authentication(text[5:],DATA):
                #SAVEGROUP AND USER IN XML FILE
                g = setup.Group
                nid = getallids(group_id)
                g.var = {'islunchasked' : '0',
                        'mod' : '0',
                        'isreset' : '0'}
                g.id = nid[0]
                g.users = nid[1:]
                DATA['groups'].append(g)
                setup.saveData(DATAFILE,DATA,'a')

    

    if echo: BOT.sendMessage(DATA['admin'],str(user_id) + ': ' + text)

def on_callback_query(msg):
    global lunchpeople
    query_id, from_id, query_data = telepot.glance(msg, flavor = 'callback_query')
    
    BOT.answerCallbackQuery(query_id,text="Ricevuto")
    
    msgid = int(str(msg['message']['chat']['id'])+str(msg['message']['message_id']))
    sender = msg['from']['id']
    if not sender in lunchpeople: lunchpeople.append(sender)

    print(lunchpeople)
    print(msgid)


def getallids(groupid):
    ids = [groupid]

    for person in BOT.getChatAdministrators(int(groupid)):
        if not person['user']['is_bot']: ids.append(person['user']['id'])

    return ids
   
def main():
    global DATA,echo,DATASET, BOT,msgid,keyboard, lunchpeople

    if not path.exists(DATAFILE):
        values = {}
        tvalues = ['ADMIN ID','TOKEN','USERNAME','PASSWORD']
        keys = ['admin','token','user','pw']
        for times in range(len(keys)):
            values[keys[times]] = ''
            while values[keys[times]] == '':
                values[keys[times]] = input(tvalues[times]+': ')
        values['groups'] = []
        setup.saveData(DATAFILE,values,'w')
    
    
    
    DATA = setup.getData(DATAFILE)

    DATASET = textanalysis.loadexamples('dataset/LUNCH.dat')
    
    keyboard = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Conferma",callback_data = "pressed")],])

    BOT = telepot.Bot(DATA['token'])

    BOT.message_loop({'chat': msghandler,'callback_query' : on_callback_query})

    echo = 0
    setup.logmanager('log','ciao')

    lunchpeople = []
    while 1:
        time.sleep(2)
        t = time.localtime().tm_hour
        if t == 0:
            #CONTROLLARE CHE TUTTI GLI UTENTI DI UN GRUPPO SIANO SALVATI
            setup.saveData(DATAFILE,DATA,'w')
            #SALVARE LE VARIABILI SU FILE
            pass#RESET DATA
        elif (t == 17) and not DATA['groups'][0].var['islunchasked']:
            BOT.sendMessage(DATA['groups'][0].id,"Quanti a pranzo oggi?",reply_markup = keyboard)
            DATA['groups'][0].var['islunchasked'] = 1
            setup.saveData(DATAFILE,DATA,'w')




#MACROS
DATAFILE = 'setup.xml'
LOGPATH = 'log'


if __name__ == "__main__": main()