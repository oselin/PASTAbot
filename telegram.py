import telepot, textanalysis,setup
from pprint import pprint
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os.path
from os import path

def msghandler(msg):
    global DATA, echo

    chat_type = msg['chat']['type']
    try: text = msg['text']
    except: text = ""

    user_id, group_id = 0,0

    if text:
        if chat_type == ('private'):
            user_id = msg['chat']['id']
        elif (chat_type == 'group') | (chat_type == 'supergroup'):
            group_id, user_id = msg['chat']['id'], msg['from']['id']
   
    if user_id in DATA['groups'][0].users:
        if user_id == DATA['admin']:
            if text == 'admin@help':
                BOT.sendMessage(DATA['admin'],"LIST OF COMMANDS YOU CAN EXECUTE")

            elif text == 'admin@echo':
                if echo: echo=0
                else: echo = 1
            #elif text ==
            else:
                conf = textanalysis.compatibility(text,DATASET)#: pass#print(user_id," ha cancellato")
                if conf>0.7 and conf<1:
                    textanalysis.savein('dataset/LUNCH.dat',text)
                    DATASET.append(text.split(" "))
        else:
            #UNDERSTAND THE CONTENT OF TEXT     
            conf = textanalysis.compatibility(text,DATASET)#: pass#print(user_id," ha cancellato")
            if conf>0.7 and conf<1:
                textanalysis.savein('dataset/LUNCH.dat',text)
                DATASET.append(text.split(" "))
            #BOT.sendMessage(IDs[0],"CONFIDENCE: " + str(textanalysis.compatibility(text,DATASET)))
    else:
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
    #global howmuchpasta
    query_id, from_id, query_data = telepot.glance(msg, flavor = 'callback_query')
    BOT.answerCallbackQuery(query_id,text="Ricevuto")
    #howmuchpasta.append(msg['from']['id'])

def setBot(TOKEN):
    global BOT 
    BOT = telepot.Bot(TOKEN)

def startbot():
    BOT.message_loop({'chat': msghandler,'callback_query' : on_callback_query})

def getallids(groupid):
    ids = [groupid]
     #IMPLEMENT CLASS APPROACH
    for person in BOT.getChatAdministrators(int(groupid)):
        if not person['user']['is_bot']: ids.append(person['user']['id'])
    return ids
   
def main():
    global DATA,echo,DATASET
    if not path.exists(DATAFILE):
        values = ['','','','']
        tvalues = ['ADMIN ID','TOKEN','USERNAME','PASSWORD']
        for times in range(len(values)):
            while values[times] == '':
                values[times] = input(tvalues[times]+': ')
        setup.saveData(DATAFILE,values,'w')
    
    
    
    DATA = setup.getData(DATAFILE)
    DATASET = textanalysis.loadexamples('dataset/LUNCH.dat')
    
    keyboard = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Conferma",callback_data = "pressed")],])

    setBot(DATA['token'])
    startbot()

    echo = 0
    while 1:
        time.sleep(2)
        t = time.localtime().tm_hour
        if t == 0:
            #CONTROLLARE CHE TUTTI GLI UTENTI DI UN GRUPPO SIANO SALVATI

            #SALVARE LE VARIABILI SU FILE
            pass#RESET DATA
        elif (t == 17) and not DATA['groups'][0].var['islunchasked']:
            BOT.sendMessage(DATA['groups'][0].id,"Quanti a pranzo oggi?",reply_markup = keyboard)
            DATA['groups'].var['islunchasked'] = 1


#DEFINE
DATAFILE = 'setup.xml'

if __name__ == "__main__": main()