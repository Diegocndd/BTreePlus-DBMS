"""
As funções de parse leem o conteúdo das páginas e retornam dicionários com as informações
para serem tratadas pelo programa.
"""

from random import random
import math
import os
from utils import getRangeOfKey
from editIndex import editIndex
from editLeaf import editLeaf

ORDER = 4
ERROR_ROOT = 'root node does not exist'

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
        if typeData == 'back':
            dataList.append({'back': valueData})
    
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

def createLeaf(titleNode, data, parent='null', next='null', back='null'):
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
    newContent += "parent: " + str(parent) + "\n"
    newContent += "back: " + str(back)

    f.write(newContent)
    f.close()

def orderDataNode(data):
    return sorted(data, key=lambda d: int(d['key'])) 

def addInLeaf(titleNode, data):
    # data é um array de dicionários
    f = open("paginas/folhas/" + titleNode + ".txt", "r")
    oldContent = f.readlines()
    backLine = oldContent[-1]
    parentLine = oldContent[-2]
    nextLine = oldContent[-3]
    oldContent.pop()
    oldContent.pop()
    oldContent.pop()
    oldContent = ''.join(oldContent)

    arrayToSort = parseLeaf(titleNode)[:-3]
    for element in data:
        arrayToSort.append(element)

    f.close()

    f = open("paginas/folhas/" + titleNode + ".txt", "w+", encoding="utf-8")
    newContent = ''

    for element in orderDataNode(arrayToSort):
        key = element['key']
        id_element = element['id']
        tipo = element['tipo']
        rotulo = element['rotulo']

        newContent += "key: {}\nid: {} \nrotulo: {}\ntipo: {}\n\n".format(str(key), str(id_element), rotulo, tipo)
    
    f.write(newContent + nextLine + parentLine + backLine)
    f.close()    

def addInIndex(titleNode, data):
    f = open("paginas/indices/" + titleNode + ".txt", "r")
    oldContent = f.readlines()
    oldContent = ''.join(oldContent)

    arrayToSort = parseIndex(titleNode)
    for element in data:
        arrayToSort.append(element)

    f.close()

    f = open("paginas/indices/" + titleNode + ".txt", "w+", encoding="utf-8")
    newContent = ''

    for element in orderDataNode(arrayToSort):
        key = element['key']
        left = element['left']
        right = element['right']

        newContent += "key: {}\nleft: {} \nright: {}\n\n".format(str(key), left, right)
    
    f.write(newContent)
    f.close()   

def deleteFileLeaf(titleNode):
    os.remove("paginas/folhas/" + titleNode + ".txt")

