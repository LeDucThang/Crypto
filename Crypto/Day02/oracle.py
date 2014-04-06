import random
def xor_two_string(msg1,msg2):
    return "".join(chr(ord(x) ^ ord(y)) for x,y in zip(msg1[:],msg2[:]))

def oracle(msg):
    key = ""
    len_key = random.randrange(20,100,1)
    for i in range(0,len_key,1):
        key = key + chr(random.randrange(0,255,1))
    result = ""

    for i in range(0,len(msg),len(key)):
        min_len = min(len(msg)-i,len(key))
        result = result + xor_two_string(msg[i:i+min_len],key[:min_len]).encode("hex")
    return result

def oracle_with_prefix_and_suffix(msg):
    key = "abcdefgagasdfjasdfkh"
    prefix = ""
    suffix = ""

    # create prefix random
    len_prefix = random.randrange(2,10,1)
    for i in range(0,len_prefix,1):
        prefix = prefix + chr(random.randrange(0,255,1))

    # create suffix random
    len_suffix = random.randrange(2,10,1)
    for i in range(0,len_suffix,1):
        suffix = suffix + chr(random.randrange(0,255,1))

    print "Key: " + key.encode("hex")
    result = ""
    msg = prefix + msg + suffix
    for i in range(0,len(msg),len(key)):
        min_len = min(len(msg)-i,len(key))
        result = result + xor_two_string(msg[i:i+min_len],key[:min_len]).encode("hex")
    return result

def max_substring(str1,str2):
    f =  [[0 for x in xrange(len(str2))] for x in xrange(len(str1))] 
    trace = [[0 for x in xrange(len(str2))] for x in xrange(len(str1))] 
    for i in range(0,len(str1)):
        for j in range(0,len(str2)):
            f[i][j]=0
            trace[i][j]=-2
    for i in range(1,len(str1)):
        for j in range(1,len(str2)):
            if str1[i-1] == str2[j-1]:
                f[i][j] = f[i-1][j-1] +1
                trace[i][j]=0
            else:
                if (f[i-1][j] > f[i][j-1]):
                    f[i][j] = f[i-1][j]
                    trace[i][j] = 1
                else:
                    f[i][j] = f[i][j-1]
                    trace[i][j] = -1
    return trace

def trace_string(trace,str1,str2):
    result = ""
    m = len(str1) - 1
    n = len(str2) - 1
    index_trace = []
    while (m > 0 and n > 0 ):
        if trace[m][n] == 0:
            result = result + str1[m]
            m = m-1
            n = n-1
            index_trace.append(m)
        else:
            if trace[m][n] == 1:
                m = m-1
            else:
                if trace[m][n] == -1:
                    n = n-1
    return get_max_substring(index_trace[::-1],str1)

def get_max_substring(trace,str):
    max_len_substring = 0
    index_substring = 0
    max_substring = ""
    i = 0
    while i < len(trace):
        len_substring = 1
        index = trace[i]
        while i < len(trace)-1 and trace[i]+1 == trace[i+1]:
            len_substring += 1
            i += 1
        if len_substring > max_len_substring:
            max_len_substring = len_substring
            index_substring = index
        i += 1
    return str[index_substring:index_substring + max_len_substring], index_substring,trace

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def get_max_substring_not_repeated(str):
    max_len = 0
    max_substring = ""
    for i in range(1,len(str)):
        count = list(find_all(str, str[:i]))
        if len(count) > 1 and int(count[0]) + i == int(count[1]) and i > max_len:
            max_len = i
    return max_len

cipher1 = oracle_with_prefix_and_suffix("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000".decode("hex"))

cipher2 = oracle_with_prefix_and_suffix("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000".decode("hex"))
print cipher1

trace = max_substring(cipher1,cipher2)  # trace in 2D
max_substring_continue, max_index_substring, trace = trace_string(trace,cipher1,cipher2) # trace in 1D, only store index of cipher1
index_max_substring = 0
max_len_substring = get_max_substring_not_repeated(max_substring_continue)
for i in range(max_index_substring+1,trace[-1]):
    if i % max_len_substring == 0:
        index_max_substring = i
        break

print cipher1[index_max_substring:(index_max_substring+max_len_substring)]