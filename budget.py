import random
import requests
import datetime
#API_KEY = "1UNCN8Q4LIZ0G96I"
#API_KEY = "YJDNZ1VJ8A4EHE3W"
API_KEY = "0OTA7Y5GEQ94B9UH"
today = datetime.date.today()
print(today)
#Classing Bank
class Bank:
    def __init__ (self,name,balance,history):
        self.moneybalance = balance
        self.history = history
        self.name = name
        self.investings = {}
    
    #loaning
    def giveloan(self,amount,interest,duration,loaner):
        interest+=credit_rating_to_loan_interest[credit_rating]-1
        print(interest)
        if self.moneybalance > amount and loaner.moneybalance > amount*interest:
            self.moneybalance-=amount
            loaner.moneybalance+=amount
            for month in range(duration*12):
                self.moneybalance+=((amount/duration)/12)*interest
                loaner.moneybalance-=((amount/duration)/12)*interest
                print(self.moneybalance,loaner.moneybalance)
            self.history.append(("A loan was given",self.name,loaner.name,amount,interest,duration))
            loaner.history.append(("A loan was taken",loaner.name,self.name,amount,interest,duration))
        else:
            print("bank is currently unable to give you this loan")
    
    #buying stock
    def buy(self,stock_symbol,amount):
        if amount>self.moneybalance:
            raise ValueError("you don't have enough money to purchase those shares!")
        Current_URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={API_KEY}"
        response = requests.get(Current_URL)
        data = response.json()
        #getting the current price
        if "Global Quote" in data:
            stock_price = float(data["Global Quote"]["05. price"])  
        else:
            print(f'Error:{data}')
            raise TypeError("There was an error recieving data from the API")
        if not stock_price == 0:
            stock_amount = amount/stock_price
        else:
            raise ValueError("your stock has no value")
        
        if stock_symbol in self.investings.keys():
            self.investings[stock_symbol]+=float(stock_amount)
        else:
           self.investings[stock_symbol] = stock_amount
        self.moneybalance-= amount


        #selling stock
    def sell(self,stock_symbol,amount):
        Current_URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={API_KEY}"
        response = requests.get(Current_URL)
        data = response.json()
        #getting the current price
        if "Global Quote" in data:
           stock_price = float(data["Global Quote"]["05. price"])  
        else:
            print(f'Error:{data}')
            raise TypeError("There was an error recieving data from the API")
        if not stock_price == 0:
            stock_amount = amount/stock_price
        else:
            raise ValueError("your stock has no value")
        
        if stock_symbol in self.investings.keys() and self.investings[stock_symbol]>=stock_amount:
            self.investings[stock_symbol]-=float(stock_amount)
            self.moneybalance += amount
        else:
            raise ValueError("You don't have enough shares of this stock to sell!")


#Classing Costumer
class Costumer():
    def __init__(self,name,balance,history,credit_rate):
        self.moneybalance = balance 
        self.history = history
        self.credit_rate = credit_rate
        self.name = name
        self.investings = {}

    #buying stock
    def buy(self,stock_symbol,amount):
        if amount>self.moneybalance:
            raise ValueError("you don't have enough money to purchase those shares!")
        Current_URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={API_KEY}"
        response = requests.get(Current_URL)
        data = response.json()
        #getting the current price
        if "Global Quote" in data:
            stock_price = float(data["Global Quote"]["05. price"])  
        else:
            print(f'Error:{data}')
            raise TypeError("There was an error recieving data from the API")
        if not stock_price == 0:
            stock_amount = amount/stock_price
        else:
            raise ValueError("your stock has no value")
        
        if stock_symbol in self.investings.keys():
            self.investings[stock_symbol]+=float(stock_amount)
            self.history.append()
        else:
           self.investings[stock_symbol] = stock_amount
        self.moneybalance-= amount


        #selling stock
    def sell(self,stock_symbol,amount):
        Current_URL = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={API_KEY}"
        response = requests.get(Current_URL)
        data = response.json()
        #getting the current price
        if "Global Quote" in data:
           stock_price = float(data["Global Quote"]["05. price"])  
        else:
            print(f'Error:{data}')
            raise TypeError("There was an error recieving data from the API")
        if not stock_price == 0:
            stock_amount = amount/stock_price
        else:
            raise ValueError("your stock has no value")
        
        if stock_symbol in self.investings.keys() and self.investings[stock_symbol]>=stock_amount:
            self.investings[stock_symbol]-=float(stock_amount)
            self.moneybalance += amount
        else:
            raise ValueError("You don't have enough shares of this stock to sell!")


#creating credit rating list
credit_ratings = []
for letter in ["A","B","C"]:
    for i in range(3,0,-1):
        credit_ratings.extend((letter*i+"+",letter*i,letter*i+"-"))
credit_ratings.remove("AAA-")
credit_ratings.remove("AAA+")
credit_ratings.append("D")
print(credit_ratings)

CREDIT_RATING_MINIMUM = 1.0001
credit_rating_current = CREDIT_RATING_MINIMUM
credit_rating_to_loan_interest = {}
for credit_rating in credit_ratings:
    credit_rating_to_loan_interest[credit_rating] = credit_rating_current
    credit_rating_current = float(str(credit_rating_current*1.007+0.0067)[:6])
print(credit_rating_to_loan_interest)

#trying
Hapoalim = Bank("Hapoalim",500,[])
David = Costumer("David",400,[],"AA+")

David.buy("MSFT",250)
David.sell("MSFT",240)
David.sell("MSFT",5)

#Hapoalim.giveloan(300,1.1,5,David)

#print(Hapoalim.history, David.history)

print(David.investings,David.moneybalance)