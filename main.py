"""
TODO: INSERÇÃO DE DADOS QUANDO EXISTE NÓ ROOT
"""

from random import random
import math
import os
from utils import getRangeOfKey

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

def createLeaf(titleNode, data, parent='null', next='null'):
    # data é um array de dicionários
    f = open("paginas/folhas/" + titleNode + ".txt", "w")
    newContent = ''

    for element in data:
        key = element['key']
        id_element = element['id']
        tipo = element['tipo']
        rotulo = element['rotulo']

        newContent += "key: {}\nid: {} \nrotulo: {}\ntipo: {}\n\n".format(str(key), str(id_element), rotulo, tipo)
    
    newContent += "next: " + str(next) + "\n"
    newContent += "parent: " + str(parent)

    f.write(newContent)
    f.close()

def orderDataLeaf(data):
    return sorted(data, key=lambda d: d['key']) 

def addInLeaf(titleNode, data):
    # data é um array de dicionários
    f = open("paginas/folhas/" + titleNode + ".txt", "r")
    oldContent = f.readlines()
    parentLine = oldContent[-1]
    nextLine = oldContent[-2]
    oldContent.pop()
    oldContent.pop()
    oldContent = ''.join(oldContent)

    arrayToSort = parseLeaf(titleNode)[:-2]
    for element in data:
        arrayToSort.append(element)

    f.close()

    f = open("paginas/folhas/" + titleNode + ".txt", "w+", encoding="utf-8")
    newContent = ''

    for element in orderDataLeaf(arrayToSort):
        key = element['key']
        id_element = element['id']
        tipo = element['tipo']
        rotulo = element['rotulo']

        newContent += "key: {}\nid: {} \nrotulo: {}\ntipo: {}\n\n".format(str(key), str(id_element), rotulo, tipo)
    
    f.write(newContent + nextLine + parentLine)
    f.close()    

def deleteFileLeaf(titleNode):
    os.remove("paginas/folhas/" + titleNode + ".txt")

def splitLeaf(titleNode):
    leafContent = parseLeaf(titleNode)

    # se o pai for nulo, não existe root
    if leafContent[-1]['parent'] == 'null':
        dataLeaf = leafContent[:-2]
        mid = math.floor(len(dataLeaf) / 2)

        leftContent = dataLeaf[:mid]
        rightContent = dataLeaf[mid:]

        rootKey = rightContent[0]['key']
        rootIndexName = 'node_root'

        leftLeafName = 'leaf_' + str(generateNumberNode())
        rightLeafName = 'leaf_' + str(generateNumberNode())

        createLeaf(leftLeafName, leftContent, parent=rootIndexName, next=rightLeafName)
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
            createLeaf('leaf_' + str(generateNumberNode()), [data])
        else:
            titleFile = contentLeaf[0].split('.')[0]
            leafContent = parseLeaf(titleFile)
            addInLeaf(titleFile, [data])

            # -2 porque desconsideramos as linhas do parent e do next
            if (len(leafContent) - 2 == ORDER - 1): # split no nó e criação do root
                splitLeaf(titleFile)
    else:
        actualNode = parseIndex('node_root')
        referenceNode, position = getRangeOfKey(data['key'], actualNode)

        page = actualNode[referenceNode][position]

        while(page.split('_')[0] != 'leaf'):
            referenceNode, position = getRangeOfKey(data['key'], page)
            page = actualNode[referenceNode][position]

        addInLeaf(page, [data])
        leafContent = parseLeaf(page)
        print(leafContent)

        if (len(leafContent) - 2 == ORDER):
            print('fazer split')

insertData({"key": '1956', "tipo": "rose", "rotulo": "bla_bla", "id": '9'})
insertData({"key": '1888', "tipo": "bbb", "rotulo": "bla_bla", "id": '9'})
insertData({"key": "1777", "tipo": "bbb", "rotulo": "bla_bla", "id": "9"})
insertData({"key": "9999", "tipo": "lalal", "rotulo": "opopopo", "id": "19"})
