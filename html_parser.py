import json
import sys
import threading
import requests
import logging
from bs4 import BeautifulSoup
from time import perf_counter as pc
import time
from datetime import datetime


class HTMLParser:
    # def __init__(number) -> None:
    # logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
    #                     format="%(asctime)s %(levelname)s %(message)s")
    # html = HTMLParser.get_html(number)
    # json = HTMLParser.parse_html(html)
    # HTMLParser.save_json(json)

    @staticmethod
    def create_url(request, teacher_surname_or_not=False):
        # URL страницы, которую нужно получить
        url = f'https://itmo.ru/ru/schedule/{int(teacher_surname_or_not)}/{request}/'

        return url

    @staticmethod
    def get_html(url):
        # Отправляем запрос к сайту и получаем ответ
        response = requests.get(url)

        if not response:
            logging.error(f'NOT connected to {url}!!!')
            input()

        # Извлекаем HTML-код из ответа
        html = response.content

        return html

    @staticmethod
    def get_teacher_schedule_html(html):
        # создать объект BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        all_a = soup.find_all('a', {'href': True})
        for a in all_a:
            if a.get('href').startswith('/ru/schedule/3'):
                end_url = a.get('href').split('/ru/schedule/')[1]

        url = f'https://itmo.ru/ru/schedule/{end_url}'

        return HTMLParser.get_html(url)

    @staticmethod
    def check_html(html):
        check = BeautifulSoup(html, 'html.parser').find('article', {'class': 'content_block'})
        return 'Расписание не найдено' in check.text

    @staticmethod
    def get_day_tables(html):
        # создать объект BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # найти все таблицы с классом "rasp-tabl-day"
        day_tables = soup.find_all('table', {'class': 'rasp_tabl'})

        schedule_week = soup.find('h2', {'class': 'schedule-week'})
        if schedule_week is not None:
            cur_week = ''.join(
                filter(str.isdigit, schedule_week.text.split('.')[1]))  # оставить только номер текущей недели
        else:
            cur_week = ''

        return day_tables, cur_week

    @staticmethod
    def day_tables_work(day_tables, teacher_schedule_check=False, number='', teacher=''):
        # создать список для хранения данных
        data = []

        # перебрать все таблицы
        for day_table in day_tables:
            # print(day_table)
            try:
                day = day_table.find('th', {'class': 'day'}).find('span').text
            except:
                continue
            # найти все строки таблицы
            rows = day_table.find_all('tr')
            rows = day_table.find_all('tbody') + rows
            # print(rows)

            for row in rows:
                # извлечь данные из столбцов
                if row.text == '':
                    continue

                time_field = row.find('td', {'class': 'time'})
                if time_field is not None:
                    time_field_parsed = time_field.text.strip().split('\n')[:2]
                else:
                    time_field_parsed = ['', '']

                room_field = row.find('td', {'class': 'room'})
                if room_field is not None:
                    room_field_parsed = room_field.text.strip().split('\n')
                    if len(room_field_parsed) == 1:
                        try:
                            if room_field_parsed[0][0].isdigit():
                                room_field_parsed.append('')
                            else:
                                room_field_parsed = [''] + room_field_parsed
                        except:
                            room_field_parsed = ['', '']
                else:
                    room_field_parsed = ['', '']

                lesson_field = row.find('td', {'class': 'lesson'})
                if lesson_field is not None:
                    lesson_field_parsed = list(map(str.strip, lesson_field.text.strip().split('\n')))
                else:
                    lesson_field_parsed = ['()', '']

                lesson_format = row.find('td', {'class': 'lesson-format'})
                if lesson_format is not None:
                    lesson_format_parsed = lesson_format.text.strip()
                else:
                    lesson_format_parsed = ''

                if teacher_schedule_check:
                    group = row.find('td', {'class': False}).text.strip()
                    if group != number:
                        continue

                # создать словарь с данными
                time = time_field_parsed[0].strip()
                weeks = time_field_parsed[1].strip()
                type_week = lesson_field_parsed[0].split(')')[1].strip()
                room = room_field_parsed[0].strip()
                address = room_field_parsed[1].strip()
                lesson = lesson_field_parsed[0].split('(')[0].strip()
                type_lesson = lesson_field_parsed[0].split('(')[1].split(')')[0].strip()  # достаем то, что в скобках
                if not teacher_schedule_check:
                    teacher = lesson_field_parsed[1].strip()

                item = {'day': day, 'time': time, 'weeks': weeks, 'type_week': type_week, 'room': room,
                        'address': address, 'lesson': lesson, 'type_lesson': type_lesson, 'teacher': teacher,
                        'lesson_format': lesson_format_parsed}

                # добавить словарь в список
                data.append(item)
                pass

        logging.info('Parsed HTML to JSON.')
        return list({tuple(d.items()): d for d in data}.values())

    @staticmethod
    def check_number(day_tables, number):
        count = 0
        # перебрать все таблицы
        for day_table in day_tables:
            # print(day_table)
            try:
                day = day_table.find('th', {'class': 'day'}).find('span').text
            except:
                continue
            # найти все строки таблицы
            rows = day_table.find_all('tr')
            rows = day_table.find_all('tbody') + rows
            # print(rows)

            for row in rows:
                row_find = row.find('td', {'class': False})
                if row_find is not None:
                    group = row_find.text.strip()
                    if group != number:
                        continue
                    else:
                        count += 1

        return count == 0

    @staticmethod
    def save_json(data, name):

        # сохранить данные в JSON-файл
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logging.info(f'JSON saved in {name}')


