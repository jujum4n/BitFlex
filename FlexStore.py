__author__ = 'juju'
import hashlib
import datetime
import sqlite3

def connect():
    conn = sqlite3.connect('example.db')
    c=conn.cursor()
    #c.execute('''CREATE TABLE pricechecks
    #         (timestamp text, totalamount real, subtotalamount real, coinbasefee real, bankfee real, digested_storage BLOB, type text)''')
    return conn

def store(TYPE,DICT):
    hs=hashlib
    datahash=hs.sha256(str(DICT))
    ts=str(datetime.datetime.now())
    hexdigest=str(datahash.hexdigest())
    airy = {'totalamount': DICT['totalamount'],'subtotalamount': DICT['subtotalamount'] ,'coinbasefee': DICT['coinbasefee'], 'bankfee': DICT['bankfee'],'digested_storage': hexdigest, 'type': TYPE, 'timestamp': ts}
    if(verifystore(hexdigest,DICT)):
        return airy
    else:
        return 0

def sqlinsert(dict, conn):
    cursor=conn.cursor()
    cursor.execute('insert into pricechecks values (?,?,?,?,?,?,?)', [dict["totalamount"], dict["subtotalamount"], dict["coinbasefee"], dict["bankfee"], dict["digested_storage"], dict["type"], dict["timestamp"]])
    #cursor.execute('INSERT INTO pricechecks(totalamount,subtotalamount,coinbasefee,bankfee,digested_storage,type,timestamp)', [dict["totalamount"], dict["subtotalamount"], dict["coinbasefee"], dict["bankfee"], dict["digested_storage"], dict["type"], dict["timestamp"]])
    #cursor.execute("INSERT INTO pricechecks VALUES (?,?,?,?,?,?,?)", [dict["totalamount"], dict["subtotalamount"], dict["coinbasefee"], dict["bankfee"], dict["digested_storage"], dict["type"], dict["timestamp"]])
    return 1

#Verifies the given hash for a stored
def verifystore(HASH,DICT):
    hs=hashlib
    if(str(hs.sha256(str(DICT)).hexdigest())==HASH):
        print "Hash verification successful"
        return True
    else:
        print "Hash verification failure"
        return False
