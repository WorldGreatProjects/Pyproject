from Item import Item
import telebot
import schedule
import requests
import random
import time
from telebot.types import Message
from adidas import GetAdidas
from end import GetEnd
from asos import GetAsos
from puma import Puma
from lamodaparse import Lamoda
from reebok import Reebok


TOKEN : str= "821455349:AAEPBbnU4hCsjcKpP3BbM2sxwsayTx_DMGg"


def GetClothing():
        headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        item_list = []
        while len(item_list) == 0:
                i = random.randint(0,1)
                if i == 0:
                        item_list.extend(GetEnd(Flag = False))
                elif i == 1:
                        item_list.extend(GetAsos(Flag = False))
                # elif i == 2:    
                #         item_list.extend(Lamoda())
        if len(item_list) == 0:
                with open("log.txt" , "a") as f:
                        f.write(str(time.ctime()) + " GLOBAL ERROR!!!\n")
                return None
        item = item_list.pop(random.randint(0,len(item_list)-1))
        image = requests.get(item.img_link, headers=headers)
        bot.send_photo("@bigweargang",image.content ,caption = item.info())
        item_list.clear()

def GetSneakers():
        headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        item_list = []
        while len(item_list) == 0:
                i = random.randint(0,2)
                if i == 0:
                        item_list.extend(GetEnd(Flag = True))
                elif i == 2:
                        item_list.extend(GetAdidas())
                elif i == 1:    
                        item_list.extend(GetAsos(Flag = True))
                # elif i == 2:
                #         item_list.extend(Reebok())
                # elif i == 2:
                #         item_list.extend(Puma())
        if len(item_list) == 0:
                with open("log.txt" , "a") as f:
                        f.write(str(time.ctime()) + " GLOBAL ERROR!!!\n")
                return None
        item = item_list.pop(random.randint(0,len(item_list)-1))
        image = requests.get(item.img_link, headers=headers)
        bot.send_photo("@bigweargang",image.content ,caption = item.info())
        item_list.clear()
        



        
bot = telebot.TeleBot(TOKEN)

def main():
        schedule.every(8).seconds.do(GetSneakers)
        schedule.every(13).seconds.do(GetClothing)
        # schedule.every().day.at("13:00").do(GetSneakers)
        # schedule.every().day.at("03:00").do(GetClothing)
        while True:
                schedule.run_pending()
                time.sleep(1)

        
while True:
        main()
        bot.polling(True)
