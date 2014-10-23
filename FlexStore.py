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
        #print "last hash= " +  str(all_rows[0][0]) + " This Current hash: " + str(diction["digested_storage"])
        digested=hashlib.sha256(str(all_rows[0][0])+str(diction["digested_storage"]))
        #print "combined hash = " + str(digested.hexdigest())
        cur.execute('INSERT INTO price_checks values (?,?,?,?,?,?,?)', [float(diction["totalamount"]), float(diction["subtotalamount"]), float(diction["coinbasefee"]), float(diction["bankfee"]), str(digested.hexdigest()), str(diction["type"]), diction["timestamp"]])
        FlexHelper.log("INSERTING: " + str(diction) + " into price_checks.db","runlog.log",'a')
        return True
    return False

def price_check_insert_first(diction, LASTHASH):
    con = lite.connect('price_checks.db')
    with con:
        cur = con.cursor()
        if(LASTHASH==""):
            cur.execute('INSERT INTO price_checks values (?,?,?,?,?,?,?)', [float(diction["totalamount"]), float(diction["subtotalamount"]), float(diction["coinbasefee"]), float(diction["bankfee"]), str(diction["digested_storage"]), str(diction["type"]), diction["timestamp"]])
            FlexHelper.log("INSERTING: " + str(diction) + " into price_checks.db","runlog.log",'a')
            return str(diction["digested_storage"])
        else:
            #print "New Dictionary Hash: " + str(diction["digested_storage"])
            #print "last hash to add in: " + str(LASTHASH)
            #print "resulting string combination: " + str(str(LASTHASH)+str(diction["digested_storage"]))
            #print "combined hash of whole string: " + hashlib.sha256(str(LASTHASH)+str(diction["digested_storage"])).hexdigest()
            inserthash=hashlib.sha256(str(LASTHASH)+str(diction["digested_storage"])).hexdigest()
            #print "Insert hash: " + str(inserthash)
            cur.execute('INSERT INTO price_checks values (?,?,?,?,?,?,?)', [float(diction["totalamount"]), float(diction["subtotalamount"]), float(diction["coinbasefee"]), float(diction["bankfee"]), inserthash, str(diction["type"]), diction["timestamp"]])
            FlexHelper.log("INSERTING: " + str(diction) + " into price_checks.db","runlog.log",'a')
            return inserthash

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

def verifyIntegrity():
    #Create a dictionary from each row
    con = lite.connect('price_checks.db')
    LAST_HASH=""
    with con:
        cur = con.cursor()
        #Grab the length of the database
        cur.execute(str('SELECT * FROM price_checks'))
        #DATABASE_LENGTH=len(cur.fetchall())
        #Grab the last hash stored at the last spot
        all_rows = cur.fetchall()
        for row in all_rows:
            # row[0] returns the first column in the query (name), row[1] returns email column.
            print str(row[0]) + str(row[1]) + str(row[2]) + str(row[3]) + str(row[4]) + str(row[5]) + str(row[6])
            recon={'totalamount': str('u')+str(row[0]),'subtotalamount': row[1] ,'coinbasefee': row[2], 'bankfee': row[3], 'type': row[5], 'timestamp': row[6]}
            print "Dictionary Contents: " + str(recon)
            print "Entire Dictionary Hash: " +str(hashlib.sha256(str(recon)).hexdigest())
            print "First Hash to match: " + str(row[4])
            justice=verifystore(str(hashlib.sha256(str(str(LAST_HASH)+str(row[4]))).hexdigest()),str(recon))
            if(justice==True):
                print "True"
                LAST_HASH=str(row[4])
            else:
                print "False"

    #Calculate the first Dictionaries HASH
    #Chain the First hash into the calculation for all the rest
    #if (verifyStore(HASH,DICT)!=True):
        #return 0
    return 1

#{'timestamp': '2014-10-23 14:09:48.121000', 'bankfee': u'0.15', 'totalamount': u'363.33', 'coinbasefee': u'3.60', 'type': 'buy', 'subtotalamount': u'359.58'}
#{'timestamp': '2014-10-23 14:09:48.121000', 'bankfee': '0.15', 'totalamount': '363.33', 'coinbasefee': '3.6', 'type': 'buy', 'subtotalamount': '359.58'}