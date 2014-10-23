__author__ = 'juju'
import FlexCosts
import FlexStore
import FlexHelper

def HigherThanLowerThanTrigger(current_sell,current_buy,TOTALBITCOIN,TOTALUSD,buy_target,sell_target):
    if(float(current_sell)>=float(sell_target)):
        #Sell all of the coins and set your USD to the result and your total bitcoin to 0
        if(TOTALBITCOIN!=0.00):
            TOTALUSD=sell_coins(TOTALBITCOIN,TOTALUSD,current_sell)
            TOTALBITCOIN=0.00000000
    if(float(current_buy)<=float(buy_target)):
        #Buy as many coins as possible and set USD to 0
        if(TOTALUSD!=0.00):
            TOTALBITCOIN=buy_coins(TOTALBITCOIN,TOTALUSD,current_buy)
            TOTALUSD=0.00
    retvals = {'TOTALBITCOIN': TOTALBITCOIN,'TOTALUSD': TOTALUSD}
    return retvals

def buy_coins(TOTALBITCOIN,TOTALUSD,current_buy):
    if(float(TOTALBITCOIN)==0.00000000):
        TOTALBITCOIN=(float(TOTALUSD)/float(current_buy))
        FlexHelper.log("Buying: " + str(TOTALBITCOIN) + " @ " + str(current_buy) + " for " + str(TOTALUSD),"runlog.log",'a')
        FlexStore.insertBuy(TOTALBITCOIN,TOTALUSD,current_buy)
        return TOTALBITCOIN

def sell_coins(TOTALBITCOIN,TOTALUSD,current_sell):
    if(TOTALUSD==0.00):
        TOTALUSD=(float(TOTALBITCOIN)*float(current_sell))
        FlexHelper.log("Selling: " + str(TOTALBITCOIN) + " @ " + current_sell + " for " + str(TOTALUSD),"runlog.log",'a')
        FlexStore.insertSell(TOTALBITCOIN,TOTALUSD,current_sell)
        return TOTALUSD

def tick(LASTBUYPRICE, LASTSELLPRICE, SATISFYTRIGGER, TOTALBITCOIN, TOTALUSD, buy_target, sell_target, first):
    fc=FlexCosts
    fs=FlexStore
    fh=FlexHelper

    #Wait 5 Seconds
    fh.litewait(5,"s")

    #Get Prices
    coinbase_buy=fc.getCoinbaseBuy()
    current_buy=fc.retCoinbaseTotalAmount(coinbase_buy)
    coinbase_sell=fc.getCoinbaseSell()
    current_sell=fc.retCoinbaseTotalAmount(coinbase_sell)

    FlexHelper.log("Current Buy: " + current_buy + " Current Sell: " + current_sell,"runlog.log",'a')
    FlexHelper.log("Total Bitcoin: " + str(TOTALBITCOIN) + " Total USD: " + str(TOTALUSD),"runlog.log",'a')

    #If the prices changed since the last stored values
    if (float(current_buy)!=float(LASTBUYPRICE)):
        insert=fs.store("buy",coinbase_buy)
        if(first==True):
            print "inserting first buy record"
            fs.price_check_insert_first(insert)
        else:
            fs.price_check_insert_first(insert)
    #Prices did not change, dont update SQL Database
    if(float(current_buy)==float(LASTBUYPRICE)):
        FlexHelper.log("Ignoring storage of price check","runlog.log",'a')

    #If the prices changed since the last stored values
    if (float(current_sell)!=float(LASTSELLPRICE)):
        insert=fs.store("sell",coinbase_sell)
        fs.price_check_insert_first(insert)
    #Prices did not change, dont update SQL Database
    if(float(current_sell)==float(LASTSELLPRICE)):
        FlexHelper.log("Ignoring storage of price check","runlog.log",'a')

    # Call the function to decide on trades and update the totals
    updated_totals=SATISFYTRIGGER(current_sell,current_buy, TOTALBITCOIN, TOTALUSD, buy_target,sell_target)

    #Return the values for the next tick
    retvals = {'BUYTARGET': buy_target, 'SELLTARGET':sell_target, 'LASTBUYPRICE': current_buy, 'LASTSELLPRICE': current_sell, 'SATISFYTRIGGER': SATISFYTRIGGER, 'TOTALBITCOIN': updated_totals['TOTALBITCOIN'],'TOTALUSD': updated_totals['TOTALUSD']}
    return retvals