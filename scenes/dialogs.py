from dialogic.cascade import DialogTurn, Cascade
from dialogic.dialog_connector import DialogConnector
from dialogic.dialog_manager import TurnDialogManager
from dialogic.server.flask_server import FlaskServer

csc = Cascade()


# def is_single_pass(turn: DialogTurn) -> bool:
#     """ Check that a command is passed when the skill is activated """
#     if not turn.ctx.yandex:
#         return False
#     if not turn.ctx.yandex.session.new:
#         return False
#     return bool(turn.ctx.yandex.request.command)


def is_new_session(turn: DialogTurn):
    return turn.ctx.session_is_new() or not turn.text


@csc.add_handler(priority=1, intents=['help'])
def do_help(turn: DialogTurn):
    turn.response_text = 'Помогаю! Вы в навыке ITMO Alarm, который поможет вам настроить будильники под ваше учебное расписание. ' \
                         'Назовите вашу учебную группу, а я начну строить ваше расписание' \
                         '\nЧтобы выйти, скажите "Алиса, стоп".'
    turn.suggests.append('Выход')


@csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй)')
@csc.add_handler(priority=10, intents=['start'])
@csc.add_handler(priority=3, checker=is_new_session)
def hello(turn: DialogTurn):
    turn.next_stage = 'group'
    turn.response_text = 'Привет! Вы в навыке ITMO Alarm, который поможет вам настроить будильники под ваше учебное расписание. ' \
                         'Назовите вашу учебную группу, а я начну строить ваше расписание.'
    turn.suggests.append('Выход')


@csc.add_handler(priority=10, intents=['stop'], stages=['group'])
def stop_do_schedule_before_group(turn: DialogTurn):
    turn.response_text = 'Расписание сформировано без учета предметов по выбору.'
    total_exit()


@csc.add_handler(priority=10, intents=['group'])
def add_group(turn: DialogTurn):
    turn.next_stage = 'stream'
    turn.response_text = 'Отлично, я добавила основные предметы. Давайте разберемся с предметами по выбору. ' \
                         'Вы мне называете поток, а я отвечаю, нашла ли его в расписании. Приступим:'


@csc.add_handler(priority=10, intents=['stop'], stages=['stream'])
def stop_do_schedule_after_group(turn: DialogTurn):
    turn.response_text = 'Расписание сформировано без учета предметов по выбору.'


@csc.add_handler(priority=10, intents=['not_from_itmo'])
def answer_not_itmo_student(turn: DialogTurn):
    turn.response_text = 'Извините, я умею ставить будильники только для студентов университета ИТМО.'
    turn.suggests.append('Выход')


@csc.add_handler(priority=10, intents=['stream'])
def add_stream(turn: DialogTurn):
    turn.next_stage = 'next_stream'
    turn.response_text = 'Поток найден. Добавила в расписание. Продолжить?'
    turn.suggests.append('Да')
    turn.suggests.append('Нет')


@csc.add_handler(priority=10, intents=['next'], stages=['next_stream'])
def add_next_stream(turn: DialogTurn):
    turn.response_text = 'Назовите следующий поток: '


@csc.add_handler(priority=10, intents=['stop'], stages=['next_stream'])
def stop_do_schedule_at_stream(turn: DialogTurn):
    turn.response_text = 'Расписание сформировано.'


@csc.add_handler(priority=10, intents=['total_exit'])
def total_exit(turn: DialogTurn):
    turn.response_text = 'Была рада помочь! ' \
                         'Чтобы обратиться ко мне снова,' \
                         'запустите навык "ITMO.Alarm"'
    # turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=1)
def fallback(turn: DialogTurn):
    if turn.prev_stage == 'group':
        turn.response_text = 'Не могу найти расписание этой группы. Попробуйте еще раз.'
    elif turn.prev_stage == 'stream' or turn.prev_stage == 'next_stream':
        turn.response_text = 'Не могу найти этот поток. Давайте попробуем еще раз'
    else:
        turn.response_text = 'Я вас не поняла. Повторите еще раз'


dm = TurnDialogManager(cascade=csc, intents_file='C:/Users/user/projects/ITMO.Alarm/data/intents.yaml')
connector = DialogConnector(dialog_manager=dm, alice_native_state='session')
handler = connector.serverless_alice_handler

server = FlaskServer(connector=connector)

if __name__ == '__main__':
    server.parse_args_and_run()
