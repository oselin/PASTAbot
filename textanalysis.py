
def loadexamples(PATHFILE):
    data = []
    loadfile = open(PATHFILE,'r')
    for line in loadfile.read().splitlines():
        temp = []    
        for line2 in line.split(" "):
            temp.append(line2)
        data.append(temp)
    loadfile.close()
    return data

def compatibility(msg,dataset):
    confidence = []
    msg = msg.split(" ")
    l = len(msg)

    for example in dataset:
        #print('-----------------\n',example,'\n')
        ind0 = getindex(msg,example[0])
        ind = ind0
        acc = 0
        #print(example,": ",acc)
        #print('INDEX OF',example[0],ind)
        for x in example[1:]:
            #print("confrontando: ",x,msg)
            ind2 = getindex(msg,x)
            #print('INDICI',ind,ind2)
            if ind2>ind:
                acc += (ind2-ind) 
                ind = ind2
            else: 
                acc=0
        #print(float(acc)/len(msg))
        #print(example,": ",float(ind2+1-ind0)/len(example))
        # if l-acc==1: 
        #     print("VALORE AUMENTATO PER ",example)
        #     acc+=1
        #print("CONFIDENCE INTERA: ",acc, " con LUNGHEZZA TESTO: ",len(msg))
        #print("TEST VALORE: ",(float(acc)/l))
        if acc!=0:acc+=1
        confidence.append(float(acc)/len(msg))#float(ind2+1-ind0)/len(example))#float(acc/(len(x)-ind0)))
    
    #for x in range(len(confidence)): confidence[x] = float(confidence[x])/(l-ind0) 
    #print(confidence)

    con = max(confidence)
    print(con)
    
    return con

def getconfidence(test,solid):
    c = 0
    lenght = 0
    if len(test)<len(solid): lenght = len(test)
    else: lenght = len(solid)
    for i in range(lenght): 
        if test[i]==solid[i]: c+=1
    return float(c)/len(solid)

def authentication(text,DATA):
    username = ''
    password = ''
    temp=0
    for i in text:
        if i == ':': break
    username = text[:text.index(i)]
    password = text[text.index(i)+1:]

    if DATA['user'] == username and DATA['pw'] == password: return 1
    else: return 0

def getindex(arr, word):
    for x in range(len(arr)-1 ,-1,-1):
        if arr[x] == word: return x
    return 0


def savein(DATAPATH,sentence):
    global dataset
    f = open(DATAPATH,'a')
    f.write('\n' + sentence)
    f.close()



#SCOMMENTARE PER USARE SOLO L'ANALISI DEL TESTO
# test = loadexamples('dataset/LUNCH.dat')

# for i in test:print(i,'\n')
# # while 1:
#     text = input(">>> ")
#     print(compatibility(text,test))