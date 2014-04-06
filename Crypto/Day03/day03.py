import random

def hamming_distance(x,y):
    count = 0
    bin_x = bin(x)[::-1]
    bin_y = bin(y)[::-1]
    len_min = min(len(bin_x),len(bin_y))
    for i in range(0,len_min-2):
        if bin_x[i] != bin_y[i]:
            count += 1
    len_max = max(len(bin_x),len(bin_y))
    count = count + len_max - len_min
    return count


char_start = 32
char_end = 127
set2 = [] # cchua cac tap plain text thoa man
set3 = [] # chua cac key tam thoi
set4 = [] # chua cac key thoa man
def oracle(a):
    HD_MAX = 0
    u = 0
    v = 0
    set2 = []
    set3 = []
    set4 = []

    for i in range(0,len(a)):
        for j in range(0,len(a)):
            if i < j :
                if hamming_distance(a[i],a[j]) > HD_MAX:
                    HD_MAX = hamming_distance(a[i],a[j])
                    u = i
                    v = j
    for i in range(char_start, char_end+1):
        for j in range(char_start, char_end+1):
            if (i<j):
                if (i^j) == (a[u]^a[v]):
                    set2.append([i,j])

    for i in range(0,len(set2)):
        set3.append(set2[i][0]^a[u])
        set3.append(set2[i][0]^a[v])

    for i in range(0,len(set3)):
        choose = True
        for j in range(0,len(a)):
            if a[j] ^ set3[i] < char_start or a[j] ^ set3[i] > char_end:
                choose = False
        if choose:
            set4.append(set3[i])
    return set4

b = []

def compute_key():
    file = open('cipher.txt', 'r')
    for line in file:
        b.append(line.decode('base64'))
    file.close()
    for k in range(0,20):
        a = []
        result_set = []
        for i in range(0,len(b)):
            if (len(b[i]) > k+1):
                a.append(ord(b[i][k]))
        set = oracle(a)
        for i in range(0,len(b)):
            if (len(b[i]) > k+1):
                result_set.append(chr(set[0]^ord(b[i][k])))
        print result_set


compute_key()