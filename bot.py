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
from yoox import Yoox
from lamodaparse import Lamoda
from reebok import Reebok


TOKEN : str= "821455349:AAEPBbnU4hCsjcKpP3BbM2sxwsayTx_DMGg"
chat_id : str = ""


def GetClothing(message: Message):
        headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        item_list = []
        item_list.extend(GetEnd(Flag = False))
        item_list.extend(GetAsos(Flag = False))
        #item_list.extend(Lamoda())
        if len(item_list) == 0:
                with open("log.txt" , "a") as f:
                        f.write(str(time.ctime()) + " GLOBAL ERROR!!!\n")
                return None
        item = item_list.pop(random.randint(0,len(item_list)-1))
        image = requests.get(item.img_link, headers=headers)
        bot.send_photo(message.chat.id,image.content ,caption = item.info())
        item_list.clear()

def GetSneakers(message: Message):
        headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        item_list = []
        item_list.extend(GetEnd(Flag = True))
        item_list.extend(GetAdidas())
        item_list.extend(GetAsos(Flag = True))
        item_list.extend(Reebok())
        item_list.extend(Puma())
        if len(item_list) == 0:
                with open("log.txt" , "a") as f:
                        f.write(str(time.ctime()) + " GLOBAL ERROR!!!\n")
                return None
        item = item_list.pop(random.randint(0,len(item_list)-1))
        image = requests.get(item.img_link, headers=headers)
        bot.send_photo(message.chat.id,image.content ,caption = item.info())
        item_list.clear()
        



        
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands = ['start'])
def main(message: Message):
        if message.chat.id == "":
                pass
        else:
                pass
        if message.text == "/start":
                #schedule.every(3).seconds.do(GetSneakers,message)
                #schedule.every(8).seconds.do(GetClothing,message)
                schedule.every().day.at("13:00").do(GetSneakers,message)
                schedule.every().day.at("03:00").do(GetClothing,message)
                while True:
                        schedule.run_pending()
                        time.sleep(1)




bot.polling(True)