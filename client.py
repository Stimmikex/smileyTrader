import requests
import json
import subprocess

SMILEY_CONSOLE = "smileycoin-cli"

class User:
    """Smiley coin trading client instance"""

    def __init__(self, username, credits, pubKey, privKey):
        """
        Constructor for the trading client.
        Takes a client address to operate using.
        """
        self.username = username
        self.credits = credits
        self.pubKey = pubKey
        self.importPrivateKey(privKey)
    
    @staticmethod
    def getMarketValue():
        """Gets current market value of SMLY in USD"""
        return float(json.loads(requests.get("https://chainz.cryptoid.info/smly/api.dws?q=ticker.usd").text))

    @staticmethod
    def printMarketValue():
        """Prints the current market value of SMLY in USD"""
        print(f"Market value: ${format(User.getMarketValue(), 'f')}")

    def getUserBalance(self):
        """Gets the users current SMLY balance"""
        return json.loads(requests.get("https://blocks.smileyco.in/api/addr/"+ self.pubKey +"/").text)['balance']

    def printUserBalance(self):
        """Prints the users current SMLY balance"""
        print(f"Current balance: {self.getUserBalance()} SMLY")

    def displayClient(self):
        """Displays the clients address and current balance"""
        print(f"Address: {self.pubKey}")
        print(f"Balance: {self.getUserBalance} SMLY")

    def sendToAddress(self, recipient, amount, comment=None):
        """Sends an amount to a recipient with"""
        if amount < self.getUserBalance():
            query = f"{SMILEY_CONSOLE} sendtoaddress {recipient} {amount}" + (f" ( '{comment}' '{recipient}' )") if comment else ''
            subprocess.call(query, shell=True)
        else:
            print(f"User has inadiquade funds.\nCurrent balance is {self.getUserBalance()} and is smaller than the requested transfer of {amount}.")

    def importPrivateKey(self, key):
        """Imports a private key into the wallet"""
        subprocess.call(f"{SMILEY_CONSOLE} importprivkey {key}", shell=True)

    def transferCoin(self, amount, recipient):
        """Sells a given amount of SMLY to the recipient"""
        if amount <= self.getUserBalance(self.pubKey):
            subprocess.call(SMILEY_CONSOLE +' sendtoaddress '+ recipient +' '+ amount, shell=True)
        else:
            print(f"User has inadiquade funds\nCurrent balance is {self.getUserBalance()} and is smaller than the requested transfer of {amount}")
