import requests
import json
import socket
import os
import subprocess
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0

smileyConsole = 'smileycoin-cli'
Bank = 'BScjubKYSj779oXWygw1EbfRTgVjtQHPGQ'
privkey = ''

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def getUserBalance(baseAddress):
    response = json.loads(requests.get("https://blocks.smileyco.in/api/addr/"+ Bank +"/").text)
    return str(response['balance'])

def sellCoin(amount):
    if amount <= getUserBalance(Bank):
        subprocess.call(smileyConsole +' sendtoaddress '+ Bank +' '+ amount, shell=True)
    else:
        print("bruh are you broke!?")

def importprivkey(key):
    subprocess.call(smileyConsole +' importprivkey '+ key, shell=True)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        bankbal = 'Bank Balance: ' + getUserBalance(Bank)
        if not data:
            break
        connection.sendall(str.encode(bankbal))
        connection.sendall(str.encode(response))
    connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()
    