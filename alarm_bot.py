import json

import telegram
from datetime import datetime
import time
import asyncio
from db.PostgresDB import *


bot = telegram.Bot(token='1918476417:AAF99mfMy2lXJuknUemmiljlF8WVQfl4Kfc')

db = PostgresDB(user='lesha',
                password='lesha123',
                host='rc1b-zaqqd5xitiqlw9d1.mdb.yandexcloud.net',
                port="6432",
                database='ITMO_ALARM')


def get_schedule_for_day(day, row):
    if day == 0:
        return row.monday
    elif day == 1:
        return row.tuesday
    elif day == 2:
        return row.wednesday
    elif day == 3:
        return row.thursday
    elif day == 4:
        return row.friday
    elif day == 5:
        return row.saturday
    elif day == 6:
        return row.sunday


# with open('test_alarm.json', 'r', encoding='utf-8') as f:
    # data = json.load(f)
#
# db.put_week(data)
alarms = dict()
schedule_rows = db.find_schedule()
cur_weekday = datetime.weekday(datetime.now())
for row in schedule_rows:
    tg_id = db.find_user_by_id(row.id).tg_id
    min_class_num = 10
    for item in get_schedule_for_day(cur_weekday, row):
        if int(item['class_num']) < min_class_num:
            alarms[tg_id] = item['alarms']
            min_class_num = int(item['class_num'])

print(alarms)



# async def send_messages():
#     while True:
#         now = datetime.datetime.now()
#         if now.hour == hour and now.minute == minute:
#             for user in users:
#                 await bot.send_message(chat_id=user, text='Привет! Это сообщение от бота.')
#         await asyncio.sleep(1)
#
# asyncio.run(send_messages())