class HTMLParserInterface(HTMLParser):
    @classmethod
    def get_schedule_tn(cls, teacher, number):
        """
        Возвращает информацию по расписанию по преподавателю и номеру группы(потока).

        Args:
            teacher (_type_): ФИО учителя(предпочтительно)
            number (_type_): номер группы(потока)
        """

        url = cls.create_url(teacher, True)
        html = cls.get_html(url)
        schedule_html = cls.get_teacher_schedule_html(html)
        day_tables, cur_week_number = cls.get_day_tables(schedule_html)
        # print(day_tables)
        data = cls.day_tables_work(day_tables, True, number, teacher)
        # print(data)
        # data = [f'Пример запроса с параметрами {teacher} и {number}'] + data
        return data
        # name = 'data_tn.json'
        # cls.save_json(data, name)

    @classmethod
    def get_schedule_n(cls, number):
        url = cls.create_url(number)
        # print(url)
        html = cls.get_html(url)
        # print(html)
        day_tables, cur_week_number = cls.get_day_tables(html)

        data = cls.day_tables_work(day_tables)

        # data = [f'Пример запроса с параметром {number}', f'Номер текущей недели: {cur_week_number}'] + data
        return data
        # name = 'data_n.json'
        # cls.save_json(data, name)

    @classmethod
    def create_schedule(cls):
        teacher = ''
        study_group = cls.get_input('номер учебной группы')
        data = cls.get_schedule_n(study_group)
        while teacher != 'stop':
            teacher = cls.get_input('ФИО преподавателя')
            if teacher == 'stop':
                break
            number = cls.get_input('поток', teacher)
            data += cls.get_schedule_tn(teacher, number)
        cls.save_json(data, 'test1.json')

    @classmethod
    def get_input(cls, template, teacher=''):
        if template == 'номер учебной группы':
            study_group = input(f'Введите {template}')

            url = cls.create_url(study_group)
            html = cls.get_html(url)

            if cls.check_html(html):
                print(f'Неверный {template}')
                cls.get_input(template)
            else:
                return study_group

        elif template == 'поток':
            number = input(f'Введите {template}')
            if teacher == 'stop':
                return 'stop'

            url = cls.create_url(teacher, True)
            html = cls.get_html(url)
            schedule_html = cls.get_teacher_schedule_html(html)
            day_tables, cur_week_number = cls.get_day_tables(schedule_html)

            if cls.check_number(day_tables, number):
                print(f'Неверный {template}')
                cls.get_input(template)
            else:
                return number

        elif template == 'ФИО преподавателя':
            teacher = input(f'Введите {template}')
            if teacher == 'stop':
                return 'stop'

            url = cls.create_url(teacher, True)
            html = cls.get_html(url)
            schedule_html = cls.get_teacher_schedule_html(html)

            if cls.check_html(schedule_html):
                print('Нет преподавателя с таким ФИО')
                cls.get_input(template)
            else:
                return teacher


