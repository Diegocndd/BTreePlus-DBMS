def getRangeOfKey(key, data):
    keyRange = None
    searchKey = int(key)
    qty = len(data)
    for x in range(0, qty):
        if x == 0 and searchKey < int(data[x]['key']):
            keyRange = (0, 'left')
            break
        elif x == qty - 1 and searchKey >= int(data[x]['key']):
            keyRange = (x, 'right')
            break
        else:
            if searchKey >= int(data[x]['key']) and searchKey < int(data[x + 1]['key']):
                keyRange = (x, 'right')
                break
    
    return keyRange
