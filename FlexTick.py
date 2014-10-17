__author__ = 'juju'
import FlexCosts
import FlexStore
import FlexHelper

def HigherThanTrigger(PRICE):
    return 1

def LowerThanTrigger(PRICE):
    return 1

def tick(LASTBUYPRICE,LASTSELLPRICE,SATISFYTRIGGER,TOTALBITCOIN,TOTALUSD, conn):
    fc=FlexCosts
    fs=FlexStore
    fh=FlexHelper

    #Wait 5 Seconds
    fh.litewait(1,"s")

    #Get Prices
    coinbase_buy=fc.getCoinbaseBuy()
    current_buy=fc.retCoinbaseTotalAmount(coinbase_buy)
    coinbase_sell=fc.getCoinbaseSell()
    current_sell=fc.retCoinbaseTotalAmount(coinbase_sell)

    #If the prices changed since the last stored values
    if (coinbase_buy!=LASTBUYPRICE):
        insert=fs.store("buy",coinbase_buy)
        fs.sqlinsert(insert,conn)
    #Prices did not change, dont update SQL Database
    elif(coinbase_buy==LASTBUYPRICE):
        print "Ignoring storage of price check"

    #If the prices changed since the last stored values
    if (coinbase_sell!=LASTSELLPRICE):
        insert=fs.store("sell",coinbase_sell)
        fs.sqlinsert(insert,conn)
    #Prices did not change, dont update SQL Database
    elif(coinbase_sell==LASTSELLPRICE):
        print "Ignoring storage of price check"
    PARAM=1
    SATISFYTRIGGER(PARAM)
    retvals = {'LASTBUYPRICE': current_buy, 'LASTSELLPRICE': current_sell, 'SATISFYTRIGGER': SATISFYTRIGGER, 'TOTALBITCOIN': TOTALBITCOIN,'TOTALUSD': TOTALUSD, 'conn': conn}
    return retvals