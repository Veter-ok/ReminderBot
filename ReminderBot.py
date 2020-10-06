import telebot
from telebot import types
from datetime import datetime
from time import sleep
import os

TOKEN = os.environ.get('BOT_TOKEN') 
now = datetime.now()
now_data = str(now.day) + "." + str(now.month)
olimpiades = {"30.9" : "обществознанию", "12.10" : "истории", "13.10" : "технологии и итальянскому языку", "14.10" : "литературе",
              "16.10" : "географии", "19.10" : "праву", "22.10" : "математике", "26.10" : "экономике",
              "27.10" : "экономике", "28.10" : "исскуству", "29.10" : "информатике"}
bot = telebot.TeleBot(str(TOKEN))


@bot.message_handler(commands=['start'])
def start(message):
	#bot.send_message ( message.chat.id,"Бот запущен" )
	while True:
		olimpiad = cheackData()
		bot.send_message ( message.chat.id,"р" )
		if now.hour == 9 and olimpiad != None:
			bot.send_message ( message.chat.id,"Доброе утро, ребята!" )
			bot.send_message(message.chat.id, "Напоминаю, что сегодня проводится олимпиада по {}. Прошу отписаться тех, кто примет участие".format(cheackData()))
		elif now.hour == 17 and olimpiad != None:
			bot.send_message ( message.chat.id,"Добрый вечер, ребята! У выс есть ещё время, чтобы принять участие в олипиаде по {}".format (cheackData () ) )
			del olimpiades[olimpiad]
		sleep(10)


def cheackData():
	for data in olimpiades:
		if now_data == data:
			return olimpiades[data]


@bot.message_handler(content_types=['text'])
def lalala(message):
	#bot.send_message(message.chat.id, message.text)
	pass


bot.polling(none_stop=True)
