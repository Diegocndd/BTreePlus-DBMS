"""
As funções de parse leem o conteúdo das páginas e retornam dicionários com as informações
para serem tratadas pelo programa.
"""

from random import random
import math
import os
from utils import getRangeOfKey
from editIndex import editIndex

ORDER = 3
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

def orderDataNode(data):
    return sorted(data, key=lambda d: int(d['key'])) 

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

    for element in orderDataNode(arrayToSort):
        key = element['key']
        id_element = element['id']
        tipo = element['tipo']
        rotulo = element['rotulo']

        newContent += "key: {}\nid: {} \nrotulo: {}\ntipo: {}\n\n".format(str(key), str(id_element), rotulo, tipo)
    
    f.write(newContent + nextLine + parentLine)
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
    if leafContent[-1]['parent'] == 'null':
        dataLeaf = leafContent[:-2]
        mid = math.floor(len(dataLeaf) / 2)

        leftContent = dataLeaf[:mid]
        rightContent = dataLeaf[mid:]

        rootKey = rightContent[0]['key']
        rootIndexName = 'node_root'

        leftLeafName = 'leaf_' + str(generateNumberNode())
        rightLeafName = 'leaf_' + str(generateNumberNode())

        # cria o root e faz o split na folha
        createLeaf(leftLeafName, leftContent, parent=rootIndexName, next=rightLeafName)
        createLeaf(rightLeafName, rightContent, parent=rootIndexName)
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
        dataLeaf = leafContent[:-2]
        mid = math.floor(len(dataLeaf) / 2)

        leftContent = dataLeaf[:mid]
        rightContent = dataLeaf[mid:]

        parentName = leafContent[-1]['parent']
        parentNode = parseIndex(leafContent[-1]['parent'])

        leftLeafName = 'leaf_' + str(generateNumberNode())
        rightLeafName = 'leaf_' + str(generateNumberNode())

        createLeaf(leftLeafName, leftContent, parent=parentName, next=rightLeafName)
        createLeaf(rightLeafName, rightContent, parent=parentName)
        editIndex(parentName, parentNode[0]['key'], newRight=leftLeafName)
        addInIndex(parentName, [{
            'key': rightContent[0]['key'],
            'left': 'null',
            'right': rightLeafName, 
        }])
        deleteFileLeaf(titleNode)

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

            # -2 porque desconsideramos as linhas do parent e do next
            if (len(leafContent) - 2 == ORDER - 1): # se a folha estiver cheia, fazer o split e criar o root
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

        if (len(leafContent) - 2 == ORDER):
            splitLeaf(page)

insertData({"key": '1956', "tipo": "rose", "rotulo": "bla_bla", "id": '9'})
insertData({"key": '1888', "tipo": "cabernet", "rotulo": "xxxxxx", "id": '155'})
insertData({"key": "1777", "tipo": "ssss", "rotulo": "bla_bla", "id": "30"})
insertData({"key": "9999", "tipo": "lalal", "rotulo": "opopopo", "id": "19"})
