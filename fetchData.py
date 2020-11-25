import requests
import json
import subprocess

BaseSender = 'BScjubKYSj779oXWygw1EbfRTgVjtQHPGQ'
Bank = 'BScjubKYSj779oXWygw1EbfRTgVjtQHPGQ'
privateKey = ''

smileyConsole = 'smileycoin-cli'

BaseResiver = ''

def getUserBalance(baseAddress):
    response = json.loads(requests.get("https://blocks.smileyco.in/api/addr/"+ BaseSender +"/").text)
    return response['balance']

def sendtoaddress(resive, amount, comment):
    if amount <= getUserBalance(BaseSender):
        subprocess.call(smileyConsole +' sendtoaddress '+ resive +' '+ amount + '( "'+ comment +'" "'+resive+'" )', shell=True)
    else:
        print("get more money!")

def importprivkey(key):
    subprocess.call(smileyConsole +' importprivkey '+ key, shell=True)

def displayBaseSender(sender):
    response = json.loads(requests.get("https://blocks.smileyco.in/api/addr/"+ BaseSender +"/").text)
    print("BaseAddress: "+ response['addrStr'])
    print("Balance: "+ str(response['balance'])+"&sml")

def getMarketValue():
    response = json.loads(requests.get("https://chainz.cryptoid.info/smly/api.dws?q=ticker.usd").text)
    print("MarketValue: $" + format(float(response), 'f'))

def sellCoin(amount):
    if amount <= getUserBalance(BaseSender):
        subprocess.call(smileyConsole +' sendtoaddress '+ Bank +' '+ amount, shell=True)
    else:
        print("bruh are you broke!?")

# def buyCoin(amount, trade):

# for trans in response['transactions']:
#     transInfo = json.loads(requests.get("https://blocks.smileyco.in/api/tx/"+trans).text)
#     print(transInfo['vout'][0]['value'])

# sendtoaddress(smileyConsole, BaseResiver, 5, "Testing this shit")

# importprivkey(privateKey)
displayBaseSender(BaseSender)
getMarketValue()