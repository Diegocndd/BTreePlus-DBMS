from random import random
import math
import os

ORDER = 3
ERROR_ROOT = 'node does not exist'

def generateNumberNode():
    return int(random() * 10000)

def parseLeaf(titleNode):
    f = open("paginas/folhas/" + titleNode + ".txt", "r")
    elements = f.read().split('\n')
    elements[:] = [x for x in elements if x]

    dataList = []
    count = 0
    data = {}
    for element in elements:
        typeData = element.split(':')[0]
        valueData = element.split(':')[1].strip()
        if typeData != 'tipo':
            data[typeData] = valueData
        else:
            data[typeData] = valueData
            dataList.append(data)
            data = {}
            count += 1
        if typeData == 'next':
            dataList.append({'next': valueData})
        if typeData == 'parent':
            dataList.append({'parent': valueData})
    
    f.close()

    return dataList

def parseIndex(titleNode):
    f = None
    try:
        f = open("paginas/indices/" + titleNode + ".txt", "r")
    except:
        return ERROR_ROOT

    elements = f.read().split('\n')
    elements[:] = [x for x in elements if x]

    dataList = []
    count = 0
    data = {}
    for element in elements:
        typeData = element.split(':')[0]
        valueData = element.split(':')[1].strip()
        if typeData != 'right':
            data[typeData] = valueData
        else:
            data[typeData] = valueData
            dataList.append(data)
            data = {}
            count += 1
    
    f.close()

    return dataList

def createIndex(titleNode, data):
    # data é um array de dicionários
    f = open("paginas/indices/" + titleNode + ".txt", "w")
    newContent = ''

    for element in data:
        key = element['key']
        left = element['left']
        right = element['right']

        newContent += "key: {}\nleft: {} \nright: {}\n\n".format(str(key), left, right)
    
    f.write(newContent)
    f.close()

def createLeaf(titleNode, data, parent='null'):
    # data é um array de dicionários
    f = open("paginas/folhas/" + titleNode + ".txt", "w")
    newContent = ''

    for element in data:
        key = element['key']
        id_element = element['id']
        tipo = element['tipo']
        rotulo = element['rotulo']

        newContent += "key: {}\nid: {} \nrotulo: {}\ntipo: {}\n\n".format(str(key), str(id_element), rotulo, tipo)
    
    if not parent:
        newContent += "parent: null"
    else:
        newContent += "parent: " + str(parent)

    f.write(newContent)
    f.close()

def addInLeaf(titleNode, data):
    # data é um array de dicionários
    f = open("paginas/folhas/" + titleNode + ".txt", "r")
    oldContent = f.readlines()
    parentLine = oldContent[-1]
    oldContent.pop()
    oldContent = ''.join(oldContent)
    f.close()

    f = open("paginas/folhas/" + titleNode + ".txt", "w+", encoding="utf-8")
    newContent = ''

    for element in data:
        key = element['key']
        id_element = element['id']
        tipo = element['tipo']
        rotulo = element['rotulo']

        newContent += "key: {}\nid: {} \nrotulo: {}\ntipo: {}\n\n".format(str(key), str(id_element), rotulo, tipo)
    
    f.write(oldContent + newContent + parentLine)
    f.close()    

def deleteFileLeaf(titleNode):
    print('REMOVENDO ' + titleNode)
    os.remove("paginas/folhas/" + titleNode + ".txt")

def splitLeaf(titleNode):
    leafContent = parseLeaf(titleNode)

    # se o pai for nulo, não existe root
    if leafContent[-1]['parent'] == 'null':
        # TODO: -2
        dataLeaf = leafContent[:-1]
        mid = math.floor(len(dataLeaf) / 2)

        leftContent = dataLeaf[:mid]
        rightContent = dataLeaf[mid:]

        rootKey = rightContent[0]['key']
        rootIndexName = 'node_root'

        leftLeafName = 'node_' + str(generateNumberNode())
        rightLeafName = 'node_' + str(generateNumberNode())

        createLeaf(leftLeafName, leftContent, parent=rootIndexName)
        createLeaf(rightLeafName, rightContent, parent=rootIndexName)
        createIndex(rootIndexName, [{
            'key': rootKey,
            'left': leftLeafName,
            'right': rightLeafName,
        }])

        deleteFileLeaf(titleNode)
    else:
        """..."""

def insertData(data):
    root = parseIndex('node_root')

    if root == ERROR_ROOT:
        # verifica se já existe nó folha sendo construído
        contentLeaf = os.listdir(path='./paginas/folhas')
        if len(contentLeaf) == 0:
            createLeaf('node_' + str(generateNumberNode()), [data])
        else:
            titleFile = contentLeaf[0].split('.')[0]
            leafContent = parseLeaf(titleFile)
            addInLeaf(titleFile, [data])

            # -1 porque desconsideramos a linha do parent
            # TODO: -2 para descosiderar a linha do next
            if (len(leafContent) - 1 == ORDER - 1): # split no nó e criação do root
                splitLeaf(titleFile)
    else:
        """percorrer árvore para adicionar"""

insertData({"key": '1956', "tipo": "rose", "rotulo": "bla_bla", "id": '9'})
insertData({"key": '1888', "tipo": "bbb", "rotulo": "bla_bla", "id": '9'})
insertData({"key": "1777", "tipo": "bbb", "rotulo": "bla_bla", "id": "9"})
