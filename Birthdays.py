from datetime import datetime

def DaysList():
	days = {"30.2" : "Айнышева Эрбола", "19.3" : "Волкову Сашу", "11.8" : "Воронкова Даниила", "23.1" : "Голополосову Дашу и Маслову Таню",
			"25.1" : "Долгова Глеба", "29.3" : "Калужских Максима", "7.9" : "Креневу Машу", "6.3" : "Лаврова Родиона",
			"5.2" : "Мальцева Илью", "6.5" : "Мамедову Лиану", "18.1" : "Орлова Егора и Сидоренко Настю",
			"5.7" : "Подрядова Степана", "5.4" : "Ранецкого Артёма", "6.1" : "Рябинину Лену", "9.9" : "Уразбаеву Адину",
			"25.11" : "Федина Сашу", "29.12" : "Николаеву Арину", "23.3" : "Веронику Васильевну", "23.6" : "Мухаметгалееву Валерию"}
	return days

def checkDay():
	now = datetime.now()
	days = DaysList()
	message = "Поздравляем, {} с Днём рождения! 🥳 🥳 🥳 🎂 🎂 🎂 "
	now_date = str(now.day) + "." + str(now.month)
	for date in days:
		if date == now_date:
			return message.format(days[date])
	return None

def BirthList():
	message_list = ""
	days = DaysList()
	for day in days:
		message_list += str(day) + " - " + str(days[day]) + "\n"
	return message_list
