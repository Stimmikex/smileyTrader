import requests
import json
import subprocess

SMILEY_CONSOLE = "smileycoin-cli"
BANK = 'BScjubKYSj779oXWygw1EbfRTgVjtQHPGQ'

class Client:
    """Smiley coin trading client instance"""
    def __init__(self, clientAddress):
        """
        Constructor for the trading client.
        Takes a client address to operate using.
        """
        self.address = clientAddress

    def getMarketValue(self):
        """Gets current market value of SMLY in USD"""
        return float(json.loads(requests.get("https://chainz.cryptoid.info/smly/api.dws?q=ticker.usd").text))

    def printMarketValue(self):
        """Prints the current market value of SMLY in USD"""
        print(f"Market value: ${format(self.getMarketValue(), 'f')}")

    def getUserBalance(self):
        """Gets the users current SMLY balance"""
        return json.loads(requests.get("https://blocks.smileyco.in/api/addr/"+ self.address +"/").text)['balance']

    def printUserBalance(self):
        """Prints the users current SMLY balance"""
        print(f"Current balance: {self.getUserBalance()} SMLY")

    def displayClient(self):
        """Displays the clients address and current balance"""
        print(f"Address: {self.address}")
        print(f"Balance: {self.getUserBalance} SMLY")

    def sendToAddress(self, recipient, ammount, comment=None):
        """Sends an ammount to a recipient with"""
        if ammount < self.getUserBalance():
            query = f"{SMILEY_CONSOLE} sendtoaddress {recipient} {ammount}" + (f" ( '{comment}' '{recipient}' )") if comment else ''
            subprocess.call(query, shell=True)
        else:
            print(f"User has inadiquade funds.\nCurrent balance is {self.getUserBalance()} and is smaller than the requested transfer of {ammount}.")

    def importPrivateKey(self, key):
        """Imports a private key into the wallet"""
        subprocess.call(f"{SMILEY_CONSOLE} importprivkey {key}", shell=True)

    def sellCoin(self, ammount):
        """Sells a given ammount of SMLY to the bank"""
        if ammount <= self.getUserBalance(self.address):
            subprocess.call(SMILEY_CONSOLE +' sendtoaddress '+ BANK +' '+ ammount, shell=True)
        else:
            print(f"User has inadiquade funds\nCurrent balance is {self.getUserBalance()} and is smaller than the requested transfer of {ammount}")
