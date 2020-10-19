import telebot
from datetime import datetime
from time import sleep
import os
import ParserLinks
import Birthdays

TOKEN = os.environ.get('BOT_TOKEN')
olimpiades = {"12.10" : "истории", "13.10" : "технологии и итальянскому языку", "14.10" : "литературе",
              "16.10" : "географии", "19.10" : "праву", "22.10" : "математике", "26.10" : "экономике и китайскому языку",
              "27.10" : "химии и испанскому языку", "28.10" : "исскуству", "29.10" : "информатике"}
bot = telebot.TeleBot(str(TOKEN))


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message ( message.chat.id,"Бот запущен" ) 
	while True:
		print("проверка событий" )
		now = datetime.now() # remember now date
		now_date = str(now.day) + "." + str(now.month) # remember now month and now day
		if now.hour == 6 and now.minute <= 25:
			olimpiad = cheackData() # check if there are olympiads now
			if olimpiad != None:
				bot.send_message(message.chat.id, "Напоминаю, что сегодня проводится олимпиада по {}. Прошу отписаться тех, кто примет участие".format(cheackData()))
		elif now.hour == 14 and now.minute <= 10:
			olimpiad = cheackData() # check if there are olympiads now
			if olimpiad != None:
				bot.send_message ( message.chat.id,"Добрый вечер, ребята! У вас есть ещё время, чтобы принять участие в олимпиаде по {}.".format (cheackData () ) )
				del olimpiades[now_date]
		#if now.hour == 6 and now.minute <= 10:
			#messageLesson = createMessage() 
			#if messageLesson != None:
				#bot.send_message ( message.chat.id, messageLesson)
		if now.hour == 6 and now.minute <= 10:
			birthdays = Birthdays.checkDay()
			if  birthdays != None:
				bot.send_message ( message.chat.id, str(birthdays))
		print("проверка событий завершена"  )
		sleep(600)


def cheackData():
	now = datetime.now()
	now_date = str(now.day) + "." + str(now.month)
	for data in olimpiades:
		if now_date == data:
			return olimpiades[data]
	return None

		
def createMessage():
	now = datetime.now()
	all_parser = ParserLinks.parser_links()
	links = all_parser[0]
	time = all_parser[1]
	message = "Что у вас сегодня:\n"
	index = 1
	for i in range(len(links)):
		date = str(now.month) + str(now.day)
		if date == links[i][0]:
			message += str(index) + ". " + str(time[i]) + " " + str(links[i][2]) + "\n" + str(links[i][1][8:])+"\n"
			index += 1
	if index == 1:
		return None
	else:
		return str(message)

	

@bot.message_handler(content_types=['text'])
def lalala(message):
	print("проверка сообщений"  )
	if message.text == "др.лист":
		bot.send_message(message.chat.id, Birthdays.BirthList())
	print("проверка сообщений завершена"  )


bot.infinity_polling(True)
