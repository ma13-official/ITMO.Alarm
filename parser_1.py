import json
from bs4 import BeautifulSoup

# загрузить HTML-страницу
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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
        day = day_table.attrs['id']
    except:
        continue
    # найти все строки таблицы
    rows = day_table.find_all('tr')
    # пропустить первую строку (заголовок)
    for row in rows[1:]:
        # извлечь данные из столбцов
        try:
            time = row.find('td', {'class': 'time'}).text.strip()
            room = row.find('td', {'class': 'room'}).text.strip()
            lesson = row.find('td', {'class': 'lesson'}).text.strip()
            # создать словарь с данными
            item = {'day': day, 'time': time, 'room': room, 'lesson': lesson}
            # добавить словарь в список
            data.append(item)
        except:
            pass

# сохранить данные в JSON-файл
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
