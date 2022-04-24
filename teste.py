f = open("teste.txt", "r")
elements = f.read().split('\n')
elements[:] = [x for x in elements if x]

newLeft = 'bolsonaro'
newRight = None

newContent = ''

count = 0
edit = False
dontAdd = False

key = '1005'

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
                newContent += 'right: ' + newLeft + '\n'
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

print(newContent)
# print(elements)