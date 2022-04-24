def editIndex(titleNode, key, newLeft=None, newRight=None):
    f = open("paginas/indices/" + titleNode + ".txt", "r")
    elements = f.read().split('\n')
    elements[:] = [x for x in elements if x]

    newContent = ''

    edit = False
    dontAdd = False

    if newLeft != None:
        for el in elements:
            dontAdd = False
            if edit:
                if el.split(':')[0] == 'left':
                    newContent += 'left: ' + newLeft + '\n'
                    dontAdd = True
                    edit = False
            if el.split(':')[0] == 'key' and el.split(':')[1].strip() == key:
                newContent += '\n'
                edit = True
                newContent += el + '\n'
                dontAdd = True
            if not dontAdd:
                newContent += el + '\n'
                dontAdd = False

    if newRight != None:
        for el in elements:
            dontAdd = False
            if edit:
                if el.split(':')[0] == 'right':
                    newContent += 'right: ' + newRight + '\n'
                    dontAdd = True
                    edit = False
            if el.split(':')[0] == 'key' and el.split(':')[1].strip() == key:
                newContent += '\n'
                edit = True
                newContent += el + '\n'
                dontAdd = True
            if not dontAdd:
                newContent += el + '\n'
                dontAdd = False

    f.close()

    f = open("paginas/indices/" + titleNode + ".txt", "w")
    f.write(newContent)
    f.close()

