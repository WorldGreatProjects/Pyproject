import requests
from bs4 import BeautifulSoup as bs
import lxml
import time
import random
from Item import Item

def GetEnd(Flag : bool):
    if Flag == True:
       Url : str = "https://www.endclothing.com/row/sale/sneakers?brand=A%20Bathing%20Ape~Adidas~Adidas%20Consortium~Adidas%20Spezial~Adidas%20x%20Raf%20Simons~Alexander%20McQueen~Asics~Calvin%20Klein%20205W39NYC~Comme%20des%20Gar%C3%A7ons%20Play~Comme%20des%20Gar%C3%A7ons%20SHIRT~Converse~Diadora~ETQ.%20Amsterdam~Fred%20Perry%20Authentic~Givenchy~Gosha%20Rubchinskiy~Kenzo~Maison%20Margiela~McQ%20Alexander%20McQueen~Neighborhood~New%20Balance~Nike~Nike%20Jordan~Nike%20x%20Undercover%20Gyakusou~Off-White~PACCBET~Paul%20Smith~Polo%20Ralph%20Lauren~Puma~Reebok~Saint%20Laurent~Saucony~The%20North%20Face~Tommy%20Jeans~Vans~Vans%20Vault~Versace~Y-3" 
    else:
        Url : str = "https://www.endclothing.com/row/sale/sale-clothing"
    item_list = []

    params : dict = {"page" : "0"}
    headers : dict = { "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    params["page"] = random.randint(0,10)
    try:
        request = requests.get(Url,headers = headers,params=params)
    except:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    if request.status_code == 200:
        soup = bs(request.content , "lxml")
        try:
            divs = soup.find_all("div" , attrs={"class":"ProductList__ProductSC-sc-114chzc-3 fAXAhx"})
            if len(divs) == 0:
                raise ParsingError
        except:
            with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " parsing error from " + Url + "\n")
            return item_list
        for div in divs:
            try:
                NameSpan = div.findChildren("span", attrs = {"class":"ProductList__ProductNameSC-sc-114chzc-4 drGpFD"})
                name = NameSpan[0].get_text()
                if len(name) > 300:
                    continue
            except:
                continue                
            try:
                link = "https://www.endclothing.com" + NameSpan[0].findChildren("a" , recursive = False , href = True)[0]["href"]
            except:
                continue
            try:
                img_link = div.findChildren("img")[0]["src"]
            except:
                 continue
            try:
                old_price = div.findChildren("span", attrs = {"class":"ProductList__ProductPriceFullSC-sc-114chzc-8 gZjGtV ProductList__ProductPriceSC-sc-114chzc-6 etcLga"})[0].get_text()
                if len(old_price) > 100:
                    continue
            except:
                continue
            try:
                new_price = div.findChildren("span", attrs = {"class":"ProductList__ProductPriceSaleSC-sc-114chzc-9 gzRDAo ProductList__ProductPriceSC-sc-114chzc-6 etcLga"})[0].get_text()
                if len(new_price) > 100:
                    continue           
            except:
                continue
            item_list.append(Item(name , link, img_link, old_price, new_price ))
    else:
        with open("log.txt" , "a") as f:
                f.write(str(time.ctime()) + " Connection error to " + Url + "\n")
        return item_list
    done_list = []
    for i in range(10):
        done_list.append(item_list.pop(random.randint(0,len(item_list)-1)))
    return done_list

