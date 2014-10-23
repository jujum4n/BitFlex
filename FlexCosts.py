__author__ = 'juju'
import urllib
import urllib2
import json
import datetime

def getCoinbaseBuy():
    urllib.urlencode({'qty': '1', 'currency': 'USD'})
    data=json.load(urllib2.urlopen("https://api.coinbase.com/v1/prices/buy?"))
    ts=str(datetime.datetime.now())
    airy = {'totalamount': '0','subtotalamount': '0' ,'coinbasefee': '0', 'bankfee': '0', 'type': "buy", 'timestamp': ts}
    airy['totalamount']=data['amount']
    airy['subtotalamount']=data['subtotal']['amount']
    cbasetotal=data['fees'][0]
    airy['coinbasefee']=cbasetotal['coinbase']['amount']
    banktotal=data['fees'][1]
    airy['bankfee']=banktotal['bank']['amount']
    print str(airy)
    return airy

def retCoinbaseTotalAmount(airy):
    return airy['totalamount']

def getCoinbaseSell():
    urllib.urlencode({'qty': '1', 'currency': 'USD'})
    data=json.load(urllib2.urlopen("https://api.coinbase.com/v1/prices/sell?"))
    ts=str(datetime.datetime.now())
    airy = {'totalamount': '0','subtotalamount': '0' ,'coinbasefee': '0', 'bankfee': '0', 'type': "sell", 'timestamp': ts }
    airy['totalamount']=data['amount']
    airy['subtotalamount']=data['subtotal']['amount']
    cbasetotal=data['fees'][0]
    airy['coinbasefee']=cbasetotal['coinbase']['amount']
    banktotal=data['fees'][1]
    airy['bankfee']=banktotal['bank']['amount']
    return airy