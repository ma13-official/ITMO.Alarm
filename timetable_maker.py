from html_parser import *
import json
import datetime

class Class:
    def __init__(self, class_data, class_num):
        self.time = class_data['time']
        self.teacher = class_data['teacher']
        self.type = class_data['type_lesson']
        self.place = class_data['address']
        self.name = class_data['lesson']
        self.num = class_num

class Day:
    def __init__(self, day_data):
        self.day_num = day_data
        self.classes = {}

    def add_class(self, day_data):
        match day_data['time']:
            case "08:20-09:50":
                self.classes['1'] = Class(day_data, "1")
            case "10:00-11:30":
                self.classes['2'] = Class(day_data, "2")
            case "11:40-13:10":
                self.classes['3'] = Class(day_data, "3")
            case "13:30-15:00":
                self.classes['4'] = Class(day_data, "4")
            case "15:20-16:50":
                self.classes['5'] = Class(day_data, "5")
            case "17:00-18:30":
                self.classes['6'] = Class(day_data, "6")
            case _:
                self.classes[day_data['time']] = Class(day_data, day_data['time'])

class TimeTable:
    def __init__(self, number, week_num):
        HTMLParser_Interface.get_schedule_n(number)
        self.data = self.input_data()
        self.week = self.create_week(week_num)

    def input_data(self):
        path = 'data_n.json'
        with open(path, 'r', encoding='utf-8') as f:
            self.data = json.loads(f.read())
        return self.data

    def create_week(self, week_num):
        week = {'Пн' : Day('Пн'), 'Вт': Day('Вт'), 'Ср': Day('Ср'), 'Чт': Day('Чт'), 'Пт': Day('Пт'), 'Сб': Day('Сб'), 'Вс': Day('Вс')}
        for i in self.data:
            weeks = i['weeks'].replace(' ', '').split(',')
            if str(week_num) in weeks:
                week[i['day']].add_class(i)
        return week

    def output_data(self):
        for k in self.week.keys():
            print(self.week[k].day_num)
            s = self.week[k]
            for lesson in s.classes.keys():
                print(s.classes[lesson].time, s.classes[lesson].name)


tets = TimeTable("K32201", 6)
tets.input_data()
tets.output_data()

