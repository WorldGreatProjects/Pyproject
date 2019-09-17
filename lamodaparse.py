#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import requests
from bs4 import BeautifulSoup
import random
from Item import Item
import time
import lxml


BASE_URL = 'https://www.lamoda.ru'









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
		items = soup.find_all('a', class_='products-list-item__link link')
		if (len(items) == 0):
			raise ParsingError
	except:
		with open('log.txt', 'a') as f:
			f.write(time.ctime() + ' Parsing error from ' + BASE_URL + '\n')
			exit(0)


	for item in items:
		try:
			link = BASE_URL + item.get('href')
		except:
			continue
		try:
			category = item.find('span', class_='products-list-item__type').text 
			label = item.find('span', class_='products-list-item__brand-name').text
			name = category + ' ' + label
		except:
			continue
		try:
			old_price = item.find('span', class_='price__old').text
		except:
			continue
		try:
			new_price = item.find('span', class_='price__new').text
		except:
			continue
		try:
			img_link = 'https:' + item.find('img', class_='products-list-item__img').get('src')
		except:
			continue
		product = Item(name, link, img_link, old_price, new_price)
		item_list.append(product)
	return item_list







def Lamoda():
		page = random.randint(1,3)
		PAGE_URL = 'https://www.lamoda.ru/c/479/clothes-muzhskaya-verkhnyaya-odezhda/?is_sale=1&brands=1061%2C1163%2C25579%2C4035%2C28539%2C5172%2C4869%2C28208%2C25451%2C2037%2C1169%2C2003%2C27481%2C6158%2C5181%2C471%2C4351%2C5401%2C893%2C2047%2C23662%2C1107%2C1543%2C1063%2C18583%2C5706%2C5162%2C25889%2C573%2C4535%2C26934%2C25571%2C4978%2C18649%2C1787%2C25442&page='
		return parse(get_html(PAGE_URL + str(page)))






if __name__=='__main__':
	Lamoda()