def splitLeaf(titleNode):
    leafContent = parseLeaf(titleNode)

    # se o pai for null, não existe root. então, deve ser criado
    if leafContent[-2]['parent'] == 'null':
        dataLeaf = leafContent[:-3]
        mid = math.floor(len(dataLeaf) / 2)

        leftContent = dataLeaf[:mid]
        rightContent = dataLeaf[mid:]

        rootKey = rightContent[0]['key']
        rootIndexName = 'node_root'

        leftLeafName = 'leaf_' + str(generateNumberNode())
        rightLeafName = 'leaf_' + str(generateNumberNode())

        # cria o root e faz o split na folha
        createLeaf(leftLeafName, leftContent, parent=rootIndexName, next=rightLeafName, back='null')
        createLeaf(rightLeafName, rightContent, parent=rootIndexName, back=leftLeafName)
        createIndex(rootIndexName, [{
            'key': rootKey,
            'left': leftLeafName,
            'right': rightLeafName,
        }])

        deleteFileLeaf(titleNode)
    else:
        # se já existir root, fazer o split do nó e subir mais uma key para o root
        """
        TODO: Essa função só funciona se o root não estiver cheio.
        """
        dataLeaf = leafContent[:-3]
        mid = math.floor(len(dataLeaf) / 2)

        leftContent = dataLeaf[:mid]
        rightContent = dataLeaf[mid:]

        leftLeafName = 'leaf_' + str(generateNumberNode())
        rightLeafName = 'leaf_' + str(generateNumberNode())

        parentName = leafContent[-2]['parent']
        backName = leafContent[-1]['back']

        createLeaf(leftLeafName, leftContent, parent=parentName, next=rightLeafName, back=backName)
        createLeaf(rightLeafName, rightContent, parent=parentName, next=leafContent[-3]['next'], back=leftLeafName)
        editLeaf(backName, newNext=leftLeafName)

        # dataLeaf = leafContent[:-2]
        # mid = math.floor(len(dataLeaf) / 2)

        # leftContent = dataLeaf[:mid]
        # rightContent = dataLeaf[mid:]

        # parentName = leafContent[-1]['parent']
        # parentNode = parseIndex(leafContent[-1]['parent'])

        # leftLeafName = 'leaf_' + str(generateNumberNode())
        # rightLeafName = 'leaf_' + str(generateNumberNode())

        # createLeaf(leftLeafName, leftContent, parent=parentName, next=rightLeafName)
        # createLeaf(rightLeafName, rightContent, parent=parentName, next=leafContent[-2]['next'])
        # editIndex(parentName, parentNode[0]['key'], newRight=leftLeafName)
        # addInIndex(parentName, [{
        #     'key': rightContent[0]['key'],
        #     'left': 'null',
        #     'right': rightLeafName, 
        # }])
        # # editLeaf(parentNode[0]['left'], newNext=leftLeafName)

def insertData(data):
    root = parseIndex('node_root')

    if root == ERROR_ROOT:
        # verifica se já existe algum nó-folha sendo construído
        contentLeaf = os.listdir(path='./paginas/folhas')
        if len(contentLeaf) == 0:
            # se não existir, cria a primeira folha
            createLeaf('leaf_' + str(generateNumberNode()), [data])
        else:
            # se existir, adiciona na folha já existente
            titleFile = contentLeaf[0].split('.')[0]
            leafContent = parseLeaf(titleFile)
            addInLeaf(titleFile, [data])

            # -3 porque desconsideramos as linhas do parent, do next e do back
            if (len(leafContent) - 3 == ORDER - 1): # se a folha estiver cheia, fazer o split e criar o root
                splitLeaf(titleFile)
    else:
        # se o root existe, vamos percorrer a árvore para descobrir onde colocar o novo dado
        actualNode = parseIndex('node_root')
        referenceNode, position = getRangeOfKey(data['key'], actualNode)

        page = actualNode[referenceNode][position]

        while(page.split('_')[0] != 'leaf'):
            referenceNode, position = getRangeOfKey(data['key'], page)
            page = actualNode[referenceNode][position]

        addInLeaf(page, [data])
        leafContent = parseLeaf(page)

        if (len(leafContent) - 3 == ORDER):
            splitLeaf(page)

# insertData({"key": "5000", "tipo": "lalal", "rotulo": "opopopo", "id": "19"})
# insertData({"key": '1956', "tipo": "rose", "rotulo": "bla_bla", "id": '9'})
# insertData({"key": '1888', "tipo": "cabernet", "rotulo": "xxxxxx", "id": '155'})
# insertData({"key": "1777", "tipo": "ssss", "rotulo": "bla_bla", "id": "30"})
# insertData({"key": "1", "tipo": "hhhhh", "rotulo": "xyxyxyxy", "id": "344"})

insertData({"key": "3", "tipo": "lalal", "rotulo": "opopopo", "id": "19"})
insertData({"key": '3', "tipo": "rose", "rotulo": "bla_bla", "id": '9'})
insertData({"key": '3', "tipo": "cabernet", "rotulo": "xxxxxx", "id": '155'})
insertData({"key": "3", "tipo": "ssss", "rotulo": "bla_bla", "id": "30"})
# insertData({"key": "9", "tipo": "hhhhh", "rotulo": "xyxyxyxy", "id": "344"})
# insertData({"key": "8", "tipo": "hhhhh", "rotulo": "xyxyxyxy", "id": "344"})
