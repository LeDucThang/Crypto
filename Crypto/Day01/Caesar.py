def encodeCaesar(msg, index):
    return "".join(chr(ord("a") + (ord(s) - ord("a") + index)%26) for s in msg[:])

def decodeCaesar(msg):
    for i in range(0,26):
        print "".join(chr(ord("a") + (ord(s) - i + 26)%26) for s in msg[:])

result = encodeCaesar ("love",3)
print result
print decodeCaesar(result)