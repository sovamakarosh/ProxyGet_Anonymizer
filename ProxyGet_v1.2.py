#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import re
import subprocess
import requests
import cfscrape
from lxml import html, etree
from datetime import datetime
from PyQt5.QtWidgets import (QMessageBox, QWidget, QLabel, QLineEdit, QTableView, QGridLayout, QApplication, QPushButton, QAction, QComboBox, QCheckBox, QProgressBar, QMenu, QAction)
from PyQt5.QtGui import (QIcon, QStandardItemModel, QStandardItem, QCursor)
from PyQt5.QtCore import (Qt, QModelIndex)
 
class proxyGet(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		global menuRight
		global setAction 
		global viewTable
		global model
		global chCountry
		global prBar
		global chHttp
		global chHttps
		global chSocks4
		global chSocks5
		global chAnon1
		global chAnon2
		global chAnon3
		global chAnon4
		global titleHttp
		global viewHttp
		global titleHttps
		global viewHttps
		global titleFtp
		global viewFtp
		global titleSocks
		global viewSocks
		global chLocal
		global proxy_table
		proxy_table = []
		global proxy_reg
		proxy_reg = []
		
		titleType = QLabel('Тип прокси:')
		chHttp = QCheckBox('HTTP', self)
		chHttp.stateChanged.connect(lambda:self.checkState(chHttp))
		chHttp.toggle()
		chHttps = QCheckBox('HTTPS', self)
		chHttps.stateChanged.connect(lambda:self.checkState(chHttps))
		chHttps.toggle()
		chSocks4 = QCheckBox('Socks 4', self)
		chSocks4.stateChanged.connect(lambda:self.checkState(chSocks4))
		chSocks4.toggle()
		chSocks5 = QCheckBox('Socks 5', self)
		chSocks5.stateChanged.connect(lambda:self.checkState(chSocks5))
		chSocks5.toggle()
		titleAnon = QLabel('Анонимность:')
		chAnon1 = QCheckBox('Нет', self)
		chAnon1.stateChanged.connect(lambda:self.checkState(chAnon1))
		chAnon1.toggle()
		chAnon2 = QCheckBox('Низкая', self)
		chAnon2.stateChanged.connect(lambda:self.checkState(chAnon2))
		chAnon2.toggle()
		chAnon3 = QCheckBox('Средняя', self)
		chAnon3.stateChanged.connect(lambda:self.checkState(chAnon3))
		chAnon3.toggle()
		chAnon4 = QCheckBox('Высокая', self)
		chAnon4.stateChanged.connect(lambda:self.checkState(chAnon4))
		chAnon4.toggle()
		self.model = QStandardItemModel(self)
		viewTable = QTableView()
		viewTable.setModel(self.model)
		viewTable.horizontalHeader().setStretchLastSection(True)
		viewTable.setContextMenuPolicy(Qt.CustomContextMenu)
		viewTable.customContextMenuRequested.connect(self.openMenu)
		self.selectionModel = viewTable.selectionModel()
		titleCountry = QLabel('Страна:')
		chCountry = QComboBox()
		chCountry.addItems(['Россия', 'Бразилия', 'Канада', 'США', 'Франция', 'Германия', 'Италия', 'Тайланд', 'Африка', 'Нидерланды'])
		chCountry.currentIndexChanged[str].connect(self.checkCountry)
		chSpeed = QLineEdit('1500', self)
		chSpeed.setInputMask('00000 мс')
		chSpeed.setMaxLength(5)
		chSpeed.textChanged[str].connect(self.checkSpeed)
		prBar = QProgressBar(self)
		prBar.setAlignment(Qt.AlignCenter)
		
		titleHttp = QLabel('HTTP')
		viewHttp = QLineEdit(self)
		viewHttp.setPlaceholderText('Не используется')
		viewHttp.textChanged[str].connect(self.checkSetHttp)
		titleHttps = QLabel('HTTPS')
		viewHttps = QLineEdit(self)
		viewHttps.setPlaceholderText('Не используется')
		viewHttps.textChanged[str].connect(self.checkSetHttps)
		titleFtp = QLabel('FTP')
		viewFtp = QLineEdit(self)
		viewFtp.setPlaceholderText('Не используется')
		viewFtp.textChanged[str].connect(self.checkSetFtp)
		titleSocks = QLabel('SOCKS')
		viewSocks = QLineEdit(self)
		viewSocks.setPlaceholderText('Не используется')
		viewSocks.textChanged[str].connect(self.checkSetSocks)
		chLocal = QCheckBox('Не использовать прокси-сервер для локальных адресов', self)
		chLocal.stateChanged.connect(lambda:self.checkState(chLocal))
		chLocal.toggle()

		btnSearch = QPushButton('Поиск', self)
		btnExit = QPushButton('Выход', self)
		btnExit.clicked.connect(self.close)
		btnSearch.clicked.connect(self.buttonSearch)
		btnOnProxy = QPushButton('Применить', self)
		btnOnProxy.clicked.connect(self.buttonOnProxy)
		btnOffProxy = QPushButton('Отключить прокси', self)
		btnOffProxy.clicked.connect(self.buttonOffProxy)
		
		grid = QGridLayout()
		grid.setSpacing(5)
		grid.setRowMinimumHeight(0, 0)
		grid.setRowMinimumHeight(1, 15)
		grid.setRowMinimumHeight(2, 15)
		grid.setRowMinimumHeight(3, 15)
		grid.setRowMinimumHeight(4, 15)
		grid.setRowMinimumHeight(5, 15)
		grid.setColumnMinimumWidth(0, 90)
		grid.setColumnMinimumWidth(1, 90)
		grid.setColumnMinimumWidth(2, 90)
		grid.setColumnMinimumWidth(3, 90)
		grid.setColumnMinimumWidth(4, 90)
		grid.addWidget(titleType, 2, 0)
		grid.addWidget(chHttp, 2, 1)
		grid.addWidget(chHttps, 2, 2)
		grid.addWidget(chSocks4, 2, 3)
		grid.addWidget(chSocks5, 2, 4)
		grid.addWidget(titleAnon, 3, 0)
		grid.addWidget(chAnon1, 3, 1)
		grid.addWidget(chAnon2, 3, 2)
		grid.addWidget(chAnon3, 3, 3)
		grid.addWidget(chAnon4, 3, 4)
		grid.addWidget(btnSearch, 1, 3)
		grid.addWidget(btnExit, 1, 4)
		grid.addWidget(titleCountry, 1, 0)
		grid.addWidget(chCountry, 1, 1)
		grid.addWidget(chSpeed, 1, 2)
		grid.addWidget(prBar, 5, 0, 1, 5)
		grid.addWidget(viewTable, 6, 0, 10, 5)
		grid.addWidget(btnOnProxy, 17, 3, 4, 1)
		grid.addWidget(btnOffProxy, 17, 4, 4, 1)
		
		grid.addWidget(titleHttp, 17, 0)
		grid.addWidget(viewHttp, 17, 1, 1, 2)
		grid.addWidget(titleHttps, 18, 0)
		grid.addWidget(viewHttps, 18, 1, 1, 2)
		grid.addWidget(titleFtp, 19, 0)
		grid.addWidget(viewFtp, 19, 1, 1, 2)
		grid.addWidget(titleSocks, 20, 0)
		grid.addWidget(viewSocks, 20, 1, 1, 2)
		grid.addWidget(chLocal, 21, 0, 1, 4)
		
		self.setLayout(grid)
		self.setGeometry(100, 100, 350, 400)
		self.setWindowTitle('ProxyGet v1.2')
		self.setWindowIcon(QIcon('logo.png'))   
		self.show()
		
	def chErrors(self):
		reply = QMessageBox.question(self, 'Error', 'Нет соединения с сервером: попробуйте отключить прокси.', QMessageBox.Ok)
		
	def openMenu(self, position):
		menu = QMenu()
		addHttp = QAction('Установить как HTTP', menu)
		addHttp.triggered.connect(self.setHttp)
		menu.addAction(addHttp)
		addHttps = QAction('Установить как HTTPS', menu)
		addHttps.triggered.connect(self.setHttps)
		menu.addAction(addHttps)
		addFtp = QAction('Установить как FTP', menu)
		addFtp.triggered.connect(self.setFtp)
		menu.addAction(addFtp)
		addSocks = QAction('Установить как SOCKS', menu)
		addSocks.triggered.connect(self.setSocks)
		menu.addAction(addSocks)
		menu.exec_(viewTable.viewport().mapToGlobal(position))
		
	def getItem(self):
		global item
		item = 'None'
		indexes = self.selectionModel.selectedIndexes()
		for index in indexes:
			row = index.row()
			col = index.column()
			item = self.model.item(row, 0).text()
		return item
				
	def setHttp(self):
		global http
		self.getItem()
		viewHttp.setText(item)
		http = 'http=' + item
		i=0
		while True:
			try:
				if 'http=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break
		proxy_reg.append(http)

	def setHttps(self):
		global https
		self.getItem()
		viewHttps.setText(item)
		https = 'https=' + item
		i=0
		while True:
			try:
				if 'https=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break		
		proxy_reg.append(https)
		
		
	def setFtp(self):
		global ftp
		self.getItem()
		viewFtp.setText(item)
		ftp = 'ftp=' + item
		i=0
		while True:
			try:
				if 'ftp=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break
		proxy_reg.append(ftp)

	def setSocks(self):
		global socks
		self.getItem()
		viewSocks.setText(item)
		socks = 'socks=' + item
		i=0
		while True:
			try:
				if 'socks=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break
		proxy_reg.append(socks)
		
	def checkSetHttp(self, text):
		global http
		item = text
		http = 'http=' + item
		i=0
		while True:
			try:
				if 'http=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break		
		proxy_reg.append(http)
		
	def checkSetHttps(self, text):
		global https
		item = text
		https = 'https=' + item
		i=0
		while True:
			try:
				if 'https=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break		
		proxy_reg.append(https)
		
	def checkSetFtp(self, text):
		global ftp
		item = text
		ftp = 'ftp=' + item
		i=0
		while True:
			try:
				if 'ftp=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break		
		proxy_reg.append(ftp)
		
	def checkSetSocks(self, text):
		global socks
		item = text
		socks = 'socks=' + item
		i=0
		while True:
			try:
				if 'socks=' in proxy_reg[i]:
					del proxy_reg[i]
				i = i+1				
			except:
				break		
		proxy_reg.append(socks)
		
	def checkSpeed(self, text):
		global speed
		if len(text[0:-3]) < 1:
			text = '0 мс'
		speed = text[0:-3]

	def checkCountry(self, text): 
		global country
		if text == 'Россия':
			country = 'RU'
		elif text == 'США':
			country = 'US'
		elif text == 'Германия':
			country = 'DE'
		elif text == 'Италия':
			country = 'IT'
		elif text == 'Тайланд':
			country = 'TH'
		elif text == 'Бразилия':
			country = 'BR'
		elif text == 'Канада':
			country = 'CA'
		elif text == 'Франция':
			country = 'FR'
		elif text == 'Африка':
			country = 'ZA'
		elif text == 'Нидерланды':
			country = 'NL'
		return country
		
	def checkState(self, state):
		global typeHttp
		if state.text() == "HTTP" :
			if state.isChecked() == True:
				typeHttp = 'h'
			else:
				typeHttp = ''
		global typeHttps
		if state.text() == "HTTPS" :
			if state.isChecked() == True:
				typeHttps = 's'
			else:
				typeHttps = ''
		global typeSocks4
		if state.text() == "Socks 4" :
			if state.isChecked() == True:
				typeSocks4 = 's4'
			else:
				typeSocks4 = ''
		global typeSocks5
		if state.text() == "Socks 5" :
			if state.isChecked() == True:
				typeSocks5 = 's5'
			else:
				typeSocks5 = ''
		global anon1
		if state.text() == "Нет" :
			if state.isChecked() == True:
				anon1 = '1'
			else:
				anon1 = ''
		global anon2
		if state.text() == "Низкая" :
			if state.isChecked() == True:
				anon2 = '2'
			else:
				anon2 = ''
		global anon3
		if state.text() == "Средняя" :
			if state.isChecked() == True:
				anon3 = '3'
			else:
				anon3 = ''
		global anon4
		if state.text() == "Высокая" :
			if state.isChecked() == True:
				anon4 = '4'
			else:
				anon4 = ''
		global proxy_reg_local
		global proxy_reg_local_po
		if state.text() == "Не использовать прокси-сервер для локальных адресов" :
			if state.isChecked() == True:
				proxy_reg_local = '070000003C6C6F63616C3E'
				proxy_reg_local_po = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyOverride" /t "REG_SZ" /d "<local>" /f'
			else:
				proxy_reg_local = ''
				proxy_reg_local_po = 'Reg Delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyOverride" /f'

	def checkSetProxy(self, address): 
		global ip
		global ip_convert
		list_chars = []
		ip = address
		for char in ip:
			chars = '3'+char
			chars = re.sub('3\.','2E',chars)
			chars = re.sub('3:','3A',chars)
			chars = re.sub('3;','3B',chars)
			chars = re.sub('3=','3D',chars)
			chars = re.sub('3h','68',chars)
			chars = re.sub('3t','74',chars)
			chars = re.sub('3p','70',chars)
			chars = re.sub('3s','73',chars)
			chars = re.sub('3f','66',chars)
			chars = re.sub('3o','6F',chars)
			chars = re.sub('3c','63',chars)
			chars = re.sub('3k','6B',chars)
			chars = re.sub('3N','4E',chars)
			chars = re.sub('3n','6E',chars)
			chars = re.sub('3e','65',chars)
			list_chars.append(chars)
		ip_convert = ''.join(list_chars)
		return ip_convert
		
	def buttonOnProxy(self):
		sender = self.sender()
		ip_reg = ';'.join(proxy_reg)
		proxy_reg_mid = hex(len(ip_reg)).upper()[2:]
		self.checkSetProxy(ip_reg)
		ip_reg = ip_convert
		proxy_reg_on = '460000003E2E000003000000' + proxy_reg_mid + '000000'

		pe = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyEnable" /t "REG_DWORD" /d "0x00000001" /f'
		show_pe = subprocess.Popen(pe, shell = True)
		ps = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyServer" /t "REG_SZ" /d "' + ip + '" /f'
		show_ps = subprocess.Popen(ps, shell = True)
		po = proxy_reg_local_po
		show_po = subprocess.Popen(po, shell = True)
		dcs = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections" /v "DefaultConnectionSettings" /t "REG_BINARY" /d "' + proxy_reg_on + ip_reg + proxy_reg_local + '" /f'
		show_dcs = subprocess.Popen(dcs, shell = True)
		
	def buttonOffProxy(self):
		sender = self.sender()
		ip_reg = ';'.join(proxy_reg)
		proxy_reg_mid = hex(len(ip_reg)).upper()[2:]
		self.checkSetProxy(ip_reg)
		ip_reg = ip_convert
		proxy_reg_off = '460000003E2E000009000000' + proxy_reg_mid + '000000'

		pe = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyEnable" /t "REG_DWORD" /d "0x00000000" /f'
		show_pe = subprocess.Popen(pe, shell = True)
		ps = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyServer" /t "REG_SZ" /d "' + ip + '" /f'
		show_ps = subprocess.Popen(ps, shell = True)
		po = proxy_reg_local_po
		show_po = subprocess.Popen(po, shell = True)
		dcs = 'Reg Add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections" /v "DefaultConnectionSettings" /t "REG_BINARY" /d "' + proxy_reg_off + ip_reg + proxy_reg_local + '" /f'
		show_dcs = subprocess.Popen(dcs, shell = True)
		

	def buttonSearch(self):
		completed = 10
		self.model.clear()
		proxy_table.clear()
		time.sleep(1)
		try:
			global country
			print(country)
		except NameError:
			country = 'RU'
		completed = 30
		prBar.setValue(completed)
		time.sleep(1)
		try:
			global speed
			print(speed)
		except NameError:
			speed = '1500'
		completed = 80
		prBar.setValue(completed)
		time.sleep(1)
		
		self.parsing()
				
		for row in proxy_table:
			items = [
				QStandardItem(field)
				for field in row.split('#')
			]
			self.model.appendRow(items)
	
	def parsing(self):
		url = 'https://hidemy.name/ru/proxy-list/?country='+country+'&maxtime='+speed+'&type='+typeHttp+typeHttps+typeSocks4+typeSocks5+'&anon='+anon1+anon2+anon3+anon4+'#list'
		scraper = cfscrape.create_scraper()
		try:
			r = scraper.get(url)
		except :
			r = 'None'
		if r != 'None':
			parsing = str(r.text)
			parsing = re.sub('(?<=\<span).*?(?=\</span\>)', '', parsing)
			parsing = re.sub('\<span', '', parsing)
			parsing = re.sub('\</span\>', '', parsing)
			tree = html.fromstring(parsing)
			table = tree.xpath('//table[@class = "proxy__t"]')[0]
			tbody = tree.xpath('.//tbody')
			i=0
			while True:
				try:
					for tr in tbody:
						tr = tr.xpath('.//tr')[i]
						for td in tr:
							ip = tr.xpath('.//td')[0]
							port = tr.xpath('.//td')[1]
							prcountry = tr.xpath('.//div')[0]
							prspeed = tr.xpath('.//p')[0]
							prtype = tr.xpath('.//td')[4]
							pranon = tr.xpath('.//td')[5]
							lastcheck = tr.xpath('.//td')[6]
						proxy_table.append(str(ip.text) + ':' + str(port.text) + '#' + str(prtype.text) + '#' + str(prcountry.text) + '#' + str(pranon.text) + '#' + str(prspeed.text) + '#' + str(lastcheck.text))
						i = i+1
				except :
					break
			completed = 100
			prBar.setValue(completed)
		else:
			self.chErrors()
		completed = 0
		prBar.setValue(completed)
if __name__ == '__main__':
	app = QApplication(sys.argv)
	pg = proxyGet()
	sys.exit(app.exec_())