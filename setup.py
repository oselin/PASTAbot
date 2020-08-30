import xml.etree.ElementTree as ET
import time
from pprint import pprint


"""

STRUCT DATA

DATA = {
    'admin'    : string
    'token'    : string
    'user'     : string
    'password' : string
    'groups'   : list of class Group
}
"""

class Group:
    var = {}
    id = ""
    users = []

def getData(DATAFILE):

    data = {'groups' : []}
    g = Group
    root = ET.parse(DATAFILE).getroot()
    for child in root:
        if child.tag == 'admin':
            data[child.tag] = int(child.attrib['value'])

        elif child.tag == 'token':
            data[child.tag] = child.attrib['value']

        elif child.tag == 'user':
            data[child.tag] = child.attrib['value']

        elif child.tag == 'pw':
            data[child.tag] = child.attrib['value']

        elif child.tag == 'group':
            g.id = int(child.attrib['value'])
            for m in child:
                if m.tag == 'userid':
                    g.users.append(int(m.attrib['value']))
                else:
                    g.var[m.tag] = int(m.attrib['value'])
        
            data['groups'].append(g)
    return data

def saveData(PATHFILE,data):

    tree = ET.ElementTree()    

    tags = ['admin','token','user','pw']
    root = ET.Element('data')
    for x in range(len(tags)):
        el = ET.Element(str(tags[x]))
        el.attrib['value'] = str(data[tags[x]])
        root.append(el)
    for g in data['groups']:
        master = ET.Element('group')
        master.attrib['value'] = str(g.id)

        for key,value in g.var.items():
            val = ET.Element(str(key))
            val.attrib['value'] = str(value)
            master.append(val)

        for usr in g.users:
            user = ET.Element('userid')
            user.attrib['value'] = str(usr)
            master.append(user)
        
        root.append(master)
    tree._setroot(root)
    tree.write(PATHFILE)

def logmanager(PATH, content):
    date = str(time.localtime().tm_year)
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    if month < 10: date += '0' + str(month)
    else: date += str(month)

    if day < 10: date += '0' + str(day)
    else: date += str(day)

    f = open(PATH + '/' + date,'a')

    f.write(content+'\n')
    f.close()