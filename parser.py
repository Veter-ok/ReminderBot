import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

URL = "https://calendar.google.com/calendar/u/0/htmlembed?height=1200&wkst=1&bgcolor=%23ffffff&ctz=Europe/Moscow&src=c3JqOWdvcHRmdG9rNGc4aWhlZDExYmVoNnNAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%230B8043&showNav=1&showPrint=0&showTabs=0&showCalendars=0&mode=AGENDA&pli=1"

HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}


def get_html(url):
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


def parser():
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


def createMessage():
	now = datetime.now()
	all_parser = parser()
	links = all_parser[0]
	time = all_parser[1]
	message = "Что у вас сегодня:\n"
	index = 1
	for i in range(len(links)):
		date = str(now.month) + str(now.day)
		if date == links[i][0]:
			message += str(index) + ". " + str(time[i]) + " " + str(links[i][2][3:]) + "\n" + str(links[i][1][8:])+"\n"
			index += 1 
	return message

print(createMessage())
