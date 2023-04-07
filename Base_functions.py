from timetable_maker import *
from datetime import *
from copy import deepcopy


class Solver:

    def __init__(self, timetable_path: str):
        """
        :param timetable_path: название json файла с расписанием
        ОДНОГО конкретного пользователя (можно и поменять,
        чтобы я из бд доставал группу и потоки и сам
        формировал расписание для него, базара нет)
        """
        self.Today: date = date.today() # у этой штуки есть перспектива
        self.Timetable = self.input_timetable(timetable_path)
        self.Command = None
        self.Date = None
        self.Teacher = None

    def request_handler(self, text: str):
        """
        Функция преобразует полученный текст
        в формате *команда дата/период/препод*
        (примеры: "date 2023-03-28" - расписание на 28 марта 2023,
        "period 2023-03-01 2023-03-04" - с 1 по 4 марта 2023,
        "teacher Серебрянская 2023-04-01" -
        расписание Серебрянской на 1 апреля 2023)
        в атрибуты класса. Думаю, обрабатывать и преобразовывать
        текст стоит в файле dialogs как интенты,
        пока не представляю как это сделать здесь
        !!! позже подумаю насчет времени для поиска препода !!!
        """
        temp = text.split()
        if len(temp) > 1:
            self.Command = temp[0]
            if self.Command == 'date':
                self.Date = date.fromisoformat(temp[1])
            elif self.Command == 'period':
                self.Date = [date.fromisoformat(temp[1]), date.fromisoformat(temp[2])]
            elif self.Command == 'teacher':
                self.Teacher = temp[1]
                self.Date = date.fromisoformat(temp[2])

    def input_timetable(self, timetable_path: str):
        with open(timetable_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    def get_week_from_date(self, cur_date: date):
        starter = date(2023, 2, 6).toordinal()
        week_num = (cur_date.toordinal() - starter) // 7 + 1
        temp = cur_date.weekday()
        if temp == 0:
            week_day = 'Пн'
        elif temp == 1:
            week_day = 'Вт'
        elif temp == 2:
            week_day = 'Ср'
        elif temp == 3:
            week_day = 'Чт'
        elif temp == 4:
            week_day = 'Пт'
        elif temp == 5:
            week_day = 'Сб'
        else:
            week_day = 'Вс'
        return week_num, week_day

    def get_answer(self, text: str):
        self.request_handler(text)
        HTMLParser.save_json(self.output_data(), 'base_func_test.json')

    def output_data(self):
        if self.Command == 'date':
            return self.get_schedule_date(self.Date)
        elif self.Command == 'period':
            return self.get_schedule_period()
        elif self.Command == 'teacher':
            return self.where_is_teacher()
        else:
            return 'Извините, я вас не поняла'

    def get_schedule_date(self, cur_date: date):
        """
        фигня, но работает
        """
        week_num, week_day = self.get_week_from_date(cur_date)
        week_num = str(week_num)
        result = {'date': cur_date.isoformat(), 'weekday': week_day, 'classes': []}
        for example in self.Timetable:
            if example['day'] == week_day:
                weeks_list = list(example['weeks'].split(', '))
                if week_num in weeks_list:
                    temp = deepcopy(example)
                    temp.pop('day')
                    temp.pop('weeks')
                    temp.pop('type_week')
                    result['classes'].append(temp)
        return result

    def get_schedule_period(self):
        start_date = self.Date[0].toordinal()
        last_date = self.Date[1].toordinal()
        result = []
        for i in range(start_date, last_date+1):
            result.append(self.get_schedule_date(date.fromordinal(i)))
        return result

    def where_is_teacher(self):
        """
        Чота пока не придумал,
        надо фулл шедуле проверять
        """
        pass


tester = Solver('local_test.json')
tester.get_answer('period 2023-03-27 2023-04-02')
