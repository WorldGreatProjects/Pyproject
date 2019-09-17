import requests
class Item:
    def __init__ (self, name = None, link = None, img_link = None, old_price = None, new_price = None):
        self.name = name
        self.link = link
        self.img_link = img_link
        self.old_price = old_price
        self.new_price = new_price

    def info (self):
        return  self.name + '\n\n' + requests.get("https://clck.ru/--?url=" + self.link).content.decode() + "\n"+ u'\U000026D4'*3 + " Старая цена: " + self.old_price  + "\n" + u'\U0001F525'*3 + " Новая цена: " + self.new_price + "\n"

    