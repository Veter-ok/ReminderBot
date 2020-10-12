import telebot
from telebot import types
from datetime import datetime
from time import sleep
import os

TOKEN = os.environ.get('BOT_TOKEN')
olimpiades = {"12.10" : "истории", "13.10" : "технологии и итальянскому языку", "14.10" : "литературе",
              "16.10" : "географии", "19.10" : "праву", "22.10" : "математике", "26.10" : "экономике",
              "27.10" : "экономике", "28.10" : "исскуству", "29.10" : "информатике"}
bot = telebot.TeleBot(str(TOKEN))


@bot.message_handler(commands=['start'])
def start(message):
	now = datetime.now()
	now_data = str(now.day) + "." + str(now.month)
	bot.send_message ( message.chat.id,"Бот запущен" )
	bot.send_message ( message.chat.id,str(now))
	sendLesson = False
	morning_message = False
	sendDate = None
	while True:
		olimpiad = cheackData()
		messageLesson = None
		now = datetime.now()
		now_data = str(now.day) + "." + str(now.month)
		if sendDate != now.day and sendLesson:
			sendLesson = False
		if now.hour == 9 and olimpiad != None and not morning_message:
			bot.send_message ( message.chat.id,"Доброе утро, ребята!" )
			bot.send_message(message.chat.id, "Напоминаю, что сегодня проводится олимпиада по {}. Прошу отписаться тех, кто примет участие".format(cheackData()))
			morning_message = True
		elif now.hour == 17 and morning_message:
			bot.send_message ( message.chat.id,"Добрый вечер, ребята! У выс есть ещё время, чтобы принять участие в олипиаде по {}".format (cheackData () ) )
			morning_message = False
			del olimpiades[olimpiad]
		if messageLesson != None and not sendLesson and (now.hour == 9 and now.minute <= 30):
			bot.send_message ( message.chat.id, messageLesson)
			sendLesson = True
			sendDate = now.day
		sleep(600)


def cheackData():
	for data in olimpiades:
		if now_data == data:
			return olimpiades[data]

		
def createMessage():
	now = datetime.now()
	all_parser = parser_links()
	links = all_parser[0]
	time = all_parser[1]
	message = "Что у вас сегодня:\n"
	index = 1
	for i in range(len(links)):
		date = str(now.month) + str(now.day)
		if date == links[i][0]:
			message += str(index) + ". " + str(time[i]) + " " + str(links[i][2][3:]) + "\n" + str(links[i][1][8:])+"\n"
			index += 1
	if index == 1:
		return None
	else:
		return str(message)


@bot.message_handler(content_types=['text'])
def lalala(message):
	#bot.send_message(message.chat.id, message.text)
	pass




bot.polling(none_stop=True)
