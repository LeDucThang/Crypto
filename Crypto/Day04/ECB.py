import sys
import os
import time
from Crypto.Cipher import AES

key = "0123456789ABCDEF"
mode = AES.MODE_ECB
aes = AES.new(key,mode)
userlist = []
def encrypt_string(str,key_len):
    padding = (key_len - len(str) % key_len) % key_len
    for i in range(0,padding,1):
        str = str + chr(padding)
    return aes.encrypt(str)

def decrypt_string(str):
    plaintext = aes.decrypt(str)
    return plaintext

def create_user(user):
    userlist.append(user)

def login(user):
    expire = time.strftime("%d-%m-%Y")
    role = "guest"
    if user == "thangld":
        role="administrator"
    for u in userlist:
        if user == u:
            role = "member"
    if role == "guest":
        print
    cookie = "user=" + user + "&expire=" + expire + "&role=" + role 
    return encrypt_string(cookie,len(key)).encode("hex")

def whoami(cookie):
    str = decrypt_string(cookie.decode("hex")).split('&')
    user = str[0].split('=')[1]
    expire = str[1].split('=')[1]
    role = str[2].split('=')[1]
    if role[:5] == "guest":
        print "You are a guest"
    else:
        if role[:6] == "member":
            print "You are a member"
        else:
            if role[:13] == "administrator":
                print "You are a administrator"

#######################################################################################################################
#######################################################################################################################

print "step 1: Detect mode ECB"
create_user("a")
create_user("b")
cookie_a = login("a")
cookie_b = login("b")
print "cookie a: ",cookie_a
print "cookie b: ",cookie_b

print "\nstep 2: detect key len"

milestone = len(cookie_a)
for i in range(0,100,1):
    create_user("a" * i)
    cookie_len = len(login("a" * i))
    if cookie_len > milestone : 
        print "length of cookie: ",(cookie_len - milestone)/2
        break

print "\nstep 3: detect characters in cookie"
print "because lengh of key is 16 bytes, so we need login with account have 48 character 'a' to sure that have  2 block is same"

create_user("a" * 48)
cookie_48a = login("a"*48)
for i in range(0,len(cookie_48a),32):
    print cookie_48a[i:i+32]

print "\nwe sign each block start from 0 => block[1] == block[2]"
print "so we need decrease character 'a' until block[1] != block[2]"

for i in range(47,0,-1):
    create_user("a" * i)
    cookie = login("a" * i)
    if cookie[32:64] != cookie[64:96]:
        print i+1
        break

number_a = 43
cookie_43a = login("a"*43)
for i in range(0,len(cookie_43a),32):
    print cookie_43a[i:i+32]
print "\n=> we need add 43 character 'a' to fill all 3 blocks at first"
print "now, we need decreasing 'a' one by one to detect characters in cookie"

iblock = 2
max_block = len(cookie_43a)%32
print "\nNumber of block in cookie with 43 character 'a' ",max_block
msg = "a"*43
store = []

for i in range(0,30):
    tmp = ""
    if i % len(key) == 0:
        msg = msg + "".join(store[(iblock-2)*16:(iblock-1)*16])
        iblock = 2 + i / len(key)
    msg = msg[1:]
    create_user(msg)
    cookie_i = login(msg)
    for j in range(0,128):
        user = msg + "".join(store[(iblock-2)*16:]) + chr(j)
        create_user(user)
        cookie_j = login(user)
        if cookie_j[2*32:3*32] == cookie_i[iblock*32:iblock*32+32]:
            store.append(chr(j))
            tmp = chr(j)

            break
print "Get a part of cookie string"
part_of_cookie = "".join(store)
print part_of_cookie

print "\nstep 4: cut and paste admin role to cookie to increase privilege"
print "because 'role=administrator' need 2 blocks, so we must pad 'role=administrator' to fit in 2 blocks"
msg = "a"*43
msg = msg + "re=06-04-2014&role=administrator"


print "\nCreate user with this msg and cut 2 blocks 1 and 2 (32:96)"
create_user(msg)
cookie_step4 = login(msg)
print cookie_step4[32*3:32*5]
two_last_block = cookie_step4[32*3:32*5]
print len(part_of_cookie)

print "\nWe need shift 'a' so that length of plaintext cookie with 'role=administrator' fit 5 block"
msg = "a"*38
create_user(msg)
cookie = login(msg)
print len(cookie)
whoami(cookie)
print "\nCut last block of cookie and paste last_block into"
cookie = cookie[:-64] + two_last_block
whoami(cookie)