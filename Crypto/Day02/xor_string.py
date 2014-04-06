
def xor_two_string(msg1,msg2):
    return "".join(chr(ord(x) ^ ord(y)) for x,y in zip(msg1[:],msg2[:]))

def xor_key_len_one(msg,key):
    result = ""
    for s in msg[:]:
        result = result + xor_two_string(s,key)
    return result


def attach_xor_len_one(cipher):
    for key in range(0, 127):
        print '[*]  ' + chr(key) + ':   ' + xor_key_len_one(cipher, chr(key))

