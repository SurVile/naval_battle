import telebot
import random
import re


class Fleet:

    def __init__(self, commander):
        self.fleet_size = 10
        self.ship_num = 3
        self.commander = commander
        self.already_guessed = []
        self.fleet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.enemy_fleet = self.fleet.copy()

    def add_ship(self, ship_index):
        self.fleet[ship_index] = 1
        return self.fleet

    def shoot(self, cell_index):
        self.already_guessed.append(cell_index)
        if self.fleet[cell_index] == 1:
            self.fleet[cell_index] = 0
            return 'попал!'
        else:
            return 'промахнулся...'

    def add_enemy_ship(self, cell_index):
        self.enemy_fleet[cell_index] = 1

    def clear_fleet(self):
        self.fleet.clear()
        return 'Флот очищен'


bot = telebot.TeleBot('7242519489:AAFl-QQAUBadSvrQjWmFFfyHfiBs_XQdXco')


def assembler_fleet(player_fleet, ship_list=[]):
    if player_fleet.commander == 'bot_name':
        for i in range(0, 3):
            player_fleet.add_ship(random.randint(0, 9))
    else:
        for i in ship_list:
            player_fleet.add_ship(int(i))


@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, 'Привет, пользователь!')


@bot.message_handler(commands=['game'])
def start_game(message):
    bot.send_message(message.chat.id, 'Супер! Начинаем игру)')

    bot_fleet = Fleet('bot_name')
    user_fleet = Fleet('user_name')

    assembler_fleet(bot_fleet)

    bot.send_message(message.chat.id, 'Введи через запятую с пробелом 3 индекса ячеек от 0 до 9, в которых будут корабли')

    @bot.message_handler()
    def make_fleet(new_message):
        if re.search(r'^[\d{1}]+,+ +[\d{1}]+,+ +[\d{1}]$', new_message.text):
            assembler_fleet(user_fleet, ship_list=new_message.text.split(', '))
            bot.send_message(new_message.chat.id, 'Начинаем игру!')
            bot.send_message(new_message.chat.id, 'Ваш ход ->')
        else:
            cell = int(new_message.text)

            if cell in bot_fleet.already_guessed:
                bot.send_message(new_message.chat.id, 'Эта ячейка уже отгадана, повторите ход')
            else:
                result = bot_fleet.shoot(cell)
                bot.send_message(new_message.chat.id, f'Ты {result}')
                if result == 'попал!':
                    user_fleet.add_enemy_ship(cell)
                bot.send_message(new_message.chat.id, f'Флот бота: {user_fleet.enemy_fleet}')

                if bot_fleet.fleet.count(1) > 0:
                    bot_cell = random.randint(0, 9)
                    while True:
                        if bot_cell in user_fleet.already_guessed:
                            bot_cell = random.randint(0, 9)
                            continue
                        else:
                            bot.send_message(new_message.chat.id, f'Ход бота - {bot_cell}')
                            result = user_fleet.shoot(bot_cell)
                            bot.send_message(new_message.chat.id, f'Бот {result}')
                            bot.send_message(new_message.chat.id, f'Твой флот: {user_fleet.fleet}')

                            if user_fleet.fleet.count(1) > 0:
                                bot.send_message(new_message.chat.id, 'Следующий ход ->')
                                break
                            else:
                                bot.send_message(new_message.chat.id, 'Ты проиграл...')

                else:
                    bot.send_message(new_message.chat.id, 'Ты победил!!!')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