# HTMLParser_Interface.get_schedule_tn('Калинникова', 'АЯ-B1.2/13')
# HTMLParserInterface.create_schedule()

class FullScheduleParser:
    aaa = 111

    @classmethod
    def parser(cls, arr, aaa):
        for i in arr:
            url = f'https://itmo.ru/ru/schedule/3/{i}/'
            html = HTMLParser.get_html(url)
            if not HTMLParser.check_html(html):
                logging.warning(f'{i}    {pc() - cls.start}')
                cls.teachers_id.append(i)
            else:
                logging.info(f'{i}    {pc() - cls.start}')
            if i % 50 == 0:
                print(f'{i}    {pc() - cls.start}')

    @classmethod
    def threads(cls, i):
        threads = []
        for x in range(len(i)):
            t = threading.Thread(target=cls.parser, args=(i[x], cls.aaa))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    @classmethod
    def starter(cls):
        cls.start = pc()
        now = datetime.now()
        date = now.date()
        time = str(now.time())[:2] + str(now.time())[3:5]
        logging.basicConfig(level=logging.INFO, filename=f"logs/{date}_{time}.log", filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")

        with open('for_full_schedule/teachers_id.json', 'r') as f:
            cls.teachers_id = json.load(f)

        # with open('for_full_schedule/for_check.json', 'r') as f:
        #     cls.for_check = json.load(f)
        for_check = list(range(135000, 200000))
        for_check_parts = cls.splitter(for_check, 13)
        checked = list(range(100000, 135000))
        for part in for_check_parts:
            cls.threads(cls.splitter(part, 4))
            with open('for_full_schedule/teachers_id.json', 'w') as f:
                json.dump(cls.teachers_id, f, indent=4)

            checked += part
            with open('for_full_schedule/checked.json', 'w') as f:
                json.dump(checked, f, indent=4)

    @staticmethod
    def splitter(arr, n):
        # Determine the size of each sub-array
        subarray_size = len(arr) // n

        # Create an empty list to hold the sub-arrays
        subarrays = []

        # Iterate through the original array and extract sub-arrays
        for i in range(0, len(arr), subarray_size):
            subarrays.append(arr[i:i + subarray_size])

        # Print the resulting sub-arrays
        return subarrays

# while True:
#     try:
FullScheduleParser().starter()
    # except KeyboardInterrupt:
    #     break
    # except Exception as e:
    #     logging.error(str(e))
    #     pass


# teachers_id = []
# for_check = []
# for i in r:
#     if i[1]:
#         teachers_id.append(i[0])
#     else:
#         for_check.append(i[0])
#


# with open('for_full_schedule/teachers_id.json', 'r') as f:
#     teachers_id = json.load(f)
#
# with open('for_full_schedule/teachers_id1.json', 'r') as f1:
#     teachers_id += json.load(f1)

# with open('for_full_schedule/for_check.json', 'r') as f:
#     for_check = json.load(f)
#
# with open('for_full_schedule/for_check1.json', 'r') as f:
#     for_check1 = json.load(f)

# teachers_id = sorted(list(set(teachers_id)))
# out = []
# for i in for_check:
#     if i in for_check1:
#         out.append(i)

# for_check = sorted(list(set(for_check)))
#
# with open('for_full_schedule/teachers_id.json', 'w') as f:
#     json.dump(teachers_id, f, indent=4)

# with open('for_full_schedule/for_check.json', 'w') as f:
#     json.dump(out, f, indent=4)