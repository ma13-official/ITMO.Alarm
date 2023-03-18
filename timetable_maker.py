from html_parser import *
import json
import datetime


class Lesson:
    def __init__(self, class_data, class_num):
        self.time = class_data["time"]
        self.weeks = class_data["weeks"]
        self.type_week = class_data["type_week"]
        self.room = class_data["room"]
        self.address = class_data["address"]
        self.lesson = class_data["lesson"]
        self.type_lesson = class_data["type_lesson"]
        self.teacher = class_data["teacher"]
        self.lesson_format = class_data["lesson_format"]
        self.num = class_num
        class_data.pop('day')
        class_data.pop('weeks')
        class_data['class_num'] = str(class_num)
        self.data = class_data


class Day:
    def __init__(self, day_data):
        self.day_num = day_data
        self.classes = {}

    def add_class(self, day_data):
        time = day_data['time']
        if time == "08:20-09:50":
            self.classes['1'] = Lesson(day_data, "1")
        elif time == "10:00-11:30":
            self.classes['2'] = Lesson(day_data, "2")
        elif time == "11:40-13:10":
            self.classes['3'] = Lesson(day_data, "3")
        elif time == "13:30-15:00":
            self.classes['4'] = Lesson(day_data, "4")
        elif time == "15:20-16:50":
            self.classes['5'] = Lesson(day_data, "5")
        elif time == "17:00-18:30":
            self.classes['6'] = Lesson(day_data, "6")
        else:
            self.classes[time] = Lesson(day_data, time)


class TimeTable:
    def __init__(self, number, week_num):
        # HTMLParserInterface.get_schedule_n(number)
        self.data = self.input_data()
        self.week = self.create_week(week_num)

    def input_data(self):
        path = 'json_templates/test1.json'
        with open(path, 'r', encoding='utf-8') as f:
            self.data = json.loads(f.read())
        return self.data

    def create_week(self, week_num):
        week = {'mon': Day('mon'), 'tue': Day('tue'), 'wen': Day('wen'), 'th': Day('th'), 'fri': Day('fri'),
                'sat': Day('sat'), 'sun': Day('sun')}
        for i in self.data:
            weeks = i['weeks'].replace(' ', '').split(',')
            if str(week_num) in weeks:
                week[i['day']].add_class(i)
        return week

    def output_data(self):
        output = {'id': 123}
        for key, value in self.week.items():
            lessons = []
            for lesson in value.classes.keys():
                lessons.append(value.classes[lesson].data)
            output[value.day_num] = lessons
        HTMLParser.save_json(output, 'test.json')


test = TimeTable("K32201", 6)
test.input_data()
test.output_data()
