__author__ = 'juju'
import FlexTick
import FlexHelper
import FlexStore

def main():

    #Declare Variables
    TOTALBITCOIN=0.00000000
    TOTALUSD=10000.00
    lastbuy=0
    lastsell=0
    buy_target=384.00
    sell_target=390.00

    ft=FlexTick
    fh=FlexHelper
    fs=FlexStore

    #Clear the tables in the mean time
    fs.truncate()
    first=True

    fh.log("Staring Simulation - Target Buy: " + str(buy_target) + " Target Sell: " + str(sell_target) + " Total Bitcoin " + str(TOTALBITCOIN) + " Total USD " + str(TOTALUSD) ,"runlog.log",'w')

    while(1==1):

        #Add code here later to check if the db has count greater than 1
        #Meaning isfirst is false otherwise true

        #Call the tick and get all the return values
        retvals=ft.tick(lastbuy, lastsell, ft.HigherThanLowerThanTrigger, TOTALBITCOIN, TOTALUSD, buy_target, sell_target, first)

        #No longer first run
        first=False
        #Set all the variables for the next tick
        #Update the current buy and sell prices
        lastbuy=float(retvals['LASTBUYPRICE'])
        lastsell=float(retvals['LASTSELLPRICE'])

        #Update the Totals
        TOTALBITCOIN=float(retvals['TOTALBITCOIN'])
        TOTALUSD=retvals['TOTALUSD']


if __name__ == "__main__":
    main()