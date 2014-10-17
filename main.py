__author__ = 'juju'
import FlexCosts
import FlexStore
import FlexHelper
import FlexTick

storage=[]
def main():
    totalbitcoin=100.00000000
    totalusd=10000.00
    lastbuy=0
    lastsell=0
    fc=FlexCosts
    fs=FlexStore
    fh=FlexHelper
    ft=FlexTick

    conn=FlexStore.connect()
    while(1==1):
        retvals=ft.tick(lastbuy,lastsell,ft.HigherThanTrigger,totalbitcoin,totalusd,conn)
        lastbuy=retvals['LASTBUYPRICE']
        lastsell=retvals['LASTSELLPRICE']
        conn=retvals['conn']
    conn.close()
if __name__ == "__main__":
    main()