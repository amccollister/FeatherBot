import sqlite3 as sql
from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self):
        pass
    # TODO balance give lottery leaderboard slots flip blackjack?

    def cmd_moneyping(self, *_):
        return "$$$ pong"

    def cmd_balance(self, *_):
        pass

    def cmd_give(self, *_):
        pass

    def cmd_lottery(self, *_):
        pass

    def cmd_leaderboard(self, *_):
        pass

    def cmd_slots(self, *_):
        pass

    #def cmd_flip(self, *_):
       # pass

    def cmd_blackjack(self, *_): # ???
        pass
