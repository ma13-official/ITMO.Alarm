import string

from pony.orm import *
from typing import Dict

db = Database()

'''
Ниже указаны все сущности, которые нам нужно использовать
'''


class FullSchedule(db.Entity):
    group = Optional("Group")
    schedule = Optional("Schedule")


class Group(db.Entity):
    number = PrimaryKey(str, auto=False)
    full_schedule = Optional("FullSchedule")
    user = Set("User")


class Schedule(db.Entity):
    monday = Optional(Json)
    tuesday = Optional(Json)
    wednesday = Optional(Json)
    thursday = Optional(Json)
    friday = Optional(Json)
    saturday = Optional(Json)
    sunday = Optional(Json)
    full_schedule = Optional("FullSchedule")


class User(db.Entity):
    yandex_id = Required(str, unique=True)
    group = Set("Group")


"""
Класс, через который можно взаимодействовать с бд
"""


class PostgresDB:
    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        db.bind(provider='postgres', user=f'{user}', password=f'{password}', host=f'{host}', port=f"{port}",
                database=f'{database}')
        db.generate_mapping(create_tables=True)

    # @db_session
    # def put_week(self, json):

    @db_session
    def add_schedule_and_user_and_group(self, json, yandex_id: str, number_group: str):
        user = self.add_user(yandex_id)
        group = self.add_group_and_user(number_group, user)
        schedule = Schedule(monday=json['mon'], tuesday=json['tue'], wednesday=json['wed'], thursday=json['th'],
                            friday=json['fri'], saturday=json['sat'], sunday=json['sun'])
        FullSchedule(group=group, schedule=schedule)

    @db_session
    def add_schedule_and_group(self, json, number_group: str):
        schedule = Schedule(monday=json['mon'], tuesday=json['tue'], wednesday=json['wed'], thursday=json['th'],
                            friday=json['fri'], saturday=json['sat'], sunday=json['sun'])
        group = self.get_group_by_number(number_group)
        FullSchedule(group=group, schedule=schedule)

    @db_session
    def get_schedule_by_group_number(self, group_name):
        schedule_id = FullSchedule.get(lambda f: f.group.number == group_name)
        if schedule_id is not None:
            schedule_id = schedule_id.schedule.id
        else:
            return None
        return Schedule.get(lambda s: s.id == schedule_id)

    @db_session
    def get_schedule_by_yandex_id(self, yandex_id) -> list:
        result = []
        groups = self.get_all_group_name_by_yandex_id(yandex_id)
        for group in groups:
            result.append(self.get_schedule_by_group_number(group.number))
        return result

    @db_session
    def add_group_and_user(self, number_group: str, user: User) -> Group:
        group = Group(number=number_group, user=user)
        return group

    @db_session
    def add_group(self, number_group: str, yandex_id: str):
        user = self.get_user_by_yandex_id(yandex_id)
        self.add_group_and_user(number_group, user)

    @db_session
    def get_group_by_number(self, number_group: str) -> Group:
        return Group.get(lambda g: g.number == number_group)

    @db_session
    def get_all_group_name_by_yandex_id(self, yandex_id: str) -> [Group]:
        return select(g for g in Group for u in g.user if u.yandex_id == yandex_id)[:]

    @db_session
    def add_user(self, yandex_id: str) -> User:
        user = User(yandex_id=yandex_id)
        return user

    @db_session
    def get_user_by_yandex_id(self, yandex_id: str) -> User:
        return User.get(lambda u: u.yandex_id == yandex_id)
