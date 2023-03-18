import statistics
from datetime import datetime

from pony.orm import *

db = Database()

'''
Ниже указаны все сущности, которые нам нужно использовать
'''


class Schedule(db.Entity):
    id = PrimaryKey(int, nullable=False)
    monday = Optional(Json)
    tuesday = Optional(Json)
    wednesday = Optional(Json)
    thursday = Optional(Json)
    friday = Optional(Json)
    saturday = Optional(Json)
    sunday = Optional(Json)


class Alarm(db.Entity):
    id = PrimaryKey(int, auto=True)
    preparation_time = Required(str)
    road_time = Required(str)
    amount = Required(int)
    difficulty = Required(str)
    song = Required(str)
    intervals = Required(str)


"""
Класс, через который можно взаимодействовать с бд
"""


class PostgresDB:
    def __init__(self, user: str, password: str, host: str):
        db.bind(provider='postgres', user=f'{user}', password=f'{password}', host=f'{host}', port="6432",
                database='ITMO_ALARM')
        db.generate_mapping(create_tables=True)

    @db_session
    def add_new_week(self, json):
        Schedule(id=json['id'], monday=json['mon'], tuesday=json['tue'], wednesday=json['wen'], thursday=json['th'],
                 friday=json['fri'], saturday=json['sat'], sunday=json['sun'])

    @db_session
    def add_new_alarm(self, json):
        Alarm(preparation_time=json['prep_time'], road_time=json['road_time'], amount=json["amount"],
              difficulty=json["difficulty"], song=json["song"], intervals=json["intervals"])

    @db_session
    def find_schedule_by_id(self, id_user: int) -> Schedule:
        return get(s for s in Schedule if s.id == id_user)

    # пример как можно обратить к Schedule и получить время первой пары в понедельник:
    # Schedule.monday[0]["time"]
