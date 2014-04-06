import random

def xor_two_string(msg1,msg2):
    return "".join(chr(ord(x) ^ ord(y)) for x,y in zip(msg1[:],msg2[:]))

    return result

def oracle_with_prefix_and_suffix(msg):
    key = ""
    prefix = ""
    suffix = ""

    # create key random
    len_key= random.randrange(20,100,1)
    for i in range(0,len_key,1):
        key = key + chr(random.randrange(0,255,1))
    # create prefix random
    len_prefix = random.randrange(20,100,1)
    for i in range(0,len_prefix,1):
        prefix = prefix + chr(random.randrange(0,255,1))

    # create suffix random
    len_suffix = random.randrange(20,100,1)
    for i in range(0,len_suffix,1):
        suffix = suffix + chr(random.randrange(0,255,1))

    print "Key: " + key.encode("hex")
    result = ""
    msg = prefix + msg + suffix
    for i in range(0,len(msg),len(key)):
        min_len = min(len(msg)-i,len(key))
        result = result + xor_two_string(msg[i:i+min_len],key[:min_len]).encode("hex")
    return result

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def get_max_substring_not_repeated(str):
    max_len = 0
    max_index = 0
    max_substring = ""
    max_match = 0
    max_list = []
    result = ""
    for i in range(0,len(str)-1):
        for j in range(i+1,len(str)):
            match = 0
            index_in_list = 0
            list_index_substring = list(find_all(str,str[i:j]))
            for k in range(0,len(list_index_substring)-2):
                if int(list_index_substring[k]) + (j-i) == int(list_index_substring[k+1]):
                    if index_in_list == 0:
                        index_in_list = k
                    match += 1

            if match >=1 and (j-i) > max_len:
                max_len = j-i
                max_index = list_index_substring[index_in_list]
                max_substring = str[int(list_index_substring[index_in_list]):int(list_index_substring[index_in_list+1])]
    for i in range(max_index,max_index+max_len,1):
        if  i % len(max_substring) == 0:
            result = str[i:i+max_len]
            break
    return max_len, result
cipher1 = oracle_with_prefix_and_suffix("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000".decode("hex"))

print cipher1


print get_max_substring_not_repeated(cipher1)

#list = list_index_substring = list(find_all(cipher1,cipher1[0:1]))
#print int(list[0]) + (1-0)