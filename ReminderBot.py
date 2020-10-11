import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
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
morning_message = False


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message ( message.chat.id,"Бот запущен" )
	sendLesson = False
	sendDate = None
	while True:
		olimpiad = cheackData()
		messageLesson = createMessage()
		now = datetime.now()
		now_data = str(now.day) + "." + str(now.month)
		if sendDate != now.day and sendDate != None:
			sendDate = now.day
			sendLesson = False
		if messageLesson != None and not sendLesson:
			bot.send_message ( message.chat.id, messageLesson)
			sendLesson = True
			sendDate = now.day
		if now.hour == 9 and olimpiad != None and not morning_message:
			bot.send_message ( message.chat.id,"Доброе утро, ребята!" )
			bot.send_message(message.chat.id, "Напоминаю, что сегодня проводится олимпиада по {}. Прошу отписаться тех, кто примет участие".format(cheackData()))
			morning_message = True
		elif now.hour == 17 and olimpiad != None:
			bot.send_message ( message.chat.id,"Добрый вечер, ребята! У выс есть ещё время, чтобы принять участие в олипиаде по {}".format (cheackData () ) )
			morning_message = False
			del olimpiades[olimpiad]
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


def get_html(url):
	HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
	html = requests.get(url, headers=HEADERS)
	return html

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	all_events = soup.find_all("td", class_ = "event-eventInfo")
	all_time_events = soup.find_all("td", class_="event-time")
	all_links_events = soup.find_all("a", class_="event-link")
	event_time = []
	link_events = []
	for i in range(0, len(all_events)):
		if all_events[i].text[:3] == "8-1":
			link_events.append(all_links_events[i].get('href'))
			event_time.append(all_time_events[i].text)
	last_links = get_last_content_links(link_events)
	event_time = event_time[:len(last_links)]
	return last_links, event_time


def parser_links():
	URL = "https://calendar.google.com/calendar/u/0/htmlembed?height=1200&wkst=1&bgcolor=%23ffffff&ctz=Europe/Moscow&src=c3JqOWdvcHRmdG9rNGc4aWhlZDExYmVoNnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%230B8043&showNav=1&showPrint=0&showTabs=0&showCalendars=0&mode=AGENDA&pli=1"
	html = get_html(URL)
	if html.status_code == 200:
		return get_content(html.text)
	else:
		return None

def get_last_content_links(links):
	last_links = []
	for link in links:
		html = get_html("https://calendar.google.com/calendar/u/0/{}".format(link))
		if html.status_code == 200:
			i = get_last_links(html.text)
			if i != None:
				last_links.append(i)
		else:
			return None
	return last_links


def get_last_links(html):
	soup = BeautifulSoup(html, "html.parser")
	date = str(soup.find_all("time")[1].get("datetime"))[4:8]
	if int(date[:2]) == 10 and int(date[2:]) <= 18:
		link = soup.find_all("a")[-1].get('href')
		title = soup.find("title").text
		return [date, link, title]
	else:
		return None



@bot.message_handler(content_types=['text'])
def lalala(message):
	#bot.send_message(message.chat.id, message.text)
	pass




bot.polling(none_stop=True)
