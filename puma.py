#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import requests
from bs4 import BeautifulSoup
import random
import time
from Item import Item
import lxml


BASE_URL = "https://ru.puma.com/skidki/dlja-muzhchin.html"










def get_html(url):
	try:
		response = requests.get(url)
	except:
		with open('log.txt', 'a') as f:
			f.write(time.ctime() + ' Connection error to ' + url + '\n')
			exit(0)
	return response.text



def parse(html):
	item_list = []
	try:
		soup = BeautifulSoup(html,"lxml")
		items = soup.find_all('div', class_ = 'grid__item image-sv01')
		items.extend(soup.find_all('div', class_ = 'grid__item image-mod01'))
		if (len(items) == 0):
			raise ParsingError
	except:
		with open('log.txt', 'a') as f:
			f.write(time.ctime() + ' Parsing error from ' + BASE_URL + '\n')
			exit(0)


	for item in items:
		try:
			name = item.find('a', class_ = 'product-item__name').text
		except:
			continue
		try:
			link = item.find('a', class_ = 'product-item__name').get('href')
		except:
			continue
		try:
			img_link = item.find('img').get('data-src')
		except:
			continue
		try:
			old_price = item.find('span', class_ = 'old-price sly-old-price no-display').find('span', class_ = 'price').text
		except:
			continue
		try:
			new_price = item.find('span', class_ = 'special-price').find('span', class_ = 'price').text
		except:
			continue
		product = Item(name, link, img_link, old_price, new_price)
		item_list.append(product)
	return item_list




def Puma():
	PAGE_URL = 'https://ru.puma.com/skidki/dlja-muzhchin/rasprodazha-obuvi.html'
	return parse(get_html(PAGE_URL))



if __name__ == '__main__':
	Puma()