import requests
import time
from exmo import ExmoAPI
import json
import telebot


bot = telebot.TeleBot('961756482:AAF6DWHh0sW7PPIK1ivdst9rafxl911SFqs')
api_key = "K-96058d8097384af0c3ea99a887881f7fdfdbb49e"
api_secret = "S-d8f83f81d241f929f63357618409416604550938"


obj = ExmoAPI(api_key, api_secret)

def sell_price(obj,current_pair:str):
    try:
        response = requests.get("https://api.exmo.com/v1/trades/?pair=BTC_USD&limit=100")
    except :
        bot.send_message("@buyingapples", "Connection error : apple tree is not avaliable now...\n" )
        return None
    Unix_time = int(time.time())
    previous_orders =  []
    for order in response.json()[current_pair]:
        if(order["type"] == "sell" and (Unix_time - order["date"]) < 180):
            previous_orders.append(order["price"])
    try:
        sum = 0.0
        for  i  in previous_orders:
            sum += float(i)
        price = sum/len(previous_orders) + sum/len(previous_orders)*0.003
        return price
    except ZeroDivisionError:
        return None

def buy_price(obj,current_pair:str):
    try:
        response = requests.get("https://api.exmo.com/v1/trades/?pair=BTC_USD&limit=100")
    except :
        bot.send_message("@buyingapples", "Connection error : apple tree is not avaliable now...\n" )
        return None
    Unix_time = int(time.time())
    previous_orders =  []
    for order in response.json()[current_pair]:
        if(order["type"] == "buy" and (Unix_time - order["date"]) < 180):
            previous_orders.append(order["price"])
    try:
        sum = 0.0
        for  i  in previous_orders:
            sum += float(i)
        price = sum/len(previous_orders)
        return price
    except ZeroDivisionError:
        return None


def trade(obj):
    currency1 = "BTC"
    currency2 = "USD"

    order_counter = 0 
    current_pair = currency1 + "_" + currency2
    order_life_time = 5 
    can_spend = 5
    previous_orders = 0
    buy_dict = {}
    sell_dict = {}

    user_info = obj.api_query("user_info")
    #Если бот вылетел
    if (float(user_info["balances"]["BTC"])!= 0):
        with open("log.txt","rt") as f:
            previous_orders = float(f.read())
        avg_sell_price = sell_price(obj, current_pair)
        if (avg_sell_price != None):
            if (1 - previous_orders/avg_sell_price) * 100 >= 0.005:
                sell_dict = {"pair":current_pair,"quantity": float(user_info["balances"]["BTC"]),"price":previous_orders + previous_orders*0.004,"type":"sell"}
            else:
                sell_dict = {"pair":current_pair,"quantity": float(user_info["balances"]["BTC"]),"price":previous_orders + previous_orders*0.003,"type":"sell"}
        while True:
            result : dict = obj.api_query("order_create" , sell_dict)
            if (result["result"] == False):
                time.sleep(120)
                bot.send_message("@buyingapples", "Waiting for order_create to sell ...\n" )
            else:
                break


    time.sleep(order_life_time*60)
    open_orders : dict = obj.api_query("user_open_orders")
    if len(open_orders) != 0:
        sell_dict["price"] = sell_dict["price"] - sell_dict["price"]*0.001
        while len(open_orders) != 0:
            obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
            while True:
                result : dict = obj.api_query("order_create" , sell_dict)
                if (result["result"] == False):
                    time.sleep(120)
                    bot.send_message("@buyingapples", "Waiting for order_create to sell ...\n" )
                else:
                    break
            open_orders : dict = obj.api_query("user_open_orders")

    #Основной цикл программы
    while True:
        if (float(user_info["balances"]["USD"]) < can_spend):
            bot.send_message("@buyingapples", "Give me apples! " + str(float(user_info["balances"]["USD"])) )
        else:
            #Покупка при удачном раскладе
            while True:
                avg_buy_price = buy_price(obj, current_pair)
                if (avg_buy_price != None):
                    buy_dict : dict = {"pair":current_pair,"quantity": float(can_spend/avg_buy_price),"price": avg_buy_price,"type":"buy"}
                    while True:
                        result : dict = obj.api_query("order_create" , buy_dict)
                        if (result["result"] == False):
                            time.sleep(120)
                            bot.send_message("@buyingapples", "Waiting for order_create to buy ...\n" )
                        else:
                            with open("log.txt", "w") as f:
                                f.write(str(avg_buy_price))
                            break
                    time.sleep(order_life_time*60)
                    if float(user_info["balances"]["BTC"]) == 0:
                        obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
                    else:
                        break
                else:
                    time.sleep(300)

            #Продажа при удачном раскладе
                sell_dict = {"pair":current_pair,"quantity": float(user_info["balances"]["BTC"]),"price": avg_buy_price + avg_buy_price*0.003,"type":"sell"}
                while True:
                    result : dict = obj.api_query("order_create" , sell_dict)
                    if (result["result"] == False):
                        time.sleep(120)
                        bot.send_message("@buyingapples", "Waiting for order_create to sell ...\n" )
                    else:
                        break
                time.sleep(order_life_time * 60)
                open_orders : dict = obj.api_query("user_open_orders")
                if len(open_orders) != 0:
                    sell_dict["price"] = sell_dict["price"] - sell_dict["price"]*0.001
                    while len(open_orders) != 0:
                        obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
                        while True:
                            result : dict = obj.api_query("order_create" , sell_dict)
                            if (result["result"] == False):
                                time.sleep(120)
                                bot.send_message("@buyingapples", "Waiting for order_create to sell ...\n" )
                            else:
                                break
                        open_orders : dict = obj.api_query("user_open_orders")
                user_info = obj.api_query("user_info")
                order_counter += 1
                bot.send_message("@buyingapples", "Current apples quantity: " + user_info["balances"]["USD"] + "\n" + "Sold buskets: " + str(order_counter))





        

try:
    trade(obj)
except :
    bot.send_message("@buyingapples", "Остановлен основной поток...\n")



