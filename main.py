from database import Database
from string import punctuation
from tabulate import tabulate
import datetime
import client

db = Database()
user = None
# Mr moneybags bank account (Styrmir)
bank = 'BScjubKYSj779oXWygw1EbfRTgVjtQHPGQ'
commands_always = ["help", "value", "time", "products"]
commands_out = ["login", "register"]
commands_in = ["logout", "balance", "client", "buy"]

def main():
    """main function running the shop and shops cli"""
    print("\nWelcome to our *-'-_/* Theoretical *\_-'-* smiley store." )
    print("Here you can but some products for smileys.")
    print("You can log in using your username and password.")
    print(".. Or you can sign-up using a username password and your private and public wallet keys.")
    print("We promise your wallet data is not safe :) (use a throwaway, this is a demo)\n")
    while True:
        cliCommands()

def cliCommands():
    """command line interface handler for store commands"""
    global user
    args = input("$smlyShop ").split(" ")
    if args[0] in commands_always:
        if args[0] == "help":
            help()
        elif args[0] == "value":
            client.User.printMarketValue()
        elif args[0] == "time":
            print("Current time: " + datetime.datetime.now().strftime("%H:%M:%S"))
        elif args[0] == "products":
            if len(args) < 2:
                print(f"\"{args[0]}\" takes at minimum 1 positional arguments. {len(args)-1} were given.")
                return
            if args[1] == "all":
                data = getAllProducts()
                if len(data) != 0:
                    print(tabulate(data, headers=["Name", "Price", "Quantitiy"]))
                else:
                    print(f"No products are available.")
            elif args[1] == "search":
                if len(args) < 3:
                    print("You must provide criteria for the search. If you want to see all products use \"products all\"")
                    return
                data = getProducts(" ".join(args[2:]))
                if len(data) != 0:
                    print(tabulate(data, headers=["Name", "Price", "Quantitiy"]))
                else:
                    print(f"No results for {' '.join(args[2:])} are available.")
            else:
                print(f"Secondary argument of \"{args[0]}\" must be either \"all\" or \"search\" but {args[1]} was given.")
    elif args[0] in commands_out:
        if not user:
            if args[0] == "login":
                if len(args) != 3:
                    print(f"login takes in 2 arguments; username and password. {len(args)-1} were provided.")
                    return
                user = login(args[1], args[2])
            elif args[0] == "register":
                if len(args) != 5:
                    print(f"login takes in 5 arguments; username, password, public key and private key. {len(args)-1} were provided.")
                    return
                user = register(args[1], args[2], args[3], args[4])
        else:
            print(f"You must not be logged in to use \"{args[0]}\", use \"logout\" before doing \"{args[0]}\".")
    elif args[0] in commands_in:
        if not user:
            print(f"You must be logged in to use \"{args[0]}\", use \"login\" or \"register\" before doing \"{args[0]}\".")
        else:
            if args[0] == "logout":
                confirm = input("logout? (y/n) ")
                if confirm == "y":
                    print("loggin-out...")
                    user = None
                else:
                    print("continuing...")
            elif args[0] == "balance":
                user.printUserBalance()
            elif args[0] == "client":
                user.displayClient()
            elif args[0] == "buy":
                print(tabulate(getAllProducts(), headers=["Name", "Price", "Quantitiy"]))
                item = input("what product? ")
                buyProduct(item)
    else:
        print(f"\"{args[0]}\" is not a recognized command. Use \"help\" for a list of available commands.")

def help():
    """Custom help function for our cli shop interface"""
    print("Available commands:")
    print("!------------------!")

    print("Commands that are always available:")
    print("help - displays this message.")
    print("value - gets the current market value of SMLY in USD.")
    print("time - gets the current time.")
    print("products <all / <search terms>> - gets either all or searches for products by name based on terms")
    print("!------------------!")

    print("Commands that work only without a logged in user:")
    print("login - login the user")
    print("register - register new user")
    print("!------------------!")

    print("Commands that require a logged in user:")
    print("logout - logout the current user")
    print("balance - gets the users current SMLY balance")
    print("client - display information about the current user")
    print("buy <name of item> - this command buys the item of your chose.")

def getProducts(name):
    """Returns a list of available products with name like name."""
    return db.selectSQL(f"SELECT * FROM Products WHERE name LIKE ?", (f"%{name}%",))

def getAllProducts():
    """Returns a list of all available products"""
    return db.selectSQL(f"SELECT * FROM Products")

def register(username, password, pubKey, privKey):
    """Registers a new user with given parameters into the database"""
    if (db.existsSQL("Users", "username", username)):
        print("A user with that username already exists")
        return
    data = db.insertSQL(
        "INSERT INTO Users (username, password, credits, pubKey, privKey) VALUES (?, ?, ?, ?, ?)",
        (username, password, 0, pubKey, privKey)
    )
    print(f"Registered user \"{username}\".")
    return client.User(username, password, pubKey, privKey)

def login(username, password):
    """Attempts to log in user with given parameters."""
    data = db.selectSQL(f"SELECT * FROM Users WHERE username = (?) AND password = (?)", (username, password))
    if len(data) == 0:
        print("Invalid login.")
        return
    return client.User(data[0][0], data[0][2], data[0][3], data[0][4])

def buyProduct(pName):
    """Buy items with users smileyCoin."""
    if pName != None:
        price = getProducts(f"{pName}")[0][1]
        user.transferCoin(price, bank)
        quan = db.selectSQL(f"SELECT quantity FROM Products WHERE name = {getProducts(f'{pName}')[0][0]}")
        if quan == 0:
            print("There are no items for you to buy")
        else:
            db.insertSQL(f"UPDATE Products SET quantity = {quan[0]} WHERE name = {getProducts(f'{pName}')[0][0]}")
            print(f"Your balance is now: {user.getBalance()}")
            print(f"Thank you for buying {getProducts(f'{pName}')[0][0]}")
    else:
        print("product no good")

# Runs the program
if __name__ == "__main__":
    main()
