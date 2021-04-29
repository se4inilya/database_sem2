import datetime
from threading import Thread

import consolemenu
import redis


class EventListener(Thread):

    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        pubsub = self.connection.pubsub()
        pubsub.subscribe(['users', 'spam'])
        for item in pubsub.listen():
            if item['type'] == 'message':
                message = '\nПОДІЯ: %s | %s' % (item['data'], datetime.datetime.now())
                print(message)


def admin_menu():
    menu = consolemenu.SelectionMenu(['Користувачі онлайн', 'Топ надсилачі', 'Топ спамери'], title='МЕНЮ АДМІНІСТРАТОРА',
                                     subtitle='Оберіть опцію меню')
    menu.show()
    if menu.is_selected_item_exit():
        exit()
    return menu.selected_option + 1


def main():
    loop = True
    connection = redis.Redis(charset='utf-8', decode_responses=True)
    listener = EventListener(connection)
    listener.setDaemon(True)
    listener.start()

    while loop:
        choice = admin_menu()

        if choice == 1:
            online_users = connection.smembers('online:')
            print('Онлайн користувачі:')
            for index, user in enumerate(online_users):
                print(f'{index + 1}) {user}')

        elif choice == 2:
            top_senders_count = int(input('Скільки топ надсилачів відобразити: '))
            senders = connection.zrange('sent:', 0, top_senders_count - 1, desc=True, withscores=True)
            print('ТОП %s надсилачів' % top_senders_count)
            for index, sender in enumerate(senders):
                print(index + 1, ') ', sender[0], ' - ', int(sender[1]), 'повідомлень')

        elif choice == 3:
            top_spamers_count = int(input('Скільки топ спамерів відобразити: '))
            spamers = connection.zrange('spam:', 0, top_spamers_count - 1, desc=True, withscores=True)
            print('ТОП %s спамерів' % top_spamers_count)
            for index, spamer in enumerate(spamers):
                print(index + 1, ' ', spamer[0], ' - ', int(spamer[1]), ' повідомлень у спамі')

        input('Натисність ЕНТЕР щоб продовжити...')


if __name__ == '__main__':
    main()
