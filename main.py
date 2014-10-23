__author__ = 'juju'
import FlexTick
import FlexHelper
import FlexStore

def main():
    #Shorthand for imports
    ft=FlexTick
    fh=FlexHelper
    fs=FlexStore

    #Declare Variables
    TOTAL_BITCOIN=0.00000000
    TOTAL_USD=10000.00
    LAST_BUY=0
    LAST_SELL=0
    BUY_TARGET=384.00
    SELL_TARGET=390.00
    LAST_HASH=""
    FIRST_RUN=True

    fh.log("Staring Simulation - Target Buy: " + str(BUY_TARGET) + " Target Sell: " + str(SELL_TARGET) + " Total Bitcoin " + str(TOTAL_BITCOIN) + " Total USD " + str(TOTAL_USD) ,"runlog.log",'w')

    #Unencrypt the DB
    #fs.truncate()
    #Verify the DB's calculations to ensure the database is secure
    DB_HEIGHT=fs.verifyIntegrity()

    #Clear the tables in the mean time since they are not very good and the verify function has not been written


    while(1==1):
        print "current last hash: " + str(LAST_HASH)
        #if

        #Call the tick and get all the return values
        RETURN_VALUES=ft.tick(LAST_BUY, LAST_SELL, ft.HigherThanLowerThanTrigger, TOTAL_BITCOIN, TOTAL_USD, BUY_TARGET, SELL_TARGET, FIRST_RUN, LAST_HASH)

        #No longer first run
        FIRST_RUN=False
        #Set all the variables for the next tick
        #Update the current buy and sell prices
        LAST_BUY=float(RETURN_VALUES['LASTBUYPRICE'])
        LAST_SELL=float(RETURN_VALUES['LASTSELLPRICE'])

        #Update the Totals
        TOTAL_BITCOIN=float(RETURN_VALUES['TOTALBITCOIN'])
        TOTAL_USD=RETURN_VALUES['TOTALUSD']
        LAST_HASH=RETURN_VALUES['LASTHASH']

if __name__ == "__main__":
    main()