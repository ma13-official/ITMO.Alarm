from dialogic.dialog_connector import DialogConnector
from dialogic.dialog_manager import TurnDialogManager
from dialogic.server.flask_server import FlaskServer
from dialogic.cascade import DialogTurn, Cascade

csc = Cascade()


@csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй)')
@csc.add_handler(priority=10, intents=['start'])
# @csc.add_handler(priority=3, checker=is_new_session)
def hello(turn: DialogTurn):
    turn.response_text = 'Привет! Вы в навыке ITMO Alarm, которое поможет вам настроить ' \
                         'будильники под ваше учебное расписание' \
                         'Назовите вашу учебную группу, а я начну строить ваше расписание.'
    turn.suggests.append('Выход')


@csc.add_handler(priority=10, intents=['help', 'Yandex.HELP'])
def do_help(turn: DialogTurn):
    turn.response_text = 'Привет! Вы в навыке ITMO Alarm, которое поможет вам настроить ' \
                         'будильники под ваше учебное расписание' \
                         'Назовите вашу учебную группу, а я начну строить ваше расписание.' \
                         '\nЧтобы выйти, скажите "хватит".'
    turn.suggests.append('Выход')


@csc.add_handler(priority=10, intents=['group'])
def add_group(turn: DialogTurn):
    turn.response_text = 'Отлично, я добавила основные предметы. Давайте разберемся с предметами по выбору.' \
                         ' Вы мне называете поток, а я отвечаю, нашла ли его в расписании. Приступим:'


@csc.add_handler(priority=10, intents=['stop'])
def answer_not_found_group(turn: DialogTurn):
    turn.response_text = 'Не могу найти расписание этой группы. Попробуйте еще раз.'


@csc.add_handler(priority=10, intents=['not_from_itmo'])
def answer_not_itmo_student(turn: DialogTurn):
    turn.response_text = 'Извините, я умею ставить будильники только для студентов университета ИТМО.'
    turn.suggests.append('Выход')


@csc.add_handler(priority=10, intents=['stream'])
def add_stream(turn: DialogTurn):
    turn.response_text = 'Поток найден. Добавила в расписание. Продолжить?'


@csc.add_handler(priority=10, intents=['stop'])
def answer_not_found_stream(turn: DialogTurn):
    turn.response_text = 'Не могу найти этот поток. Давайте попробуем еще раз'


@csc.add_handler(priority=10, intents=['total_exit'])
def total_exit(turn: DialogTurn):
    turn.response_text = 'Была рада помочь!' \
                         'Чтобы обратиться ко мне снова,' \
                         'запустите навык "ITMO.Alarm"'
    # turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=1)
def fallback(turn: DialogTurn):
    turn.response_text = 'Я вас не поняла. Повторите еще раз'
    turn.suggests.append('привет')


dm = TurnDialogManager(cascade=csc)
connector = DialogConnector(dialog_manager=dm)
server = FlaskServer(connector=connector)

if __name__ == '__main__':
    server.parse_args_and_run()
