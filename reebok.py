#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import time
import requests
from bs4 import BeautifulSoup
import random
from Item import Item
import lxml
import re

BASE_URL = 'https://www.reebok.ru'









def get_html(url):
	try:
		response = requests.get(url)
	except:
		with open('log.txt', 'a') as f:
			f.write(time.ctime() + ' Connection error to ' + url + '\n')
			exit(0)
	return response.text






def page_number(html):
	soup = BeautifulSoup(html,"lxml")
	pages = soup.find('li', class_ = 'paging-total').text
	pages = pages.strip()
	pages = pages.split()[-1]
	return str(random.randint(0, int(pages)-1)*48) 





def parse(html):
	item_list = []
	try:
		soup = BeautifulSoup(html,"lxml")
		items = soup.find_all('div', class_ = 'product-tile')
		if (len(items) == 0):
			raise ParsingError
	except:
		with open('log.txt', 'a') as f:
			f.write(time.ctime() + ' Parsing error from ' + BASE_URL + '\n')
			exit(0)




	for item in items:
		try:
			name = item.find('span', class_ = 'title').text
		except:
			continue
		try:
			link = BASE_URL + item.find('div', class_ = 'product-info-inner-content clearfix with-badges').find('a').get('href')
		except:
			continue
		try:
			img_link = item.find('div', class_ = 'image plp-image-bg').find('img').get('data-original')
		except:
			continue
		try:
			old_price = re.sub("\n","",re.sub("\t","",item.find('span', class_ = 'baseprice').text))
		except:
			continue
		try:
			new_price = re.sub("\n","",re.sub("\t","",item.find('span', class_ = 'salesprice discount-price').text))
			
		except:
			continue
		product = Item(name, link, img_link, old_price, new_price)
		item_list.append(product)
		
	return item_list







def Reebok():
	PAGE_URL = 'https://www.reebok.ru/muzhchiny-obuv-classics-outlet?start=0'
	page = page_number(get_html(PAGE_URL))
	return parse(get_html(PAGE_URL[:len(PAGE_URL)-1]+page))



if __name__ == '__main__':
		Reebok()