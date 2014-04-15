#!/usr/bin/python
# -*- coding: utf-8 -*-

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pickle, os, gtk, string, sys
import readline
from Crypto.Cipher import AES
bd={}
path=os.getcwd()+os.sep+'.PassManBd' #Полный путь базы данных. По умолчанию будет создан в текущей директории, если хватит прав
path_key=os.getcwd()+os.sep+'.PassManKey' #Полный путь ключа шифрования. По умолчанию будет создан в текущей директории, если хватит прав

def inputF(key):
	'''Финкция добавляет в базу новую запись и записывает в файл'''
	print 'Добавление в базу. Введите новое имя:',
	name=raw_input()
	if name in bd:
		print 'Ошибка, такое имя уже существует, вы можете просмотреть все имена командой keys и удалить имя командой del',name
		main()
	print 'Введите логин:',
	login=raw_input()
	print 'Введите пароль:',
	passwd=raw_input()
	while len(passwd) < 16: passwd += '~' #Длина одного блока алгоритма AES равна 16 байт, забиваем мусором
	obj=AES.new(key, AES.MODE_ECB)
	ciphertext=obj.encrypt(passwd)
	t=login, ciphertext
	file=open(path,'w+')
	bd [name] = t
	pickle.dump(bd, file)
	file.close()
	print 'База данных успешно обновлена'
	return bd

def fandc(s,key):
	'''Функция ищет по ключу нужную информацию'''
	kortage=bd[s]
	passwd=kortage[1]
	obj2 = AES.new(key, AES.MODE_ECB)
	passwd=obj2.decrypt(passwd).strip("~") #Очищаем мусор, восстанавливая пароль
	clipboard = gtk.clipboard_get()
	clipboard.set_text(passwd)
	print 'Логин', kortage[0]
	print 'Пароль',passwd,'скопирован в буфер обмена'

def inputkey():
	'''Единожды вызываемая функция для генерации ключа шифрования и его сохранения на диске'''
	print 'Ключ по адресу: ',path_key,' не обнаружен!\nВведите пользовательский ключ для шифрования!\nОн может быть строго 16,24 или 32-ти байтовым\nКлюч: ',
	key=raw_input()
	if (len(key)!=16 and len(key)!=24 and len(key)!=32):
		print 'Ошибка. Длина равна: ',len(key)
		inputkey()
	file=open(path_key, 'w')
	file.write(key)
	file.close()
	print 'Секретный ключ записан по адресу: ',path_key,'\nХраните его, без него восстановить базу НЕВОЗМОЖНО!'

def delbd(s,bd):
	'''Удаление записи из базы'''
	del bd[s[4:(len(s))]]
	file=open(path,'w+')
	pickle.dump(bd, file)
	file.close()
	print 'Объект',s[4:(len(s))],'был удалён из базы'

def main():
	print 'Введите ключ для поиска:',
	try:
		s=raw_input();
		if s in bd: fandc(s, key)
		elif s=='': inputF(key) #Ввод пустой строки вызывает функцию добавления в базу
		elif s=='keys' :
			print 'В базе имеются следующие ключи:'
			for each in sorted(bd.keys()):
				print each+';',
				print
		elif s[0:3]=='del' and (s[4:(len(s))] in bd): delbd(s,bd) #Удаление записи из базы
		elif s:
			print 'Объект ',s,' в базе не найден'
			for ke in bd.keys():
				gg=string.find(ke,s,0,len(s)) #Пробуем найти подстроку в начале кажого из ключей базы
				if gg!=-1:
					print 'Возможно, вы имели ввиду: ',ke
					fandc(ke, key)
	except(EOFError):
		sys.exit("\nquiting")
	except(KeyboardInterrupt):
		sys.exit("\nhard quiting")
print 'Вас приветствует мастер паролей!\n',
m=1
try: #Блок обработки исключений
	file=open(path_key,'r')
	key=file.read()
	file.close()
except: 
	inputkey()
	file=open(path_key,'r')
	key=file.read()
	file.close()
try:
	file=open(path,'r')
	bd=pickle.load(file)
	file.close()
except:
	print 'Базы данных не существует!\nОна будет создана по адресу: ',path
	file=open(path,'w')
	file.write('')
	file.close()
if (os.path.getsize(path)) == 0: 
			print 'База данных пуста'	
			inputF(key)
while m==1: #Старт в бесконечном цикле основной функции
	main()
	
