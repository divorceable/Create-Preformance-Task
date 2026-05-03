# My Partners Modules
import tkinter as tk
from tkinter import ttk
# My Modules
import requests as r
import time
from time import sleep

# My Code
# Defines Constants
currencies = ["USD", "AUD", "EUR", "JPY", "GBP", "CNY", "SGD"]
currency_symbols = ["$", "A$", "€", "¥", "£", "¥", "S$"]
apikey = "" # Enter your API key here (https://coinmarketcap.com/api/pricing/)
total_coins = 20

class Crypto:
 
   def __init__(self, name:str, index:int, price:float, movement:list):
       self.name = name
       self.index = index
       self.price = price
       self.movement = movement

   def get_name(self):
       return self.name
 
   def get_movement(self):
       return self.movement
   
   def get_price(self):
       return self.price
 
   def get_index(self):
       return self.index
 
   def contents(self):
       contents = [self.name, self.price, self.movement, self.index]
       return contents
 
   def __repr__(self):
       return f"{self.name} (${self.price}) REPR"

# My Code
def fetch_cryptos(user_currency, possible_coins):
   url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
   formal_currency = currencies[user_currency]
   error_flag = False
   response = None 

   params = {
   'start':'1',
   'limit': possible_coins, # Coins in json
   'convert': formal_currency # "USD", "GBP", etc 
   }

   headers =  {
   'Accept': 'application/json', # Tell them we want JSON data
   'X-CMC_PRO_API_KEY': apikey,
    }  

   if apikey.strip() == "":
       print("Error: No API Key Found")
       print("Closing...")
       time.sleep(5)

   else:
       try: 
        response = r.get(url, params=params, headers=headers)
       except Exception:
           error_flag = True
           raise Exception("Error: Check Internet Connection!")

   if error_flag != True: 
        if response.status_code != 200 and response.status_code != 404:
            print(f"Error: {response.status_code} - {response.reason}")  
        elif response.status_code == 404:
            print("Please check your internet connection")
        response = response.json()

   return response

# My Code
def getPrice(data, currency, index):  # Gets price based on currency and coin-index
   price = round(data["data"][index]["quote"][currency]["price"],2)
   return price

# My Code
def getMove(data, currency, index):  # Gets movement (percentage) of currency cusing currency and coin-index
   move90d = round(data["data"][index]["quote"][currency]["percent_change_90d"], 2)
   move24h = round(data["data"][index]["quote"][currency]["percent_change_24h"], 2)
   move30d = round(data["data"][index]["quote"][currency]["percent_change_30d"], 2)
   movements = [move90d, move30d, move24h]
   return movements

# My Code
def getName(data, index):  # Gets the offical name of a coin based on index and response
   name = data["data"][index]["name"]
   return name

# My Code
def make_cryptos(user_currency, site_response):
   response = site_response
   if response == None: 
    raise Exception("Error: Please check your internet connection")
   all_coins = {}

   for cryptos in range(total_coins):

       crypto_index = cryptos
       crypto_price = getPrice(response, currencies[user_currency], cryptos)
       crypto_name = getName(response, cryptos)
       crypto_movement = getMove(response, currencies[user_currency], cryptos)

       all_coins[crypto_name] = Crypto(name=crypto_name, 
                                       price=crypto_price, 
                                       movement=crypto_movement, 
                                       index=crypto_index)

   return all_coins

# My Code
def get_coin_names(site_response):
   response = site_response
   if response == None: 
        raise Exception("Error: Please check your internet connection")
   coin_names = []

   for cryptos in range(total_coins):
       coin_names.append(getName(response, cryptos))
 
   return coin_names

# My Partners Code
def main():
    def input_checker():
        #gives you an error message if you dont enter one of the values
        inputs = [(currency_entry.get(), "Please select a currency"),(crypto_entry.get(), "Please enter a cryptocurrency")]

        #checks for errors and stops if you get one if not continues
        for value, error_message in inputs:
            if not value:
                choice.config(text = error_message)
                return

        #if no error is found
        currency_choice = currency_entry.get()
        crypto_choice = crypto_entry.get()

        # My Code
        curr_index = currencies.index(currency_choice)
        response = fetch_cryptos(curr_index, total_coins)
        all_coins = make_cryptos(currencies.index(currency_choice), response)
        movements = all_coins[crypto_choice].get_movement()

        choice.config(text = f"Selected Currency: {currency_choice} | Selected Crypto: {crypto_choice}")
        price.config(text = f"Price: {currency_symbols[curr_index] + str(all_coins[crypto_choice].get_price())}")
        movement_90_days.config(text = (f"90 Day Movement: {movements[0]}%"))
        movement_30_days.config(text = (f"30 Day Movement: {movements[1]}%"))
        movement_1_day.config(text = (f"1 Day Movement: {movements[2]}%"))

    # My Partners Code
    #creates the window for the GUI
   
    root = tk.Tk()
    root.title("Crypto Price Tracker")
    root.geometry("500x420")

    #creates text(label) asking what currency you want and displays it in the root
    currency_question = ttk.Label(root, text = "What currency would you like to use?", font = ("courier new", 12))
    currency_question.pack( pady = (20, 10))

    #gives the user options to pick from and stores it
    currency_entry = tk.StringVar()
 
    response = fetch_cryptos(0, total_coins)
    crypto_entry = tk.StringVar()
    cryptos = get_coin_names(response)

    #creates currency the dropdown
    dropdown = ttk.Combobox(root, textvariable = currency_entry, values = currencies, state = "readonly", width = 15)
    dropdown.pack(pady = 5)

    #creates text in the root asking what crypto currency you want
    crypto_question = ttk.Label(root, text = "Enter cryptocurrency:", font = ("courier new", 12))
    crypto_question.pack(pady = (20, 5))

    #creates a crypto dropdown input box
    crypto_dropdown = ttk.Combobox(root, textvariable = crypto_entry, values = cryptos, state = "readonly", width = 15)
    crypto_dropdown.pack(pady = 5)

    #creates a submit button
    button = ttk.Button(root, text = "Submit", command = input_checker)
    button.pack(pady = 10)

    #displays what you picked or an error message
    choice = ttk.Label(root, text = "", font = ("courier new", 10))
    choice.pack(pady = 5)

    price = ttk.Label(root, text =  "", font = ("courier new", 10))
    price.pack(pady = 5)

    # My code
    movement_90_days = ttk.Label(root, text="", font=("Courier New", 10))
    movement_90_days.pack(pady = 5 )

    movement_30_days = ttk.Label(root, text = "", font = ("Courier new", 10))
    movement_30_days.pack(pady = 5 )

    movement_1_day = ttk.Label(root, text = "", font = ("Courier new", 10))
    movement_1_day.pack(pady = 5 )

    footer_frame = tk.Frame(root)
    footer_frame.pack(side='bottom', fill='x', pady=8)

    footer_label = tk.Label(
        footer_frame,
        text="Crypto Price Tracker • Data from CoinMarketCap API",
        font=("Courier New", 9),
        fg="#666666"
    )

    footer_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()












  



