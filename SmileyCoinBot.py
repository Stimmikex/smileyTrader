import requests
import time
from bs4 import BeautifulSoup

URL = 'https://chainz.cryptoid.info/smly/'
page = requests.get(URL)

data = []

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find("table", _class='table-condensed')

x = ""

while((x != "exit")):

    data = []

    coin_elems = results.find_all('data-id')

    for coin_elem in coin_elems:
        account_elem = coin_elem.find('code')
        time_elem = coin_elem.find('td', _class="hidden-xxs")
        amount_elem = coin_elem.find('td', _class="amount-units")
        if int(amount_elem.text) > 200.000:
            flag_check = "WoW that is a lot of money"
        else: 
            flag_check = "better luck next time"
        data += {"account": account_elem.text, "time" : time_elem.text, "amount" : amount_elem.text, "flag" : flag_check}

    time.sleep(10)

    print(data)

    x = input("to stop (exit): ")

    time.sleep(5)
