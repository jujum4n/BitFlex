__author__ = 'juju'
import hashlib
import datetime
import sqlite3 as lite
import FlexHelper

def store(TYPE,DICT):
    hs=hashlib
    datahash=hs.sha256(str(DICT))
    ts=datetime.datetime.now()
    hexdigest=str(datahash.hexdigest())
    airy = {'totalamount': DICT['totalamount'],'subtotalamount': DICT['subtotalamount'] ,'coinbasefee': DICT['coinbasefee'], 'bankfee': DICT['bankfee'],'digested_storage': hexdigest, 'type': TYPE, 'timestamp': ts}
    if(verifystore(hexdigest,DICT)):
        return airy
    else:
        return 0

def price_check_insert(diction):
    con = lite.connect('price_checks.db')
    with con:
        cur = con.cursor()
        #Grab the length of the database
        cur.execute('SELECT * FROM price_checks')
        temp=len(cur.fetchall())
        #Grab the last hash stored at the last spot
        cur.execute(str('SELECT digested_storage FROM price_checks where ROWID='+str(temp)))
        all_rows = cur.fetchall()
        print "last hash= " +  str(all_rows[0][0]) + " This Current hash: " + str(diction["digested_storage"])
        digested=hashlib.sha256(str(all_rows[0][0])+str(diction["digested_storage"]))
        print "combined hash = " + str(digested.hexdigest())

        cur.execute('INSERT INTO price_checks values (?,?,?,?,?,?,?)', [float(diction["totalamount"]), float(diction["subtotalamount"]), float(diction["coinbasefee"]), float(diction["bankfee"]), str(digested.hexdigest()), str(diction["type"]), diction["timestamp"]])
        FlexHelper.log("INSERTING: " + str(diction) + " into price_checks.db","runlog.log",'a')
        return True
    return False

def price_check_insert_first(diction):
    con = lite.connect('price_checks.db')
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO price_checks values (?,?,?,?,?,?,?)', [float(diction["totalamount"]), float(diction["subtotalamount"]), float(diction["coinbasefee"]), float(diction["bankfee"]), str(diction["digested_storage"]), str(diction["type"]), diction["timestamp"]])
        FlexHelper.log("INSERTING: " + str(diction) + " into price_checks.db","runlog.log",'a')
        return True
    return False

def insertSell(TOTALBITCOIN,TOTALUSD,current_sell):
    con = lite.connect('price_checks.db')
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO transactions values (?,?,?,?)', [str("sell"),float(TOTALBITCOIN), float(TOTALUSD), float(current_sell)])
        FlexHelper.log("INSERTING: " + "sell Total Bitcoin: " + str(TOTALBITCOIN) + " Total USD: " + str(TOTALUSD) + " Current Sell: " +str(current_sell) + " into price_checks.db","runlog.log",'a')

def insertBuy(TOTALBITCOIN,TOTALUSD,current_buy):
    con = lite.connect('price_checks.db')
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO transactions values (?,?,?,?)', [str("buy"),float(TOTALBITCOIN), float(TOTALUSD), float(current_buy)])
        FlexHelper.log("INSERTING: " + "buy Total Bitcoin: " + str(TOTALBITCOIN) + " Total USD: " + str(TOTALUSD) + " Current Buy: " +str(current_buy) + " into price_checks.db","runlog.log",'a')

def truncate():
    con = lite.connect('price_checks.db')
    with con:
        cur = con.cursor()
        cur.execute('delete from transactions')
        cur.execute('delete from price_checks')
        FlexHelper.log("Truncating tables","runlog.log",'a')

#Verifies the given hash for a stored dictionary
def verifystore(HASH,DICT):
    hs=hashlib
    if(str(hs.sha256(str(DICT)).hexdigest())==HASH):
        return True
    else:
        return False