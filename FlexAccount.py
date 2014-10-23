__author__ = 'juju'

class FlexAccount:
    TOTAL_BITCOIN=0
    TOTAL_USD=0

    def __init__(self, STARTING_TOTAL_BITCOIN, STARTING_TOTAL_USD):
        FlexAccount.TOTAL_BITCOIN=STARTING_TOTAL_BITCOIN
        FlexAccount.TOTAL_USD=STARTING_TOTAL_USD

    def displayBitcoin(self):
        print "Bitcoin Value is: %d" % FlexAccount.TOTAL_BITCOIN

    def displayUSD(self):
        print "USD Value is: %d" % FlexAccount.TOTAL_USD