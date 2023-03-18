from pony.orm import *

db = Database()

'''
Ниже указаны все сущности, которые нам нужно использовать
'''


class Schedule(db.Entity):
    monday = Optional(Json)
    tuesday = Optional(Json)
    wednesday = Optional(Json)
    thursday = Optional(Json)
    friday = Optional(Json)
    saturday = Optional(Json)
    sunday = Optional(Json)
    user = Optional("User")


class SettingAlarm(db.Entity):
    preparation_time = Required(str)
    road_time = Required(str)
    amount = Required(int)
    intervals = Required(str)
    user = Required("User")


class User(db.Entity):
    id = PrimaryKey(int, nullable=False)
    tg_id = Optional(int)
    alarms = Set("SettingAlarm")
    schedule = Optional("Schedule")


"""
Класс, через который можно взаимодействовать с бд
"""


# пример как можно обратить к Schedule и получить время первой пары в понедельник:
# Schedule.monday[0]["time"]

class PostgresDB:
    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        db.bind(provider='postgres', user=f'{user}', password=f'{password}', host=f'{host}', port=f"{port}",
                database=f'{database}')
        db.generate_mapping(create_tables=True)

    @db_session
    def put_week(self, json):
        user = self.find_user_by_id(json["id"])
        if user is None:
            user = User(id=json["id"])
            Schedule(monday=json['mon'], tuesday=json['tue'], wednesday=json['wed'], thursday=json['th'],
                     friday=json['fri'], saturday=json['sat'], sunday=json['sun'], user=user)
        else:
            schedule = self.find_schedule_by_id(json["id"])
            schedule.monday = json['mon']
            schedule.tuesday = json['tue']
            schedule.wednesday = json['wed']
            schedule.thursday = json['th']
            schedule.friday = json['fri']
            schedule.saturday = json['sat']
            schedule.sunday = json['sun']

    @db_session
    def find_schedule_by_id(self, id_user: int) -> Schedule:
        return Schedule.get(lambda s: s.user.id == id_user)

    @db_session
    def update_alarm(self, json):
        alarm = self.find_alarm_by_id(json["id"])
        if alarm is not None:
            alarm.preparation_time = json['prep_time']
            alarm.road_time = json['road_time']
            alarm.amount = json["amount"]
            alarm.intervals = json["intervals"]

    @db_session
    def add_alarm(self, json):
        user = self.find_alarm_by_id(json["id"])
        SettingAlarm(preparation_time=json['prep_time'], road_time=json['road_time'],
                     amount=json["amount"], intervals=json["intervals"], user=user)

    @db_session
    def find_alarm_by_id(self, id_user: int) -> SettingAlarm:
        return SettingAlarm.get(lambda a: a.user.id == id_user)

    @db_session
    def find_user_by_id(self, id_user: int) -> User:
        return User.get(lambda u: u.id == id_user)
