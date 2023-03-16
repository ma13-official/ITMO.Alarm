import json
from timetable_maker import *
from abc import ABCMeta, abstractmethod
from html_parser import *


class Alarm:
    def __init__(self, prep_time, road_time, amount, difficulty, song_name, interval):
        self.person_data = {"prep_time": str(prep_time), "road_time": str(road_time), "amount": str(amount), "difficulty": str(difficulty), "song": str(song_name), "intervals": str(interval)}
        self.data = self.data_input()
        self.week = self.alaram_week()
        self.alarms = self.create_alarms()

    def data_input(self):
        path = "test.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    @abstractmethod
    def personal_data1(self):
        pass

    def create_alarms(self):
        alarms = {}
        for key in self.week.keys():
            all_alarms = []
            day = []
            for lesson in self.week[key]:
                temp = lesson['time'].split("-")
                first_alarm_time = self.time_thing(temp[0])
                all_alarms = self.make_several_alarms(first_alarm_time)
                temp = lesson.copy()
                temp["alarms"] = all_alarms
                day.append(temp)
            alarms[key] = day
        return alarms



    def time_thing(self, time1):
        temp1 = time1.split(':')
        temp2 = self.person_data['prep_time'].split(':')
        mins1 = int(temp1[0])*60 + int(temp1[1])
        mins2 = int(temp2[0])*60 + int(temp2[1])
        res_min = mins1 - mins2
        hours = res_min//60
        mins = res_min%60
        res = res = self.time_format(hours, mins)
        return res


    def time_thing_copy(self, time1):
        temp1 = time1.split(':')
        temp2 = self.person_data['intervals'].split(':')
        mins1 = int(temp1[0]) * 60 + int(temp1[1])
        mins2 = int(temp2[0]) * 60 + int(temp2[1])
        res_min = mins1 + mins2
        hours = res_min // 60
        mins = res_min % 60
        res = self.time_format(hours, mins)
        return res

    def make_several_alarms(self, start_time):
        alarms = []
        alarms.append(start_time)
        for i in range(0, int(self.person_data['amount'])):
            next_alarm = self.time_thing_copy(start_time)
            alarms.append(next_alarm)
            start_time = next_alarm
        return alarms


    def time_format(self, hours, mins):
        mins_s = None
        hours_s = None
        if mins < 10:
            mins_s = '0' + str(mins)
        else:
            mins_s = str(mins)
        if hours < 10:
            hours_s = '0' + str(hours)
        else:
            hours_s = str(hours)
        res = str(hours_s) + ":" + str(mins_s)
        return res


    def alaram_week(self):
        week = {}
        for key in self.data.keys():
            if key == "id":
                continue
            day = []
            for lesson in self.data[key]:
                day.append(lesson)
            week[key] = day
        return week

    def dump_json(self, name):
        # сохранить данные в JSON-файл
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(self.alarms, f, indent=4, ensure_ascii=False)

        logging.info(f'JSON saved in {name}')



test = Alarm(prep_time="01:00", road_time="00:30", amount="3", difficulty="0", song_name="Daruda-Sandstorm", interval="00:10")
test.dump_json("test_alarm.json")
