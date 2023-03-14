import json
import traceback
import requests
import logging
from bs4 import BeautifulSoup


class HTMLParser():
    def __init__(self, number) -> None:
        logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                            format="%(asctime)s %(levelname)s %(message)s")
        html = self.get_html(number)
        json = self.parse_html(html)
        self.save_json(json)
        

    def get_html(self, number):
        url = 'https://itmo.ru/ru/schedule/0/'

        # URL страницы, которую нужно получить
        number_url = url + number + '/'

        # Отправляем запрос к сайту и получаем ответ
        response = requests.get(number_url)

        
        if response:
            logging.info(f'Connected to {number_url}')

        # Извлекаем HTML-код из ответа
        html = response.content

        return html


    def parse_html(self, html):
        # создать объект BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # найти таблицу с классом "rasp-tabl"
        # table = soup.find('table', {'class': 'rasp_tabl', 'id': False})

        # найти все таблицы с классом "rasp-tabl-day"
        day_tables = soup.find_all('table', {'class': 'rasp_tabl'})

        # создать список для хранения данных
        data = []

        # перебрать все таблицы
        for day_table in day_tables:
            try:
                day = day_table.find('th', {'class': 'day'}).find('span').text
            except:
                continue
            # найти все строки таблицы
            rows = day_table.find_all('tr')
            # пропустить первую строку (заголовок)
            for row in rows:
                # извлечь данные из столбцов
                try:
                    time_field = row.find('td', {'class': 'time'}).text.strip().split('\n')[:2]
                    room_field = row.find('td', {'class': 'room'}).text.strip().split('\n')
                    lesson_field = list(map(str.strip, row.find('td', {'class': 'lesson'}).text.strip().split('\n')))
                    # создать словарь с данными
                    time = time_field[0]
                    weeks = time_field[1]
                    type_week = lesson_field[0].split(')')[1]
                    room = room_field[0]
                    address = room_field[1]
                    lesson = lesson_field[0].split('(')[0]
                    type_lesson = lesson_field[0].split('(')[1].split(')')[0]  # достаем то, что в скобках
                    teacher = lesson_field[1]
                    item = {'day': day, 'time': time, 'weeks': weeks, 
                            'type_week': type_week, 'room': room, 
                            'address': address, 'lesson': lesson, 
                            'type_lesson': type_lesson, 'teacher': teacher}
                    # добавить словарь в список
                    data.append(item)
                except Exception as e:
                    pass

        logging.info('Parsed HTML to JSON.')
        return data

    def save_json(self, data):
        # сохранить данные в JSON-файл
        name = 'data.json'
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logging.info(f'JSON saved in {name}')

pars = HTMLParser('K32201')