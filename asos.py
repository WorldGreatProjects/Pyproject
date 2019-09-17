import requests
from bs4 import BeautifulSoup as bs
import lxml
import re
from Item import Item
import random
import time

def GetAsos(Flag : bool):
    if Flag == True:
        Url : str = "https://www.asos.com/ru/men/rasprodazha/tufli-i-sportivnaya-obuv/cat/?cid=1935&currentpricerange=390-16390&nlid=mw|%D0%B0%D1%83%D1%82%D0%BB%D0%B5%D1%82|%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C%20%D0%BF%D0%BE%20%D1%82%D0%B8%D0%BF%D1%83%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0&refine=attribute_1047:8606|brand:17,15723,18,16346,15565,12136,13688,298,105,14513,131,156,3060,2943,15139,12664,391,401,13073,499,2986,15176,13623,15177,589,2988,16284,3672,3029,765"
    else:
        Url : str = "https://www.asos.com/ru/men/autlet/cat/?cid=27396&currentpricerange=190-47290&nlid=mw|аутлет|сортировать%20по%20типу%20продукта&refine=attribute_10992:61380,61382,61377|attribute_1047:8405,8401,8407,8415,8391|brand:17,18,16346,15565,12111,12136,13688,298,15672,15955,15155,105,15488,12507,15926,3682,14513,15059,131,14990,13838,156,3180,14722,14116,3060,202,2943,14644,15139,12461,15591,14269,14508,391,12984,15497,396,401,15503,16033,13073,15127,499,3182,2986,15176,13623,15177,3115,14096,3309,3336,3594,589,13621,2988,16284,3312,3672,3029,15631,16099,15489,765,15233,3062"
    item_list = []
    params : dict = {"page":"0"}
    headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    try:
        response = requests.get(Url,headers = headers)
    except:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    if response.status_code == 200:
        sp = bs(response.content ,"lxml")
        try:
            pages = int(sp.find("progress" , attrs={"class":"_2hirsSG"}).get("max"))//72
            params["page"] = random.randint(0,pages)
        except:
            with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " parsing error to " + Url + "\n")
            return item_list        
    else:
            with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
            return item_list

    try:
        request = requests.get(Url, headers = headers, params=params)
    except:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    if request.status_code == 200:
        soup = bs(request.content , "lxml")
        try:
            ass = soup.find_all("a" , attrs={"class":"_3x-5VWa"})
            if len(ass) == 0:
                raise ParsingError
        except:
            with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " parsing error to " + Url + "\n")
            return item_list
        for a in ass:
            try:
                info = a.get("aria-label").split("," , maxsplit = 1)
            except:
                continue
            try:
                link = a.get("href")
            except:
                continue
            name = info[0]
            price = info[1].split(".")
            try:
                old_price = re.sub(", Начальная цена: ","",price[1])
            except:
                continue
            try:
                new_price = re.sub(" Текущая цена: ","",price[0])
            except:
                continue
            try:
                img_link ="http:" + a.findChildren("img" , attrs = {"data-auto-id":"productTileImage"})[0].get("src")
            except:
                continue
            item_list.append(Item(name,link,img_link,old_price,new_price))

    else:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    done_list = []
    for i in range(10):
        done_list.append(item_list.pop(random.randint(0,len(item_list)-1)))
    return done_list
