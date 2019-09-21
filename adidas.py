import requests
from bs4 import BeautifulSoup as bs
import lxml
from Item import Item
import re
import time
import random

def GetAdidas():
    item_list = []
    headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    params : dict = {"sz" : "48","start" : "0"}
    Url : str = "https://www.adidas.ru/muzhchiny-obuv-krossovki%7Czimnie_krossovki-outlet"
    try:
        response = requests.get(Url,headers = headers)
    except:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    if response.status_code == 200:
        sp = bs(response.content ,"lxml")
        try:
            pages = int(re.findall("\d+",sp.find("li",attrs={"class":"paging-total"}).text)[0])
        except:
            with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " parsing error to " + Url + "\n")
            return item_list        
        params["start"] = random.randint(0,pages+1)*48
    else:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    try:
        request = requests.get(Url,headers = headers,params=params)
    except:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    if request.status_code == 200:
        soup = bs(request.content , "lxml")
        try:
            divs = soup.find_all("div" , attrs={"class":"product-tile"})
            if len(divs) == 0:
                raise ParsingError
        except:
            with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " parsing error to " + Url + "\n")
            return item_list
        for div in divs:
            try:
                a_element = div.findChildren("a" ,attrs = {"data-component":"productlist/ProductImage"})[0]
                name = a_element.get("data-productname")
            except :
                continue
            try:
                img_link = a_element.findChildren("img")[0].get("data-stackmobileview")
            except :
                continue
            try:
                link = "https://www.adidas.ru" + a_element.get("href")
            except:
                continue
            try:
                new_price = div.findChildren("span" , attrs = {"class":"salesprice discount-price"})[0].text.replace("\t","").replace("\r\n","")
            except:
                continue
            try:
                old_price = div.findChildren("span" , attrs = {"class":"baseprice"})[0].text.replace("\t","").replace("\r\n","")
            except:
                continue
            item_list.append(Item(name,link,img_link,old_price,new_price))
    else:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    done_list = []
    for i in range(10):
        if item_list != 0:
            done_list.append(item_list.pop(random.randint(0,len(item_list)-1)))
            return done_list
           else:
            return item_list
    


